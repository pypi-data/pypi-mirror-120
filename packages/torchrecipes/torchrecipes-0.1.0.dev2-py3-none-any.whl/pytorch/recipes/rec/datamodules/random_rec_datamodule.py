from dataclasses import dataclass
from typing import Optional, List, Iterator

import pytorch_lightning as pl
import torch

# @manual "//github/facebookresearch/hydra:hydra"
from hydra.core.config_store import ConfigStore
from pytorch.recipes.core.conf import DataModuleConf
from pytorch.recipes.rec.datamodules.commons import Batch
from pytorch.recipes.utils.config_utils import get_class_name_str
from torch.utils.data import DataLoader
from torch.utils.data.dataset import IterableDataset
from torchrec import KeyedJaggedTensor


class _RandomRecBatch:
    generator: Optional[torch.Generator]

    def __init__(
        self,
        keys: List[str],
        batch_size: int,
        hash_size: int,
        ids_per_feature: int,
        num_dense: int,
        manual_seed: Optional[int] = None,
    ) -> None:
        self.keys = keys
        self.keys_length: int = len(keys)
        self.batch_size = batch_size
        self.hash_size = hash_size
        self.ids_per_feature = ids_per_feature
        self.num_dense = num_dense

        if manual_seed is not None:
            self.generator = torch.Generator()
            # pyre-ignore[16]
            self.generator.manual_seed(manual_seed)
        else:
            self.generator = None

        self.iter_num = 0

    def __iter__(self) -> "_RandomRecBatch":
        return self

    def __next__(self) -> Batch:
        num_ids_in_batch = self.ids_per_feature * self.keys_length * self.batch_size

        sparse_features = KeyedJaggedTensor.from_offsets_sync(
            keys=self.keys,
            # pyre-ignore[28]
            values=torch.randint(
                high=self.hash_size,
                size=(num_ids_in_batch,),
                generator=self.generator,
            ),
            offsets=torch.tensor(
                list(
                    range(
                        0,
                        num_ids_in_batch + 1,
                        self.ids_per_feature,
                    )
                ),
                dtype=torch.int32,
            ),
        )

        dense_features = torch.randn(
            self.batch_size,
            self.num_dense,
            generator=self.generator,
        )
        # pyre-ignore[28]
        labels = torch.randint(
            low=0,
            high=1,
            size=(self.batch_size,),
            generator=self.generator,
        )

        batch = Batch(
            dense_features=dense_features,
            sparse_features=sparse_features,
            labels=labels,
        )
        return batch


class _RandomRecDataset(IterableDataset[Batch]):
    def __init__(
        self,
        keys: List[str],
        batch_size: int,
        hash_size: int = 100,
        ids_per_feature: int = 2,
        num_dense: int = 50,
        manual_seed: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.batch_generator = _RandomRecBatch(
            keys=keys,
            batch_size=batch_size,
            hash_size=hash_size,
            ids_per_feature=ids_per_feature,
            num_dense=num_dense,
            manual_seed=manual_seed,
        )

    def __iter__(self) -> Iterator[Batch]:
        return iter(self.batch_generator)


class RandomRecDataModule(pl.LightningDataModule):
    """
    DataModule that wraps _RandomRecDataset. This dataset generates _RandomRecBatch, or random
    batches of sparse_features in the form of KeyedJaggedTensor, dense_features and labels

    {
        "dense_features": torch.Tensor,
        "sparse_features": KeyedJaggedTensor,
        "labels": torch.Tensor,
    }
    """

    def __init__(self, manual_seed: Optional[int] = None) -> None:
        super().__init__()
        self.keys: List[str] = ["f1", "f3", "f2"]
        self.batch_size = 3
        self.manual_seed = manual_seed
        self.init_loader: DataLoader = DataLoader(
            _RandomRecDataset(
                keys=self.keys,
                batch_size=self.batch_size,
                manual_seed=self.manual_seed,
            ),
            batch_size=None,
            batch_sampler=None,
        )

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            _RandomRecDataset(
                keys=self.keys,
                batch_size=self.batch_size,
                manual_seed=self.manual_seed,
            ),
            batch_size=None,
            batch_sampler=None,
        )

    def val_dataloader(self) -> DataLoader:
        return DataLoader(
            _RandomRecDataset(
                keys=self.keys,
                batch_size=self.batch_size,
                manual_seed=self.manual_seed,
            ),
            batch_size=None,
            batch_sampler=None,
        )

    def test_dataloader(self) -> DataLoader:
        return DataLoader(
            _RandomRecDataset(
                keys=self.keys,
                batch_size=self.batch_size,
                manual_seed=self.manual_seed,
            ),
            batch_size=None,
            batch_sampler=None,
        )


@dataclass
class RandomRecDataModuleConf(DataModuleConf):
    _target_: str = get_class_name_str(RandomRecDataModule)


cs: ConfigStore = ConfigStore.instance()

cs.store(
    group="schema/datamodule",
    name="random_rec_datamodule",
    node=RandomRecDataModuleConf,
    package="datamodule",
)
