#!/usr/bin/env python3
from itertools import combinations
from typing import List, Tuple

import torch
from torch import nn
from torchrec.fb.experimental.dynamic_embedding_modules import (
    DynamicEmbeddingBagCollection,
)
from torchrec.sparse.jagged_tensor import (
    KeyedJaggedTensor,
    KeyedTensor,
)


"""
Notations uses throughout:

F: number of sparseFeatures
D: embedding_dimension of sparse features
B: batch_size
num_features: number of dense features

"""


class SparseArch(nn.Module):
    """
    Processes the Sparse Features of SparseNN. Does Embedding Lookup for all
    EmbeddingBag and Embedding features of each collection.

    Constructor Args:
        embedding_bag_collection: DynamicEmbeddingBagCollection,

    Call Args:
        features: KeyedJaggedTensor,

    Returns:
        KeyedJaggedTensor - size F * D X B

    Example:
        >>> eb1_config = EmbeddingBagConfig(
            name="t1", embedding_dim=3, num_embeddings=10, feature_names=["f1"]
        )
        eb2_config = EmbeddingBagConfig(
            name="t2", embedding_dim=4, num_embeddings=10, feature_names=["f2"]
        )
        ebc_config = DynamicEmbeddingBagCollectionConfig(tables=[eb1_config, eb2_config])

        ebc = DynamicEmbeddingBagCollection(config=ebc_config)

        #     0       1        2  <-- batch
        # 0   [0,1] None    [2]
        # 1   [3]    [4]    [5,6,7]
        # ^
        # feature
        features = KeyedJaggedTensor.from_offsets_sync(
            keys=["f1", "f2"],
            values=torch.tensor([0, 1, 2, 3, 4, 5, 6, 7]),
            offsets=torch.tensor([0, 2, 2, 3, 4, 5, 8]),
        )

        sparse_arch(features)
    """

    def __init__(self, embedding_bag_collection: DynamicEmbeddingBagCollection) -> None:
        super().__init__()
        self.embedding_bag_collection: DynamicEmbeddingBagCollection = (
            embedding_bag_collection
        )

    def forward(
        self,
        features: KeyedJaggedTensor,
    ) -> KeyedTensor:
        return self.embedding_bag_collection(features)


