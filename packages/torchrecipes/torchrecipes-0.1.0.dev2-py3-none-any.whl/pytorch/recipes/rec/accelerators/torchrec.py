import logging
from typing import Optional, Any, Union

import pytorch_lightning as pl
import torch
import torch.distributed as dist
from caffe2.torch.fb.distributed.utils.log_utils import getLogger
from pytorch_lightning.accelerators.accelerator import Accelerator
from pytorch_lightning.plugins import PrecisionPlugin
from pytorch_lightning.plugins.training_type.parallel import (
    ParallelPlugin,
)

logger: logging.Logger = getLogger()


class TorchrecTrainingTypePlugin(ParallelPlugin):
    """
    Lightning Trainer takes care of the operations that are related to DDP.
    However, our models are parallelization aware, which are not fully compatible to the
    given accelerators and plugins provided by Lightning.

    The torchrec plugin and acclerator bypasses the corresponding logic in Lightning.
    """

    def __init__(self) -> None:
        super().__init__()
        logger.info("Creating torchrec training type plugin")

    def broadcast(self, obj: object, src: int = 0) -> object:
        if dist.is_initialized:
            if isinstance(obj, torch.Tensor):
                dist.broadcast(obj, src)
                return obj
            else:
                object_list = [obj]
                dist.broadcast_object_list(object_list=object_list, src=src)
                return object_list[0]
        else:
            raise AssertionError(
                "Broadcast called in torchrec training type plugin w/o initializing distributed"
            )

    @property
    def root_device(self) -> torch.device:
        raise NotImplementedError()

    @property
    def should_rank_save_checkpoint(self) -> bool:
        return False

    def barrier(self, name: Optional[str] = None) -> None:
        if dist.is_initialized:
            dist.barrier()
        else:
            raise AssertionError(
                "All gather called in torchrec training type plugin w/o initializing distributed"
            )

    def all_gather(
        self,
        tensor: torch.Tensor,
        # pyre-ignore[2]: Parameter `group` has type `None` but type `Any` is specified.
        group: Optional[Any] = None,
        sync_grads: bool = False,
    ) -> torch.Tensor:
        if dist.is_initialized:
            dist.all_gather(tensor, group, sync_grads)
            return tensor
        else:
            raise AssertionError(
                "All gather called in torchrec training type plugin w/o initializing distributed"
            )

    # pyre-ignore[3]: Return type must be specified as type other than `Any`.
    def reduce(
        self,
        # pyre-ignore[2]: Parameter `tensor` must have a type other than `Any`.
        tensor: Union[Any, torch.Tensor],
        *args: Any,
        **kwargs: Any,
    ) -> Union[Any, torch.Tensor]:
        if dist.is_initialized:
            dist.all_reduce(tensor)
            return tensor
        else:
            raise AssertionError(
                "Reduce called in torchrec training type plugin w/o initializing distributed"
            )

    def model_to_device(self) -> None:
        raise NotImplementedError()

    def teardown(self) -> None:
        return None


class TorchrecAccelerator(Accelerator):
    def __init__(self) -> None:
        training_type_plugin = TorchrecTrainingTypePlugin()
        precision_plugin = PrecisionPlugin()
        super().__init__(
            precision_plugin=precision_plugin,
            training_type_plugin=training_type_plugin,
        )
        logger.info("Creating torchrec accelerator")

    def pre_dispatch(self, trainer: pl.Trainer) -> None:
        logger.info("Not doing anything in pre_dispatch of TorchrecAccelerator")
        return None

    # pyre-ignore[3]
    def batch_to_device(
        self,
        # pyre-ignore[2]
        batch: Any,
        device: Optional[torch.device] = None,
        dataloader_idx: Optional[int] = None,
    ) -> Any:
        return batch.to(self.lightning_module.device)
