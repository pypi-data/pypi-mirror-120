#!/usr/bin/env python3

import argparse
import sys
from typing import List

import pytorch_lightning as pl
import torch
from pytorch.recipes.rec.accelerators.torchrec import (
    TorchrecAccelerator,
)
from pytorch.recipes.rec.datamodules.criteo_datamodule import CriteoDataModule
from pytorch.recipes.rec.modules.sharded_sparsenn_classification import (
    ShardedSparseNNBinaryClassification,
)
from stl.lightning.callbacks.model_checkpoint import ModelCheckpoint
from stl.lightning.loggers import ManifoldTensorBoardLogger
from torchrec import EmbeddingBagCollection
from torchrec.modules.embedding_configs import EmbeddingBagConfig


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="torchrec + lightning app")
    parser.add_argument(
        "--epochs", type=int, default=3, help="number of epochs to train"
    )
    parser.add_argument(
        "--batch_size", type=int, default=32, help="batch size to use for training"
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=2,
        help="number of dataloader workers",
    )
    parser.add_argument(
        "--limit_train_batches",
        type=int,
        default=100,
        help="number of train batches",
    )
    parser.add_argument(
        "--limit_val_batches",
        type=int,
        default=100,
        help="number of val batches",
    )
    parser.add_argument(
        "--limit_test_batches",
        type=int,
        default=100,
        help="number of test batches",
    )
    parser.add_argument(
        "--manifold_bucket",
        type=str,
        help="manifold bucket for tensorboard logs and checkpointing",
        required=False,
    )
    parser.add_argument(
        "--tb_manifold_path",
        type=str,
        help="path in manifold bucket for tensorboard logs",
        required=False,
    )
    parser.add_argument("--load_path", type=str, help="checkpoint path to load from")
    parser.add_argument(
        "--checkpoint_output_path",
        type=str,
        help="path to place checkpoints",
        required=False,
    )
    parser.add_argument(
        "--undersampling_rate",
        type=float,
        help="Desired proportion of zero-labeled samples to retain (i.e. undersampling "
        "zero-labeled rows). Ex. 0.3 indicates only 30% of the rows with label 0 will "
        "be kept. All rows with label 1 will be kept. Value should be between 0 and "
        "1. When not supplied, no undersampling occurs.",
    )
    parser.add_argument(
        "--seed",
        type=float,
        help="Random seed for reproducibility.",
    )

    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)

    datamodule = CriteoDataModule(
        num_days=1,
        batch_size=3,
        num_days_test=1,
        num_workers=args.num_workers,
        undersampling_rate=args.undersampling_rate,
        seed=args.seed,
    )
    num_embeddings = datamodule.num_embeddings
    keys = datamodule.keys
    embedding_dim = 64

    eb_configs = [
        EmbeddingBagConfig(
            name=f"t_{feature_name}",
            embedding_dim=embedding_dim,
            num_embeddings=num_embeddings,
            feature_names=[feature_name],
        )
        for feature_name in keys
    ]
    sharded_model = ShardedSparseNNBinaryClassification(
        EmbeddingBagCollection(tables=eb_configs, device=torch.device("meta"))
    )

    callbacks = []
    if args.checkpoint_output_path is not None:
        callbacks.append(
            ModelCheckpoint(
                save_top_k=-1,
                has_user_data=False,
                ttl_days=1,
                monitor=None,
                dirpath=args.checkpoint_output_path,
            )
        )
    if args.load_path:
        print(f"loading checkpoint: {args.load_path}...")
        sharded_model.load_from_checkpoint(checkpoint_path=args.load_path)

    if args.manifold_bucket is not None and args.tb_manifold_path is not None:
        logger = ManifoldTensorBoardLogger(
            manifold_bucket=args.manifold_bucket,
            manifold_path=args.tb_manifold_path,
            has_user_data=False,
        )
    else:
        logger = None

    datamodule.setup()
    batch = next(iter(datamodule.train_dataloader())).to(sharded_model.device)
    with torch.no_grad():
        sharded_model(batch.dense_features, batch.sparse_features)

    trainer = pl.Trainer(
        logger=logger,
        max_epochs=args.epochs,
        callbacks=callbacks,
        limit_train_batches=args.limit_train_batches,
        limit_val_batches=args.limit_val_batches,
        limit_test_batches=args.limit_test_batches,
        accelerator=TorchrecAccelerator(),
        # TODO: find a better way to deal with lazy modules in lightning w/o disabling weights_summary
        weights_summary=None,
    )

    trainer.fit(sharded_model, datamodule=datamodule)
    trainer.test(sharded_model, datamodule=datamodule)


if __name__ == "__main__":
    main(sys.argv[1:])
