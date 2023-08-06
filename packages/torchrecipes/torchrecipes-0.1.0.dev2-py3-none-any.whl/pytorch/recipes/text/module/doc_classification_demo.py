#!/usr/bin/env python3

# pyre-strict

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Mapping

import hydra
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchmetrics as metrics
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pytext.contrib.pytext_lib.conf import ModelConf, OptimConf, TransformConf
from pytorch.recipes.core.conf import ModuleConf
from pytorch.recipes.core.task_base import TaskBase
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch.text.fb.transforms.model_transform import ModelTransform
from torch.nn.modules import CrossEntropyLoss

logger: logging.Logger = logging.getLogger(__name__)


class DocClassificationModule(
    TaskBase[Mapping[str, torch.Tensor], torch.Tensor, None], pl.LightningModule
):
    """
    Generic module for doc classification
    The components(model, optim etc.) can be configured and instantiated by hydra

    Note: this is a simple demo Module. Please use pytorch.recipes.text.module.doc_classification
    for training, which supports advanced features like FSDP
    """

    # See P340190896. torchscripting fails if annotated at class-level.

    def __init__(
        self,
        transform: TransformConf,
        model: ModelConf,
        optim: OptimConf,
    ) -> None:
        super().__init__()
        self.transform_conf: TransformConf = transform
        self.model_conf: ModelConf = model
        self.optim_conf: OptimConf = optim
        self.loss = CrossEntropyLoss()

        self.transform: Optional[ModelTransform] = None
        self.model: Optional[torch.nn.Module] = None
        self.optimizer: Optional[torch.optim.Optimizer] = None
        self.accuracy: Optional[metrics.Accuracy] = None
        self.fbeta: Optional[metrics.FBeta] = None

    def setup(self, stage: Optional[str]) -> None:
        """
        Called at the beginning of fit and test.
        This is a good hook when you need to build models dynamically or adjust something about them.
        This hook is called on every process when using DDP.

        Args:
            stage: either 'fit' or 'test'
        """
        # skip building model during test. Otherwise, the state dict will be re-initialized
        if stage == "fit":
            self.transform = hydra.utils.instantiate(self.transform_conf)

            transform = self.transform
            assert transform is not None

            self.model = hydra.utils.instantiate(
                self.model_conf,
                out_dim=len(transform.label_names),
                vocab=transform.vocab,
            )

            model = self.model
            assert model is not None

            self.optimizer = hydra.utils.instantiate(
                self.optim_conf,
                model.parameters(),
            )

        transform = self.transform
        assert transform is not None

        # metrics depend on transform, which is not pickle-able yet
        self.accuracy = metrics.Accuracy()
        self.fbeta = metrics.FBeta(
            num_classes=len(transform.label_names), average="macro"
        )

    # pyre-ignore[14]: This is for torchscript compatibility.
    def forward(self, batch: Dict[str, Any]) -> torch.Tensor:
        transform = self.transform
        model = self.model
        assert transform is not None and model is not None

        return model(transform(batch))

    def configure_optimizers(self) -> torch.optim.Optimizer:
        optimizer = self.optimizer
        assert optimizer is not None
        return optimizer

    def training_step(
        self,
        batch: Mapping[str, torch.Tensor],
        batch_idx: int,
        *args: Any,
        **kwargs: Any
    ) -> torch.Tensor:
        model = self.model
        assert model is not None

        logits = model(batch)
        loss = self.loss(logits, batch["label_ids"])
        self.log("train_loss", loss)
        return loss

    def validation_step(
        self,
        batch: Mapping[str, torch.Tensor],
        batch_idx: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        model = self.model
        assert model is not None
        accuracy, fbeta = self.accuracy, self.fbeta
        assert accuracy is not None and fbeta is not None

        logits = model(batch)
        loss = self.loss(logits, batch["label_ids"])
        scores = F.softmax(logits)

        accuracy(scores, batch["label_ids"])
        fbeta(scores, batch["label_ids"])
        self.log("val_loss", loss)
        self.log("val_acc", accuracy)
        self.log("val_f1", fbeta)

    def test_step(
        self,
        batch: Mapping[str, torch.Tensor],
        batch_idx: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        model = self.model
        assert model is not None
        accuracy, fbeta = self.accuracy, self.fbeta
        assert accuracy is not None and fbeta is not None

        logits = model(batch)
        loss = self.loss(logits, batch["label_ids"])
        scores = F.softmax(logits)

        accuracy(scores, batch["label_ids"])
        fbeta(scores, batch["label_ids"])
        self.log("test_loss", loss)
        self.log("test_acc", accuracy)
        self.log("test_f1", fbeta)

    def on_load_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        This hook will be called before loading state_dict from a checkpoint.
        setup("fit") will built the model before loading state_dict

        Args:
            checkpoint: A dictionary with variables from the checkpoint.
        """
        self.setup("fit")


@dataclass
class DocClassificationModuleConf(ModuleConf):
    _target_: str = get_class_name_str(DocClassificationModule)
    # pyre-fixme[4]
    transform: Any = MISSING
    # pyre-fixme[4]
    model: Any = MISSING
    # pyre-fixme[4]
    optim: Any = MISSING


cs: ConfigStore = ConfigStore.instance()


cs.store(
    group="schema/module",
    name="doc_classification",
    node=DocClassificationModuleConf,
    package="module",
)
