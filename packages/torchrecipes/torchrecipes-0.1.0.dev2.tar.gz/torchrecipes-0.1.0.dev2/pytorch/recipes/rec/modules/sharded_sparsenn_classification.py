#!/usr/bin/env python3
import os
from typing import Any, List, TypeVar, cast

import pytorch_lightning as pl
import torch
import torch.distributed as dist
import torch.nn as nn
import torchmetrics as metrics
from pytorch.recipes.rec.datamodules.criteo_datamodule import Batch
from torchrec import EmbeddingBagCollection, SimpleSparseNN
from torchrec import KeyedJaggedTensor
from torchrec.distributed.embedding import EmbeddingBagCollectionSharder
from torchrec.distributed.embedding_types import EmbeddingComputeKernel
from torchrec.distributed.model_parallel import DistributedModelParallel
from torchrec.distributed.types import ShardingType, ModuleSharder
from torchrec.optim.keyed import KeyedOptimizerWrapper

M = TypeVar("M", bound=nn.Module)


class TWEmbeddingBagCollectionSharder(EmbeddingBagCollectionSharder[M]):
    @property
    def sharding_types(self) -> List[str]:
        return [ShardingType.TABLE_WISE.value, ShardingType.DATA_PARALLEL.value]

    def compute_kernels(self, sharding_type: str, device: torch.device) -> List[str]:
        return [
            # restrict to DENSE until T98586878 is fixed
            EmbeddingComputeKernel.DENSE.value,
        ]


class ShardedSparseNNBinaryClassification(pl.LightningModule):
    def __init__(
        self,
        embedding_bag_collection: EmbeddingBagCollection,
        over_embedding_dim: int = 5,
        hidden_layer_size: int = 20,
    ) -> None:
        super().__init__()

        rank = int(os.environ["LOCAL_RANK"])
        if torch.cuda.is_available():
            device = torch.device(f"cuda:{rank}")
            backend = "nccl"
            torch.cuda.set_device(device)
        else:
            device = torch.device("cpu")
            backend = "gloo"

        if not torch.distributed.is_initialized():
            dist.init_process_group(backend=backend)
        self.to(device=device)

        model = SimpleSparseNN(
            embedding_bag_collection=embedding_bag_collection,
            hidden_layer_size=hidden_layer_size,
            over_embedding_dim=over_embedding_dim,
            dense_device=device,
            sparse_device=torch.device("meta"),
        )
        sharders = cast(
            List[ModuleSharder[nn.Module]],
            [TWEmbeddingBagCollectionSharder()],
        )

        self.model = DistributedModelParallel(
            module=model,
            device=device,
            sharders=sharders,
            init_data_parallel=False,
        )
        self.loss_fn: nn.Module = nn.BCEWithLogitsLoss()
        self.accuracy: metrics.Metric = metrics.Accuracy().to(device=device)

    # pyre-ignore[14] - `forward` overrides method defined in `pl.core.lightning.LightningModule`
    def forward(
        self,
        dense_features: torch.Tensor,
        sparse_features: KeyedJaggedTensor,
    ) -> torch.Tensor:
        logits = self.model(dense_features, sparse_features)
        return logits.squeeze()

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return KeyedOptimizerWrapper(
            dict(self.model.named_parameters()),
            lambda params: torch.optim.SGD(params, lr=0.01),
        )

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
