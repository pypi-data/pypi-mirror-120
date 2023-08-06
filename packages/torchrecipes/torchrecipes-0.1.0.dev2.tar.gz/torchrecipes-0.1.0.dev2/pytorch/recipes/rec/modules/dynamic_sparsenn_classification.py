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
from pytorch.recipes.rec.modules.dynamic_sparsenn import SimpleSparseNN
from pytorch.recipes.utils.config_utils import get_class_name_str
from torchrec import KeyedJaggedTensor
from torchrec.fb.experimental.dynamic_embedding_modules import (
    DynamicEmbeddingBagCollection,
)


class SparseNNBinaryClassification(pl.LightningModule):
    def __init__(
        self,
        embedding_bag_collection: DynamicEmbeddingBagCollection,
        output_dim: int = 5,
        hidden_layer_size: int = 20,
    ) -> None:
        super().__init__()
        self.model: SimpleSparseNN = SimpleSparseNN(
            embedding_bag_collection=embedding_bag_collection,
            hidden_layer_size=hidden_layer_size,
            output_dim=output_dim,
        )
        self.final = nn.Linear(output_dim, 1)
        self.loss_fn: nn.Module = nn.BCEWithLogitsLoss()
        self.accuracy: metrics.Metric = metrics.Accuracy()

    # pyre-ignore[14] - `forward` overrides method defined in `pl.core.lightning.LightningModule`
    def forward(
        self,
        dense_features: torch.Tensor,
        sparse_features: KeyedJaggedTensor,
    ) -> torch.Tensor:
        output_embedding = self.model(dense_features, sparse_features)
        return self.final(output_embedding).squeeze()

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.Adam(self.model.parameters())

    def _step(
        self,
        batch: Dict[str, Union[torch.Tensor, KeyedJaggedTensor]],
        batch_idx: int,
        step_phase: str,
    ) -> torch.Tensor:
        dense_features = batch["dense_features"]
        assert isinstance(dense_features, torch.Tensor)
        sparse_features = batch["sparse_features"]
        assert isinstance(sparse_features, KeyedJaggedTensor)
        labels = batch["labels"]
        assert isinstance(labels, torch.Tensor)
        logits = self.forward(
            dense_features=dense_features,
            sparse_features=sparse_features,
        )
        loss = self.loss_fn(logits, labels.float())
        preds = torch.sigmoid(logits)
        accuracy = self.accuracy(preds, labels)

        self.log(f"{step_phase}_accuracy", accuracy)
        self.log(f"{step_phase}_loss", loss)
        return loss

    def training_step(
        self,
        batch: Dict[str, Union[torch.Tensor, KeyedJaggedTensor]],
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> torch.Tensor:
        return self._step(batch, batch_idx, "train")

    def validation_step(
        self,
        batch: Dict[str, Union[torch.Tensor, KeyedJaggedTensor]],
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> torch.Tensor:
        return self._step(batch, batch_idx, "val")

    def test_step(
        self,
        batch: Dict[str, Union[torch.Tensor, KeyedJaggedTensor]],
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
