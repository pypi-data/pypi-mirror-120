from dataclasses import dataclass

import torch
from torchrec.sparse.jagged_tensor import KeyedJaggedTensor


@dataclass
class Batch:
    dense_features: torch.Tensor
    sparse_features: KeyedJaggedTensor
    labels: torch.Tensor

    def to(self, device: torch.device, non_blocking: bool = False) -> "Batch":
        return Batch(
            dense_features=self.dense_features.to(
                device=device, non_blocking=non_blocking
            ),
            sparse_features=self.sparse_features.to(
                device=device, non_blocking=non_blocking
            ),
            labels=self.labels.to(device=device, non_blocking=non_blocking),
        )

    def record_stream(self, stream: torch.cuda.streams.Stream) -> None:
        self.dense_features.record_stream(stream)
        self.sparse_features.record_stream(stream)
        self.labels.record_stream(stream)
