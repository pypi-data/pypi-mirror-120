# (c) Facebook, Inc. and its affiliates. Confidential and proprietary.

from dataclasses import dataclass
from typing import Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from stl.lightning.conf.trainer import TrainerConf


@dataclass
class ModuleConf:
    pass


@dataclass
class DataModuleConf:
    pass


@dataclass
class TrainAppConf:
    module: ModuleConf = MISSING
    datamodule: Optional[DataModuleConf] = None
    trainer: TrainerConf = MISSING


# pyre-fixme[5]: Global expression must be annotated.
cs = ConfigStore.instance()
cs.store(group="schema/trainer", name="trainer", node=TrainerConf, package="trainer")
