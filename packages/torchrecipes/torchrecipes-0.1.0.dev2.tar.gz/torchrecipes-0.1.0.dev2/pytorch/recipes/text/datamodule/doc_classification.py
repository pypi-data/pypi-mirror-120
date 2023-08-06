#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Dict, List, Optional

import pytorch_lightning as pl
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pytext.contrib.pytext_lib.data.datasets import DeprecatedTsvDataset as TsvDataset
from pytext.contrib.pytext_lib.transforms import ModelTransform
from pytorch.recipes.core.conf import DataModuleConf
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch.recipes.utils.distributed_utils import get_rank, get_world_size
from torch.utils.data import DataLoader, Dataset


logger: logging.Logger = logging.getLogger(__name__)


_DEFAULT_COLUMN_NAMES = ["text", "label"]


class DocClassificationDataModule(pl.LightningDataModule):
    def __init__(
        self,
        transform: ModelTransform,
        # Dataset args
        train_path: str,
        val_path: str,
        test_path: str,
        columns: Optional[List[str]] = None,
        column_mapping: Optional[Dict[str, str]] = None,
        delimiter: str = "\t",
        batch_size: Optional[int] = None,
        is_shuffle: bool = True,
        chunk_size: int = 1000,
        is_cycle: bool = False,
        length: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.train_path = train_path
        self.val_path = val_path
        self.test_path = test_path
        self.transform = transform
        # pyre-fixme[4]: Attribute must be annotated.
        self.dataset_partial = partial(
            TsvDataset,
            columns=columns or _DEFAULT_COLUMN_NAMES,
            column_mapping=column_mapping,
            delimiter=delimiter,
            batch_size=batch_size,
            is_shuffle=is_shuffle,
            transform=self.transform.transform,
            collate_fn=self.transform.collate_fn,
            chunk_size=chunk_size,
            is_cycle=is_cycle,
            length=length,
        )
        self.train_dataset: Optional[Dataset] = None
        self.val_dataset: Optional[Dataset] = None
        self.test_dataset: Optional[Dataset] = None

    def train_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        dataset = self.train_dataset
        assert dataset is not None
        return DataLoader(dataset, batch_size=None)

    def val_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        dataset = self.val_dataset
        assert dataset is not None
        return DataLoader(dataset, batch_size=None)

    def test_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        dataset = self.test_dataset
        assert dataset is not None
        return DataLoader(dataset, batch_size=None)

    def setup(self, stage: Optional[str] = None) -> None:
        world_size = get_world_size()
        rank = get_rank()
        logger.debug(f"setup for rank: {rank}, world_size: {world_size}")
        if stage == "fit" or stage is None:
            self.train_dataset = self.dataset_partial(
                path=self.train_path, rank=rank, world_size=world_size
            )
            self.val_dataset = self.dataset_partial(
                path=self.val_path, rank=rank, world_size=world_size
            )

        if stage == "test" or stage is None:
            self.test_dataset = self.dataset_partial(
                path=self.test_path, rank=rank, world_size=world_size
            )


@dataclass
class DocClassificationDataModuleConf(DataModuleConf):
    _target_: str = get_class_name_str(DocClassificationDataModule)
    train_path: str = MISSING
    val_path: str = MISSING
    test_path: str = MISSING
    columns: List[str] = field(default_factory=lambda: _DEFAULT_COLUMN_NAMES)
    column_mapping: Optional[Dict[str, str]] = None
    delimiter: str = "\t"
    batch_size: Optional[int] = None
    is_shuffle: bool = True
    chunk_size: int = 1000
    is_cycle: bool = False
    length: Optional[int] = None


cs: ConfigStore = ConfigStore.instance()

cs.store(
    group="schema/datamodule",
    name="doc_classification",
    node=DocClassificationDataModuleConf,
    package="datamodule",
)
