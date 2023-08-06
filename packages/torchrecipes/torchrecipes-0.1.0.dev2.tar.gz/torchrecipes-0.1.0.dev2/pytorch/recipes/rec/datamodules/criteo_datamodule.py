#!/usr/bin/env python3

from typing import (
    Any,
    Iterable,
    List,
    Mapping,
    Optional,
    Union,
    cast,
)

import pytorch_lightning as pl
import torch
from pytorch.recipes.rec.datamodules.commons import Batch
from pytorch.recipes.rec.datamodules.samplers.undersampler import ProportionUnderSampler
from torch.utils.data import DataLoader, IterDataPipe
from torchrec.datasets.criteo import (
    DEFAULT_CAT_NAMES,
    DEFAULT_INT_NAMES,
    DEFAULT_LABEL_NAME,
)
from torchrec.datasets.criteo import criteo_terabyte
from torchrec.datasets.utils import rand_split_train_val
from torchrec.fb.datasets.utils import enable_manifold_read
from torchrec.sparse.jagged_tensor import KeyedJaggedTensor


def _transform(
    batch: Mapping[str, Union[Iterable[str], torch.Tensor]],
    num_embeddings: int = 100000,
) -> Batch:
    cat_list: List[torch.Tensor] = []
    for col_name in DEFAULT_INT_NAMES:
        val = cast(torch.Tensor, batch[col_name])
        # mininum value in criteo dataset of int features is -1 so we add 2 before taking log
        cat_list.append((torch.log(val + 2)).unsqueeze(0).T)
    dense_features = torch.cat(
        cat_list,
        dim=1,
    )

    kjt_values: List[int] = []
    kjt_lengths: List[int] = []
    for col_name in DEFAULT_CAT_NAMES:
        values = cast(Iterable[str], batch[col_name])
        for value in values:
            if value:
                kjt_values.append(int(value, 16) % num_embeddings)
                kjt_lengths.append(1)
            else:
                kjt_lengths.append(0)

    sparse_features = KeyedJaggedTensor.from_lengths_sync(
        DEFAULT_CAT_NAMES,
        torch.tensor(kjt_values),
        torch.tensor(kjt_lengths, dtype=torch.int32),
    )
    labels = batch[DEFAULT_LABEL_NAME]
    assert isinstance(labels, torch.Tensor)

    return Batch(
        dense_features=dense_features,
        sparse_features=sparse_features,
        labels=labels,
    )


# Setup function to enable manifold reading for each DataLoader worker process.
def _enable_manifold_read(_worker_id: int) -> None:
    enable_manifold_read()


