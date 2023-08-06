import unittest
import uuid

from pytorch.recipes.rec.sparsenn_binary_classification_main import main
from torch.distributed.launcher.api import elastic_launch, LaunchConfig
from torchrec.tests import utils


class MainTest(unittest.TestCase):
    @classmethod
    def _run_trainer(cls) -> None:
        main(
            [
                "--limit_train_batches",
                "5",
                "--limit_val_batches",
                "5",
                "--limit_test_batches",
                "5",
            ]
        )

    @utils.skip_if_asan
    def test_main_function(self) -> None:
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
