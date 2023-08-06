# (c) Facebook, Inc. and its affiliates. Confidential and proprietary.

from dataclasses import dataclass, field
from typing import List, Any

# @manual "//github/facebookresearch/hydra:hydra"
from hydra.core.config_store import ConfigStore
from pytorch.recipes.core.base_train_app import BaseTrainApp
from pytorch.recipes.core.conf.base_config import BaseTrainAppConf
from pytorch.recipes.multimodal.datamodule.test_multimodal_datamodule import (
    TestMultimodalDataModuleConf,
)
from pytorch.recipes.multimodal.module.multimodal_classification import (
    MultimodalClassificationModuleConf,
    convert_hydra_conf_to_module as convert_hydra_conf_to_module_classification,
    MultimodalClassification,
)
from pytorch.recipes.multimodal.module.multimodal_two_tower import (
    MultimodalTwoTowerModuleConf,
    convert_hydra_conf_to_module as convert_hydra_conf_to_module_two_tower,
    MultimodalTwoTower,
)
from pytorch.recipes.utils.config_utils import get_class_name_str
from stl.lightning.conf.trainer import TrainerConf


multimodal_classification_defaults = [
    # Module
    "_self_",
    {"schema/module": "multimodal_classification"},
    # Module doesn't take any direct fields. No dataclass required.
    {"module/embeddings": "test_embedding"},
    {"module/encoders": "test_encoders"},
    {"module/fusion": "test_fusion"},
    {"module/classifier": "test_classifier"},
    {"module/optim": "adam"},
    # Data
    {"schema/datamodule": "test_multimodal_datamodule"},
    # Trainer
    {"trainer": "cpu"},
]

multimodal_two_tower_defaults = [
    # Module
    "_self_",
    {"schema/module": "multimodal_two_tower"},
    # Module doesn't take any direct fields. No dataclass required.
    {"module/embeddings": "test_embedding"},
    {"module/encoders": "test_encoders"},
    {"module/fusion": "test_fusion"},
    {"module/towers": "test_towers"},
    {"module/optim": "adam"},
    # Data
    {"schema/datamodule": "test_multimodal_datamodule"},
    # Trainer
    {"trainer": "cpu"},
]


class MultimodalClassificationTrainApp(BaseTrainApp):
    def __init__(
        self,
        module: MultimodalClassificationModuleConf,
        trainer: TrainerConf,
        datamodule: TestMultimodalDataModuleConf,
    ) -> None:
        super().__init__(module, trainer, datamodule)

    def get_lightning_module(self) -> MultimodalClassification:
        # pyre-ignore
        module = convert_hydra_conf_to_module_classification(self.module_conf)
        return module


@dataclass
class MultimodalClassificationTrainAppConf(BaseTrainAppConf):
    _target_: str = get_class_name_str(MultimodalClassificationTrainApp)
    # pyre-fixme[4]: Attribute annotation cannot contain `Any`.
    defaults: List[Any] = field(
        default_factory=lambda: multimodal_classification_defaults
    )
    module: MultimodalClassificationModuleConf = MultimodalClassificationModuleConf()


class MultimodalTwoTowerTrainApp(BaseTrainApp):
    def __init__(
        self,
        module: MultimodalTwoTowerModuleConf,
        trainer: TrainerConf,
        datamodule: TestMultimodalDataModuleConf,
    ) -> None:
        super().__init__(module, trainer, datamodule)

    def get_lightning_module(self) -> MultimodalTwoTower:
        # pyre-ignore
        module = convert_hydra_conf_to_module_two_tower(self.module_conf)
        return module


@dataclass
class MultimodalTwoTowerTrainAppConf(BaseTrainAppConf):
    _target_: str = get_class_name_str(MultimodalTwoTowerTrainApp)
    # pyre-fixme[4]: Attribute annotation cannot contain `Any`.
    defaults: List[Any] = field(default_factory=lambda: multimodal_two_tower_defaults)
    module: MultimodalTwoTowerModuleConf = MultimodalTwoTowerModuleConf()


cs: ConfigStore = ConfigStore.instance()

cs.store(
    name="multimodal_classification_app", node=MultimodalClassificationTrainAppConf
)
cs.store(name="multimodal_two_tower_app", node=MultimodalTwoTowerTrainAppConf)