class CriteoDataModule(pl.LightningDataModule):
    """`DataModule for Criteo 1TB Click Logs <https://ailab.criteo.com/download-criteo-1tb-click-logs-dataset/>`_ Dataset
    Args:
        num_days: number of days (out of 25) of data to use for train/validation
        num_days_test: number of days (out of 25) of data to use for testing
        num_embeddings: the number of embeddings (hash size) of the categorical (sparse) features
        batch_size: int
        num_workers: int
        train_percent: percent of data to use for training vs validation- 0.0 - 1.0
        read_chunk_size: int
        dataset_path: Path to the criteo dataset. Defaults to torchrec maintained manifold path
        undersampling_rate: 0.0 - 1.0. Desired proportion of zero-labeled samples to
            retain (i.e. undersampling zero-labeled rows). Ex. 0.3 indicates only 30%
            of the rows with label 0 will be kept. All rows with label 1 will be kept.
            Default: None, indicating no undersampling.
        seed: Random seed for reproducibility. Default: None.

    Examples:
        >>> dm = CriteoDataModule(num_days=1, batch_size=3, num_days_test=1)
        >>> dm.setup()
        >>> train_batch = next(iter(dm.train_dataloader()))
    """

    def __init__(
        self,
        num_days: int = 1,
        num_days_test: int = 0,
        num_embeddings: int = 100000,
        batch_size: int = 32,
        train_percent: float = 0.8,
        num_workers: int = 0,
        read_chunk_size: int = 100000,
        dataset_path: str = "manifold://torchrec/tree/datasets/criteo",
        undersampling_rate: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__()
        if not (1 <= num_days <= 24):
            raise ValueError(
                f"Dataset has only 24 days of data. User asked for {num_days} days"
            )
        if not (0 <= num_days_test <= 24):
            raise ValueError(
                f"Dataset has only 24 days of data. User asked for {num_days_test} days"
            )
        if not (num_days + num_days_test <= 24):
            raise ValueError(
                f"Dataset has only 24 days of data. User asked for {num_days} train days and {num_days_test} test days"
            )
        if not (0.0 <= train_percent <= 1.0):
            raise ValueError(f"train_percent {train_percent} must be between 0 and 1")

        # TODO handle more workers for IterableDataset

        self.batch_size = batch_size
        self._num_workers = num_workers
        self._read_chunk_size = read_chunk_size
        self._num_days = num_days
        self._num_days_test = num_days_test
        self.num_embeddings = num_embeddings
        self._train_percent = train_percent
        self._dataset_path = dataset_path
        self._undersampling_rate = undersampling_rate
        self._seed = seed

        self._train_datapipe: Optional[IterDataPipe] = None
        self._val_datapipe: Optional[IterDataPipe] = None
        self._test_datapipe: Optional[IterDataPipe] = None
        self.keys: List[str] = DEFAULT_CAT_NAMES

    def _create_datapipe(self, day_range: Iterable[int]) -> IterDataPipe:
        paths = [f"{self._dataset_path}/day_{day}.tsv" for day in day_range]
        datapipe = criteo_terabyte(
            paths,
            # this is important because without it, the reader will attempt to synchronously download the whole file...
            read_chunk_size=self._read_chunk_size,
        )

        undersampling_rate = self._undersampling_rate
        if undersampling_rate is not None:
            datapipe = ProportionUnderSampler(
                datapipe,
                CriteoDataModule._get_label,
                {0: undersampling_rate, 1: 1.0},
                seed=self._seed,
            )

        return datapipe

    @staticmethod
    # pyre-ignore[2, 3]
    def _get_label(row: Any) -> Any:
        return row["label"]

    def _batch_collate_transform(self, datapipe: IterDataPipe) -> IterDataPipe:
        return (
            datapipe.batch(self.batch_size)
            .collate()
            .map(_transform, fn_kwargs={"num_embeddings": self.num_embeddings})
        )

    def setup(self, stage: Optional[str] = None) -> None:
        # TODO: move enable_manifold_read() call in fb only when move to OSS (potentially subclass)
        enable_manifold_read()
        if stage == "fit" or stage is None:
            datapipe = self._create_datapipe(range(self._num_days))
            train_datapipe, val_datapipe = rand_split_train_val(
                datapipe, self._train_percent
            )
            self._train_datapipe = self._batch_collate_transform(train_datapipe)
            self._val_datapipe = self._batch_collate_transform(val_datapipe)

        if stage == "test" or stage is None:
            datapipe = self._create_datapipe(
                range(self._num_days, self._num_days + self._num_days_test)
            )
            self._test_datapipe = self._batch_collate_transform(datapipe)

    def _create_dataloader(self, datapipe: IterDataPipe) -> DataLoader:
        return DataLoader(
            datapipe,
            num_workers=self._num_workers,
            batch_size=None,
            batch_sampler=None,
            # TODO: move enable_manifold_read() call in fb only when move to OSS (potentially subclass)
            worker_init_fn=_enable_manifold_read,
        )

    def train_dataloader(self) -> DataLoader:
        datapipe = self._train_datapipe
        assert isinstance(datapipe, IterDataPipe)
        return self._create_dataloader(datapipe)

    def val_dataloader(self) -> DataLoader:
        datapipe = self._val_datapipe
        assert isinstance(datapipe, IterDataPipe)
        return self._create_dataloader(datapipe)

    def test_dataloader(self) -> DataLoader:
        datapipe = self._test_datapipe
        assert isinstance(datapipe, IterDataPipe)
        return self._create_dataloader(datapipe)
