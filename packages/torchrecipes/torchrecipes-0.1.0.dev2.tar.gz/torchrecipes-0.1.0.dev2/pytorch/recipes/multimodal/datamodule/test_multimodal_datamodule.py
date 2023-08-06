#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass
from typing import Dict

import torch
from hydra.core.config_store import ConfigStore
from pytorch.recipes.core.conf import DataModuleConf
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch_lightning import LightningDataModule
from torch.utils.data.dataset import Dataset


class MultimodalDataset(Dataset[Dict[str, torch.Tensor]]):
    def __init__(self, only_floats: bool = False) -> None:
        self.len = 1024
        if only_floats:
            self.modality_1_dataset: torch.Tensor = torch.randn(self.len, 128)
        else:
            self.modality_1_dataset: torch.Tensor = torch.randint(
                0, 10, size=(self.len, 128)
            )
        self.modality_2_dataset: torch.Tensor = torch.randn(self.len, 256)
        self.labels: torch.Tensor = torch.randint(0, 2, size=(self.len,))

    def __getitem__(self, index: int) -> Dict[str, torch.Tensor]:
        return {
            "modality_1": self.modality_1_dataset[index],
            "modality_2": self.modality_2_dataset[index],
            "single_task": self.labels[index],
        }

    def __len__(self) -> int:
        return self.len


class TestMultimodalDataModule(LightningDataModule):

    only_floats: bool

    def __init__(self, only_floats: bool = False) -> None:
        super().__init__()
        self.only_floats = only_floats

    def train_dataloader(self) -> torch.utils.data.DataLoader:
        return torch.utils.data.DataLoader(
            MultimodalDataset(only_floats=self.only_floats), batch_size=128
        )

    def val_dataloader(self) -> torch.utils.data.DataLoader:
        return torch.utils.data.DataLoader(
            MultimodalDataset(only_floats=self.only_floats), batch_size=128
        )

    def test_dataloader(self) -> torch.utils.data.DataLoader:
        return torch.utils.data.DataLoader(
            MultimodalDataset(only_floats=self.only_floats), batch_size=128
        )


@dataclass
class TestMultimodalDataModuleConf(DataModuleConf):
    _target_: str = get_class_name_str(TestMultimodalDataModule)
    only_floats: bool = False


cs: ConfigStore = ConfigStore.instance()

cs.store(
    group="schema/datamodule",
    name="test_multimodal_datamodule",
    node=TestMultimodalDataModuleConf,
    package="datamodule",
)