class DenseArch(nn.Module):
    """
    Processes the dense features of SparseNN model. Output layer is sized to
    the embedding_dimension of the DynamicEmbeddingBagCollection embeddings

    Constructor Args:
        hidden_layer_size: int
        embedding_dim: int - the same size of the embedding_dimension of sparseArch

    Call Args:
        features: torch.Tensor  - size B X num_features

    Returns:
        torch.Tensor  - size B X D

    Example:
        >>> B = 20
        D = 3
        dense_arch = DenseArch(hidden_layer_size=10, embedding_dim=D)
        dense_embedded = dense_arch(torch.rand((B, 10)))
    """

    def __init__(self, hidden_layer_size: int, embedding_dim: int) -> None:
        super().__init__()
        self.model: nn.Module = nn.Sequential(
            nn.LazyLinear(hidden_layer_size),
            nn.ReLU(),
            nn.LazyLinear(embedding_dim),
            nn.ReLU(),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.model(features)


class InteractionArch(nn.Module):
    """
    Processes the output of both SparseArch (sparse_features) and DenseArch
    (dense_features). Returns the pairwise dot product of each sparse feature pair,
    the dot product of each sparse features with the output of the dense layer,
    and the dense layer itself (all concatenated)

    Constructor Args:
        sparse_feature_names: List[str] - length of F

    Call Args:
        dense_features: torch.Tensor  - size B X D
        sparse_features: KeyedJaggedTensor - size F * D X B

    Returns:
        torch.Tensor - B X (D + F + F choose 2)

    Example:
        >>> D = 3
        B = 10
        keys = ["f1", "f2"]
        F = len(keys)
        inter_arch = InteractionArch(sparse_feature_names=keys)

        dense_features = torch.rand((B, D))

        sparse_features = KeyedTensor(
            keys=keys,
            length_per_key=[D, D],
            values=torch.rand((B, D * F)),
        )

        #  B X (D + F + F choose 2)
        concat_dense = inter_arch(dense_features, sparse_features)
    """

    def __init__(self, sparse_feature_names: List[str]) -> None:
        super().__init__()
        self.sparse_feature_names: List[str] = sparse_feature_names
        self.sparse_combinations: List[Tuple[str, str]] = list(
            combinations(sparse_feature_names, 2)
        )

    def forward(
        self, dense_features: torch.Tensor, sparse_features: KeyedTensor
    ) -> torch.Tensor:
        if len(self.sparse_feature_names) == 0:
            return dense_features

        interactions: List[torch.Tensor] = []
        # dense/sparse interaction
        # size B X F
        for feature_name in self.sparse_feature_names:
            sparse_values = sparse_features[feature_name]
            dots = torch.sum(sparse_values * dense_features, dim=1)
            # dots is size B
            interactions.append(dots)

        # sparse/sparse interaction
        # size B X (F choose 2)
        for (f1, f2) in self.sparse_combinations:
            f1_values = sparse_features[f1]
            f2_values = sparse_features[f2]
            dots = torch.sum(f1_values * f2_values, dim=1)
            interactions.append(dots)

        interactions_tensor = torch.stack(interactions).transpose(1, 0)
        return torch.cat((dense_features, interactions_tensor), dim=1)


class OverArch(nn.Module):
    """
    Final Arch of SparseNN - simple MLP over OverArch

    Constructor Args:
        output_dim: int

    Call Args:
        features: torch.Tensor

    Returns:
        torch.Tensor  - size B X output_dim

    Example:
        >>> B = 20
        D = 3
        over_arch = OverArch(output_dim=5)
        logits = over_arch(torch.rand((B, 10)))
    """

    def __init__(self, output_dim: int) -> None:
        super().__init__()
        self.model: nn.Module = nn.Sequential(
            nn.LazyLinear(output_dim),
            nn.ReLU(),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.model(features)


class SimpleSparseNN(nn.Module):
    """
    Basic recsys module. Processes sparse features by
    learning pooled embeddings for each feature. Learns the relationship between
    dense features and sparse features by projecting dense features into the same
    embedding space. Also, learns the pairwise relationships between sparse features.

    The module assumes all sparse features have the same embedding dimension
    (i.e, each EmbeddingBagConfig uses the same embedding_dim)

    Constructor Args:
        embedding_bag_collection: DynamicEmbeddingBagCollection,
        hidden_layer_size: int,
        output_dim: int,

    Call Args:
        dense_features: torch.Tensor,
        sparse_features: KeyedJaggedTensor,

    Returns:
        torch.Tensor - logits with size B X output_dim

    Example:
        >>> B = 2
        D = 8

        eb1_config = EmbeddingBagConfig(
            name="t1", embedding_dim=D, num_embeddings=100, feature_names=["f1", "f3"]
        )
        eb2_config = EmbeddingBagConfig(
            name="t2",
            embedding_dim=D,
            num_embeddings=100,
            feature_names=["f2"],
        )
        ebc_config = DynamicEmbeddingBagCollectionConfig(tables=[eb1_config, eb2_config])

        ebc = DynamicEmbeddingBagCollection(config=ebc_config)
        sparse_nn = SimpleSparseNN(
            embedding_bag_collection=ebc, hidden_layer_size=20, output_dim=5
        )

        features = torch.rand((B, 100))

        #     0       1
        # 0   [1,2] [4,5]
        # 1   [4,3] [2,9]
        # ^
        # feature
        sparse_features = KeyedJaggedTensor.from_offsets_sync(
            keys=["f1", "f3"],
            values=torch.tensor([1, 2, 4, 5, 4, 3, 2, 9]),
            offsets=torch.tensor([0, 2, 4, 6, 8]),
        )

        logits = sparse_nn(
            dense_features=features,
            sparse_features=sparse_features,
        )
    """

    def __init__(
        self,
        embedding_bag_collection: DynamicEmbeddingBagCollection,
        hidden_layer_size: int,
        output_dim: int,
    ) -> None:
        super().__init__()
        assert (
            len(embedding_bag_collection.embedding_bag_configs) > 0
        ), "At least one embedding bag is required"
        for i in range(1, len(embedding_bag_collection.embedding_bag_configs)):
            conf_prev = embedding_bag_collection.embedding_bag_configs[i - 1]
            conf = embedding_bag_collection.embedding_bag_configs[i]
            assert (
                conf_prev.embedding_dim == conf.embedding_dim
            ), "All EmbeddingBagConfigs must have the same dimension"
        embedding_dim: int = embedding_bag_collection.embedding_bag_configs[
            0
        ].embedding_dim

        feature_names = []
        for conf in embedding_bag_collection.embedding_bag_configs:
            for feat in conf.feature_names:
                feature_names.append(feat)

        self.sparse_arch = SparseArch(embedding_bag_collection)
        self.dense_arch = DenseArch(
            hidden_layer_size=hidden_layer_size, embedding_dim=embedding_dim
        )
        self.inter_arch = InteractionArch(sparse_feature_names=feature_names)
        self.over_arch = OverArch(output_dim)

    def forward(
        self,
        dense_features: torch.Tensor,
        sparse_features: KeyedJaggedTensor,
    ) -> torch.Tensor:
        embedded_dense = self.dense_arch(dense_features)
        embedded_sparse = self.sparse_arch(sparse_features)
        concatenated_dense = self.inter_arch(
            dense_features=embedded_dense, sparse_features=embedded_sparse
        )
        logits = self.over_arch(concatenated_dense)
        return logits
