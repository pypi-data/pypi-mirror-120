#!/usr/bin/env python3

# pyre-strict

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import hydra
from hydra.core.config_store import ConfigStore
from pytext.fb.utils.manifold_utils import register_manifold_handler
from pytorch.recipes.core.base_train_app import BaseTrainApp
from pytorch.recipes.core.conf import TrainAppConf
from pytorch.recipes.text.datamodule.doc_classification import (
    DocClassificationDataModuleConf,
)
from pytorch.recipes.text.module.doc_classification_demo import (
    DocClassificationModuleConf,
)
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch_lightning.core.datamodule import LightningDataModule
from stl.lightning.conf.trainer import TrainerConf


class DocClassificationTrainApp(BaseTrainApp):
    """
    This app is used to launch the doc classification training / testing.
    """

    module_conf: DocClassificationModuleConf

    def __init__(
        self,
        module: DocClassificationModuleConf,
        trainer: TrainerConf,
        datamodule: DocClassificationDataModuleConf,
    ) -> None:
        register_manifold_handler()
        super().__init__(module, trainer, datamodule)

    def get_data_module(self) -> Optional[LightningDataModule]:
        transform_cfg = self.module_conf.transform
        transform = hydra.utils.instantiate(transform_cfg)
        datamodule = hydra.utils.instantiate(self.datamodule_conf, transform=transform)
        return datamodule


defaults: List[Union[str, Dict[str, str]]] = [
    "_self_",
    # Module
    {"schema/module": "doc_classification"},
    # Module doesn't take any direct fields. No dataclass required.
    # Model
    {"module/model": "dummy_doc_model"},
    # Transform
    {"module/transform": "dummy_xlmr_transform"},
    # Optim
    {"module/optim": "adamw"},
    # Data
    {"schema/datamodule": "doc_classification"},
    {"datamodule": "dummy_sst2_manifold"},
    # Trainer
    {"trainer": "cpu_1_epoch"},
]


@dataclass
class DocClassificationTrainAppConf(TrainAppConf):
    _target_: str = get_class_name_str(DocClassificationTrainApp)
    # pyre-ignore: Missing attribute annotation [4]: Attribute `defaults`
    # of class `DocClassificationTrainAppConf` is used as type `List[Dict[str, str]]`
    # and must have a type that does not contain `Any`.
    defaults: List[Any] = field(default_factory=lambda: defaults)


cs: ConfigStore = ConfigStore.instance()

cs.store(name="doc_classification_app", node=DocClassificationTrainAppConf)
