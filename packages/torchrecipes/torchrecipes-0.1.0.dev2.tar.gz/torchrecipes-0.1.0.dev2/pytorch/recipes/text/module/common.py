#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# pyre-ignore-all-errors

from typing import Any, Dict

import torch
from apex import amp
from pytorch_lightning.utilities import AMPType, DeviceType


class CheckpointMixin(object):
    """Mixin to enable resuming from checkpoint
    Currently, resuming from checkpointing requires a hack in `on_pretrain_routine_end`.
    TODO: T98699770 @stevenliu remove this class after the official fix landed in Lightning
    Usage:
        MyTask(CheckpointMixin, LightningModule):
            ...

    Note: CheckpointMixin must be added ahead of LightningModule. For FSDP, it's
    required to add attribute `enable_configure_sharded_model` to Task and set it to True
    """

    def on_pretrain_routine_end(self) -> None:
        if self.trainer is None:
            return

        if self.trainer.resume_from_checkpoint is None:
            return

        # Before reconnecting, as we already restored optimizer states, lr scheduler, amp states
        #  we store it temporarily and after reconnecting, we will load it.
        restored_checkpoint = self._get_restored_trainer_states()

        # Reconnecting model, configure, and pre dispatch.
        self.trainer.accelerator.connect(self)
        self.trainer.accelerator.setup_environment()
        if getattr(self, "enable_configure_sharded_model", False):
            self.trainer._call_configure_sharded_model(self)
        self.trainer.optimizers = []
        self.trainer.accelerator.setup(self.trainer, self)
        self.trainer.accelerator.pre_dispatch(self.trainer)

        # Restore the optimizers, lr scheduler, amp states for re-connected and configured model
        self._restore_trainer_states(restored_checkpoint)

    def _get_restored_trainer_states(self) -> Dict[str, Any]:
        restored_checkpoint = {}
        optimizer_states = []
        for _, optimizer in enumerate(self.trainer.optimizers):
            # Rely on accelerator to dump optimizer state
            optimizer_state = self.trainer.accelerator.optimizer_state(optimizer)
            optimizer_states.append(optimizer_state)
        restored_checkpoint["optimizer_states"] = optimizer_states
        # dump lr schedulers
        lr_schedulers = []
        for scheduler in self.trainer.lr_schedulers:
            lr_schedulers.append(scheduler["scheduler"].state_dict())
        restored_checkpoint["lr_schedulers"] = lr_schedulers
        # dump amp scaling
        if (
            self.trainer.amp_backend == AMPType.NATIVE
            and self.trainer._device_type != DeviceType.TPU
            and self.trainer.scaler is not None
        ):
            restored_checkpoint[
                "native_amp_scaling_state"
            ] = self.trainer.scaler.state_dict()
        elif self.trainer.amp_backend == AMPType.APEX:
            restored_checkpoint["amp_scaling_state"] = amp.state_dict()
        return restored_checkpoint

    def _restore_trainer_states(self, checkpoint: Dict[str, Any]) -> None:
        # restore the optimizers
        optimizer_states = checkpoint["optimizer_states"]
        for optimizer, opt_state in zip(self.trainer.optimizers, optimizer_states):
            optimizer.load_state_dict(opt_state)

            # move optimizer to GPU 1 weight at a time
            # avoids OOM
            if self.trainer.root_gpu is not None:
                for state in optimizer.state.values():
                    for k, v in state.items():
                        if isinstance(v, torch.Tensor):
                            state[k] = v.cuda(self.trainer.root_gpu)
        # restore the lr schedulers
        lr_schedulers = checkpoint["lr_schedulers"]
        for scheduler, lrs_state in zip(self.trainer.lr_schedulers, lr_schedulers):
            scheduler["scheduler"].load_state_dict(lrs_state)
        # restore amp scaling
        if (
            self.trainer.amp_backend == AMPType.NATIVE
            and "native_amp_scaling_state" in checkpoint
        ):
            self.trainer.scaler.load_state_dict(checkpoint["native_amp_scaling_state"])
        elif (
            self.trainer.amp_backend == AMPType.APEX
            and "amp_scaling_state" in checkpoint
        ):
            amp.load_state_dict(checkpoint["amp_scaling_state"])
