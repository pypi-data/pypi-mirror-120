#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Union, Any

import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchmetrics as metrics

# @manual "//github/facebookresearch/hydra:hydra"
from hydra.core.config_store import ConfigStore
from pytorch.recipes.core.conf import ModuleConf
from pytorch.recipes.rec.datamodules.commons import Batch
from pytorch.recipes.utils.config_utils import get_class_name_str
from torchrec import EmbeddingBagCollection, SimpleSparseNN
from torchrec import KeyedJaggedTensor


class SparseNNBinaryClassification(pl.LightningModule):
    def __init__(
        self,
        embedding_bag_collection: EmbeddingBagCollection,
        over_embedding_dim: int = 5,
        hidden_layer_size: int = 20,
    ) -> None:
        super().__init__()
        self.model: SimpleSparseNN = SimpleSparseNN(
            embedding_bag_collection=embedding_bag_collection,
            hidden_layer_size=hidden_layer_size,
            over_embedding_dim=over_embedding_dim,
        )
        self.loss_fn: nn.Module = nn.BCEWithLogitsLoss()
        self.accuracy: metrics.Metric = metrics.Accuracy()

    # pyre-ignore[14] - `forward` overrides method defined in `pl.core.lightning.LightningModule`
    def forward(
        self,
        dense_features: torch.Tensor,
        sparse_features: KeyedJaggedTensor,
    ) -> torch.Tensor:
        output = self.model(dense_features, sparse_features)
        return output.squeeze()

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.Adam(self.model.parameters())

    def _step(
        self,
        batch: Batch,
        batch_idx: int,
        step_phase: str,
    ) -> torch.Tensor:
        logits = self.forward(
            dense_features=batch.dense_features,
            sparse_features=batch.sparse_features,
        )
        loss = self.loss_fn(logits, batch.labels.float())
        preds = torch.sigmoid(logits)
        accuracy = self.accuracy(preds, batch.labels)

        self.log(f"{step_phase}_accuracy", accuracy)
        self.log(f"{step_phase}_loss", loss)
        return loss

    def training_step(
        self,
        batch: Batch,
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> torch.Tensor:
        return self._step(batch, batch_idx, "train")

    def validation_step(
        self,
        batch: Batch,
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> torch.Tensor:
        return self._step(batch, batch_idx, "val")

    def test_step(
        self,
        batch: Batch,
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> torch.Tensor:
        return self._step(batch, batch_idx, "test")


@dataclass
class SparseNNBinaryClassificationModuleConf(ModuleConf):
    _target_: str = get_class_name_str(SparseNNBinaryClassification)


cs: ConfigStore = ConfigStore.instance()

cs.store(
    group="schema/module",
    name="sparsenn_binary_classification",
    node=SparseNNBinaryClassificationModuleConf,
    package="module",
)
