#!/usr/bin/env python3

import argparse
import sys
from typing import List

import pytorch_lightning as pl
import torch
from aml.ml_foundation.exp_platform.e3.data.p_report_datamodule import (
    PReportTmpTableDataModule,
)
from aml.ml_foundation.exp_platform.e3.lightning.integrity_e3_classification import (
    E3BinaryClassification,
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

    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)

    spares_feature_keys = ["f1", "f2", "f3"]
    hash_size = 10000
    embedding_dim = 64
    ids_per_feature = 3

    datamodule = PReportTmpTableDataModule(
        use_onbox_loader=False,
        distributed_loader=False,
        mock_sparse=True,
        keys=spares_feature_keys,
        hash_size=hash_size,
        ids_per_feature=ids_per_feature,
    )

    eb_configs = [
        EmbeddingBagConfig(
            name=f"t_{feature_name}",
            embedding_dim=embedding_dim,
            num_embeddings=hash_size,
            feature_names=[feature_name],
        )
        for feature_name in spares_feature_keys
    ]

    e3_model = E3BinaryClassification(
        EmbeddingBagCollection(tables=eb_configs, device=torch.device("cpu"))
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
        e3_model.load_from_checkpoint(checkpoint_path=args.load_path)

    if args.manifold_bucket is not None and args.tb_manifold_path is not None:
        logger = ManifoldTensorBoardLogger(
            manifold_bucket=args.manifold_bucket,
            manifold_path=args.tb_manifold_path,
            has_user_data=False,
        )
    else:
        logger = None

    datamodule.setup()
    batch = next(iter(datamodule.train_dataloader())).to(e3_model.device)
    with torch.no_grad():
        e3_model(batch.dense_features, batch.sparse_features, batch.text_feature)

    datamodule._log_hyperparams = False
    e3_model._log_hyperparams = False

    trainer = pl.Trainer(
        logger=logger,
        max_epochs=args.epochs,
        callbacks=callbacks,
        limit_train_batches=args.limit_train_batches,
        limit_val_batches=args.limit_val_batches,
        limit_test_batches=args.limit_test_batches,
        weights_summary=None,
    )

    trainer.fit(e3_model, datamodule=datamodule)
    trainer.test(e3_model, datamodule=datamodule)


if __name__ == "__main__":
    main(sys.argv[1:])
