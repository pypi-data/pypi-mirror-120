#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved


# pyre-ignore-all-errors

# Ignore all pyre errors in this file for now since it should be refactored to use Standard DocClassificationModule soon
import logging
from typing import Any, Dict, cast

import hydra
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchmetrics as metrics
from fairscale.nn import wrap
from pytext.contrib.pytext_lib.conf import (
    DocClassificationDataModuleConf,
    DocTransformConf,
    ModelConf,
    OptimConf,
    SchedulerConf,
    TransformConf,
)
from pytext.contrib.pytext_lib.utils.usage import log_class_usage
from pytext.utils.file_io import PathManager
from pytorch.recipes.text.module.common import CheckpointMixin
from torch.serialization import default_restore_location

logger: logging.Logger = logging.getLogger(__name__)


class DocClassificationTask(CheckpointMixin, pl.LightningModule):
    """
    Generic task for doc classification
    The components(model, optim etc.) can be configured and instantiated by hydra

    Example:
            .. code-block:: python

                with initialize_config_module("pytext.contrib.pytext_lib.conf"):
                    cfg = compose(
                        config_name="pytext_config",
                        overrides=[
                            "task/transform=doc_transform",
                            "task/datamodule=doc_classification_dummy",
                            "task/model=xlmr_dummy",
                            "task/optim=adamw",
                            "trainer=cpu",
                            "trainer.max_epochs=10",
                        ],
                    )
                task = hydra.utils.instantiate(cfg.task, _recursive_=False)
                transform = hydra.utils.instantiate(cfg.task.transform, _recursive_=False)
                datamodule = hydra.utils.instantiate(cfg.task.datamodule, transform=transform, _recursive_=False)
                trainer = Trainer(**cfg.trainer)
                trainer.fit(task, datamodule=datamodule)
                trainer.test(task, datamodule=datamodule)
    """

    def __init__(
        self,
        transform: TransformConf,
        datamodule: DocClassificationDataModuleConf,
        model: ModelConf,
        optim: OptimConf,
        scheduler: SchedulerConf = None,
        enable_auc_metric: bool = False,
        enable_configure_sharded_model: bool = False,
        encoder_eval_mode: bool = False,
        pretrained_checkpoint_path: str = "",
    ) -> None:
        super().__init__()
        self.transform_conf = transform
        # Keeping datamodule_conf for now so we don't refactor TaskConf
        self.datamodule_conf = datamodule
        self.model_conf = model
        self.optim_conf = optim
        self.scheduler_conf = scheduler
        self.loss = torch.nn.CrossEntropyLoss()
        self.enable_configure_sharded_model = enable_configure_sharded_model
        self.enable_auc_metric = enable_auc_metric
        self.encoder_eval_mode = encoder_eval_mode
        self.pretrained_checkpoint_path = pretrained_checkpoint_path
        log_class_usage(self.__class__)

        # metrics depend on transform, which is not pickle-able yet
        num_classes = len(hydra.utils.instantiate(self.transform_conf).label_names)
        self.valid_acc = metrics.Accuracy()
        self.valid_f1 = metrics.FBeta(num_classes=num_classes, average="macro")
        self.test_acc = metrics.Accuracy()
        self.test_f1 = metrics.FBeta(num_classes=num_classes, average="macro")
        if self.enable_auc_metric:
            self.valid_aucroc = metrics.AUROC(
                num_classes=num_classes, compute_on_step=False
            )
            self.test_aucroc = metrics.AUROC(
                num_classes=num_classes, compute_on_step=False
            )

    def setup(self, stage: str) -> None:
        """
        Called at the beginning of fit and test.
        This is a good hook when you need to build models dynamically or adjust something about them.
        This hook is called on every process when using DDP.

        Args:
            stage: either 'fit' or 'test'
        """
        # skip building model during test. Otherwise, the state dict will be re-initialized
        if stage == "test":
            return
        # resetting call_configure_sharded_model_hook attribute so that we could configure model
        self.call_configure_sharded_model_hook = False

        self.transform = hydra.utils.instantiate(self.transform_conf)
        num_classes = len(self.transform.label_names)
        self.model = hydra.utils.instantiate(
            self.model_conf,
            out_dim=num_classes,
            vocab=self.transform.vocab,
        )

        if self.pretrained_checkpoint_path:
            checkpoint_dict = torch.load(
                PathManager.get_local_path(self.pretrained_checkpoint_path),
                map_location=lambda s, l: default_restore_location(s, "cpu"),
            )
            self.load_state_dict(checkpoint_dict["state_dict"])
            print(f"Loaded state dict from {self.pretrained_checkpoint_path}")

    def forward(self, batch: Dict[str, Any]) -> torch.Tensor:
        return self.model(self.transform(batch))

    def training_step(self, batch, batch_idx):
        logits = self.model(batch)
        loss = self.loss(logits, batch["label_ids"])
        self.log("train_loss", loss)
        self.log("learning_rate", self.optimizer.param_groups[0]["lr"])
        return loss

    def validation_step(self, batch, batch_idx) -> None:
        logits = self.model(batch)
        assert "label_ids" in batch, batch
        loss = self.loss(logits, batch["label_ids"])
        scores = F.softmax(logits)
        # We should call update here as we are not using the output
        self.valid_acc.update(scores, batch["label_ids"])
        self.valid_f1.update(scores, batch["label_ids"])
        self.log("val_loss", loss)
        self.log("val_acc", self.valid_acc)
        self.log("val_f1", self.valid_f1)
        if self.enable_auc_metric:
            self.valid_aucroc.update(scores, batch["label_ids"])
            self.log("val_aucroc", self.valid_aucroc, metric_attribute="valid_aucroc")

    def test_step(self, batch, batch_idx) -> None:
        logits = self.model(batch)
        loss = self.loss(logits, batch["label_ids"])
        scores = F.softmax(logits)
        # We should call update here as we are not using the output
        self.test_acc.update(scores, batch["label_ids"])
        self.test_f1.update(scores, batch["label_ids"])
        self.log("test_loss", loss)
        self.log("test_acc", self.test_acc)
        self.log("test_f1", self.test_f1)
        if self.enable_auc_metric:
            self.test_aucroc.update(scores, batch["label_ids"])
            self.log("test_aucroc", self.test_aucroc, metric_attribute="test_aucroc")

    def configure_optimizers(
        self,
    ) -> Any:
        # we put optimizer instantiation in `configure_optimizers` as we
        # need wrapped model's parameters
        self.optimizer = hydra.utils.instantiate(
            self.optim_conf, self.model.parameters()
        )
        self.scheduler = hydra.utils.instantiate(self.scheduler_conf, self.optimizer)
        if self.scheduler is not None:
            return [self.optimizer], [{"scheduler": self.scheduler, "interval": "step"}]
        else:
            return self.optimizer

    def configure_sharded_model(self) -> None:
        if not self.enable_configure_sharded_model:
            return
        # wrap is annotation, which will be enabled inside
        # `enable_wrap` context manager
        if hasattr(self.model, "configure_sharded_model"):
            self.model.configure_sharded_model()
        self.model = wrap(self.model)

        num_model_parameters = sum(p.numel() for p in self.model.parameters())
        logger.info(
            f"After configuring sharded model, model's number of parameters is: {num_model_parameters}."
        )

    def on_load_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        This hook will be called before loading state_dict from a checkpoint.
        setup("fit") will built the model before loading state_dict

        Args:
            checkpoint: A dictionary with variables from the checkpoint.
        """
        self.setup("fit")

    def on_train_epoch_start(self) -> None:
        if self.encoder_eval_mode and hasattr(self.model, "encoder"):
            self.model.encoder.eval()
            logger.info("Set encoder to eval mode.")
