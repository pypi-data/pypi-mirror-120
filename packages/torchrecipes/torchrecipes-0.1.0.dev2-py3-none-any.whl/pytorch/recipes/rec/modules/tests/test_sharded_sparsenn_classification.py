#!/usr/bin/env python3

import os
import unittest
import uuid

import pytorch_lightning as pl
import torch
from pytorch.recipes.rec.accelerators.torchrec import (
    TorchrecAccelerator,
)
from pytorch.recipes.rec.datamodules.random_rec_datamodule import RandomRecDataModule
from pytorch.recipes.rec.modules.sharded_sparsenn_classification import (
    ShardedSparseNNBinaryClassification,
)
from torch.distributed.launcher.api import elastic_launch, LaunchConfig
from torchrec import EmbeddingBagCollection
from torchrec.modules.embedding_configs import EmbeddingBagConfig
from torchrec.tests.utils import skip_if_asan


class TestShardedSparseNNClassification(unittest.TestCase):
    @classmethod
    def _run_trainer(cls) -> None:
        torch.manual_seed(int(os.environ["RANK"]))
        num_embeddings = 100
        embedding_dim = 12

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
        eb_configs = [eb1_config, eb2_config]

        lit_models = []
        datamodules = []
        for _ in range(2):
            ebc = EmbeddingBagCollection(tables=eb_configs, device=torch.device("meta"))
            lit_model = ShardedSparseNNBinaryClassification(
                ebc,
                over_embedding_dim=5,
                hidden_layer_size=20,
            )

            datamodule = RandomRecDataModule(manual_seed=564733621)
            init_batch = next(iter(datamodule.init_loader)).to(lit_model.device)
            with torch.no_grad():
                lit_model(init_batch.dense_features, init_batch.sparse_features)
                lit_model.model.init_data_parallel()

            lit_models.append(lit_model)
            datamodules.append(datamodule)
        lit_model1, lit_model2 = lit_models
        dm1, dm2 = datamodules

        # Load m1 state dicts into m2
        lit_model2.model.load_state_dict(lit_model1.model.state_dict(), strict=False)
        optim1 = lit_model1.configure_optimizers()
        optim2 = lit_model2.configure_optimizers()
        optim2.load_state_dict(optim1.state_dict())

        # train model 1 using lightning
        trainer = pl.Trainer(
            max_epochs=1,
            limit_train_batches=5,
            limit_val_batches=5,
            limit_test_batches=5,
            accelerator=TorchrecAccelerator(),
            weights_summary=None,
            logger=None,
        )
        trainer.fit(lit_model1, datamodule=dm1)

        # train model 2 manually
        train_dataiterator = iter(dm2.train_dataloader())
        for _ in range(5):
            batch = next(train_dataiterator).to(lit_model2.device)
            optim2.zero_grad()
            logits = lit_model2.model(batch.dense_features, batch.sparse_features)
            loss = lit_model2.loss_fn(logits.squeeze(), batch.labels.float())
            loss.backward()
            optim2.step()

        # assert parameters equal
        sd1 = lit_model1.model.state_dict()
        for name, value in lit_model2.model.state_dict().items():
            assert torch.equal(sd1[name], value)

        # assert model evaluation equal
        test_dataiterator = iter(dm2.test_dataloader())
        with torch.no_grad():
            for _ in range(10):
                batch = next(test_dataiterator).to(lit_model2.device)
                assert torch.equal(
                    lit_model2.model(batch.dense_features, batch.sparse_features),
                    lit_model1.model(batch.dense_features, batch.sparse_features),
                )

    @skip_if_asan
    def test_lit_trainer_equivalent_to_non_lit(self) -> None:
        lc = LaunchConfig(
            min_nodes=1,
            max_nodes=1,
            nproc_per_node=2,
            run_id=str(uuid.uuid4()),
            # TODO T100608035 replace with c10d when fixed
            rdzv_backend="zeus",
            rdzv_endpoint="",
            start_method="spawn",
            monitor_interval=1,
            max_restarts=0,
        )

        elastic_launch(config=lc, entrypoint=self._run_trainer)()
