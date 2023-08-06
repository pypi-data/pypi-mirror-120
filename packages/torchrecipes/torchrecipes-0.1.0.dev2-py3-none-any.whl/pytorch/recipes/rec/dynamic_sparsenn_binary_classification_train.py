#!/usr/bin/env python3

import argparse
import sys
from typing import List

import pytorch_lightning as pl
from pytorch.recipes.rec.datamodules.criteo_datamodule import CriteoDataModule
from pytorch.recipes.rec.modules.dynamic_sparsenn_classification import (
    SparseNNBinaryClassification,
)
from stl.lightning.callbacks.model_checkpoint import ModelCheckpoint
from stl.lightning.loggers import ManifoldTensorBoardLogger
from torchrec.fb.experimental.dynamic_embedding_configs import DynamicEmbeddingBagConfig
from torchrec.fb.experimental.dynamic_embedding_modules import (
    DynamicEmbeddingBagCollection,
)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="torchrec ML app")
    parser.add_argument(
        "--epochs", type=int, default=3, help="number of epochs to train"
    )
    parser.add_argument(
        "--batch_size", type=int, default=32, help="batch size to use for training"
    )
    parser.add_argument("--load_path", type=str, help="checkpoint path to load from")
    parser.add_argument(
        "--output_path",
        type=str,
        help="path to place checkpoints and model outputs",
        required=True,
    )

    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)

    datamodule = CriteoDataModule(num_days=22, batch_size=3, num_days_test=2)
    num_embeddings = datamodule.num_embeddings
    keys = datamodule.keys
    embedding_dim = 64

    eb_configs = [
        DynamicEmbeddingBagConfig(
            name=f"t_{feature_name}",
            embedding_dim=embedding_dim,
            max_embedding_size=num_embeddings,
            feature_names=[feature_name],
        )
        for feature_name in keys
    ]
    model = SparseNNBinaryClassification(
        DynamicEmbeddingBagCollection(tables=eb_configs)
    )

    checkpoint_callback = ModelCheckpoint(
        save_top_k=-1,
        has_user_data=False,
        ttl_days=1,
        monitor=None,
    )
    if args.load_path:
        print(f"loading checkpoint: {args.load_path}...")
        model.load_from_checkpoint(checkpoint_path=args.load_path)

    logger = ManifoldTensorBoardLogger()

    trainer = pl.Trainer(
        logger=logger,
        max_epochs=args.epochs,
        callbacks=[checkpoint_callback],
        limit_train_batches=100,
        limit_val_batches=100,
        limit_test_batches=100,
        log_every_n_steps=1,
        # TODO: find a better way to deal with lazy modules in lightning w/o disabling weights_summary
        weights_summary=None,
    )

    trainer.fit(model, datamodule=datamodule)
    trainer.test(model, datamodule=datamodule)


if __name__ == "__main__":
    main(sys.argv[1:])
