#!/usr/bin/env python3

import testslide
from pytorch.recipes.rec.datamodules.criteo_datamodule import CriteoDataModule


class TestCriteoDataModule(testslide.TestCase):
    def test_none_stage(self) -> None:
        dm = CriteoDataModule(num_days=1, batch_size=3, num_days_test=1, num_workers=0)
        dm.setup()

        train_batch = next(iter(dm.train_dataloader()))
        self.assertEqual(train_batch.dense_features.size(), (3, 13))
        kjt = train_batch.sparse_features
        self.assertEqual(kjt.lengths().size(), (26 * 3,))
        self.assertEqual(kjt.keys(), dm.keys)

        test_batch = next(iter(dm.test_dataloader()))
        self.assertEqual(test_batch.dense_features.size(), (3, 13))
        kjt = test_batch.sparse_features
        self.assertEqual(kjt.lengths().size(), (26 * 3,))
        self.assertEqual(kjt.keys(), dm.keys)

    def test_fit_stage(self) -> None:
        dm = CriteoDataModule(num_days=1, batch_size=3, num_days_test=1, num_workers=0)
        dm.setup(stage="fit")

        train_batch = next(iter(dm.train_dataloader()))
        self.assertEqual(train_batch.dense_features.size(), (3, 13))
        kjt = train_batch.sparse_features
        self.assertEqual(kjt.lengths().size(), (26 * 3,))
        self.assertEqual(kjt.keys(), dm.keys)

        with self.assertRaises(AssertionError):
            # only train/val dataloaders are set up
            dm.test_dataloader()

    def test_test_stage(self) -> None:
        dm = CriteoDataModule(num_days=1, batch_size=3, num_days_test=1, num_workers=0)
        dm.setup(stage="test")

        with self.assertRaises(AssertionError):
            # only test dataloader is set up
            dm.train_dataloader()

        test_batch = next(iter(dm.test_dataloader()))
        self.assertEqual(test_batch.dense_features.size(), (3, 13))
        kjt = test_batch.sparse_features
        self.assertEqual(kjt.lengths().size(), (26 * 3,))
        self.assertEqual(kjt.keys(), dm.keys)
