#!/usr/bin/env python3

import unittest

import pytorch_lightning as pl
from pytorch.recipes.rec.datamodules.random_rec_datamodule import RandomRecDataModule
from pytorch.recipes.rec.modules.sparsenn_classification import (
    SparseNNBinaryClassification,
)
from torchrec import EmbeddingBagCollection
from torchrec.modules.embedding_configs import EmbeddingBagConfig


class TestSparseNNClassification(unittest.TestCase):
    def test_train_model(self) -> None:
        num_embeddings = 100
        embedding_dim = 10

        eb1_config = EmbeddingBagConfig(
            name="t1",
            embedding_dim=embedding_dim,
            num_embeddings=num_embeddings,
            feature_names=["f1", "f3"],
        )
        eb2_config = EmbeddingBagConfig(
            name="t2",
            embedding_dim=embedding_dim,
            num_embeddings=num_embeddings,
            feature_names=["f2"],
        )
        ebc = EmbeddingBagCollection(tables=[eb1_config, eb2_config])

        model = SparseNNBinaryClassification(ebc)
        datamodule = RandomRecDataModule()

        trainer = pl.Trainer(
            max_epochs=3,
            limit_train_batches=100,
            limit_val_batches=100,
            limit_test_batches=100,
        )

        batch = next(iter(datamodule.init_loader))
        model(
            dense_features=batch.dense_features,
            sparse_features=batch.sparse_features,
        )
        trainer.fit(model, datamodule=datamodule)
        trainer.test(model, datamodule=datamodule)
