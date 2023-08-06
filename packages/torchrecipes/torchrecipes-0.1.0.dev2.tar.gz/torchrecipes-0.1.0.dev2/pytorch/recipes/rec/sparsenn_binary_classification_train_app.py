from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional

from hydra.core.config_store import ConfigStore
from pytorch.recipes.core.base_train_app import BaseTrainApp
from pytorch.recipes.core.conf import ModuleConf, DataModuleConf
from pytorch.recipes.core.conf.base_config import BaseTrainAppConf
from pytorch.recipes.rec.datamodules.criteo_datamodule import CriteoDataModule
from pytorch.recipes.rec.modules.sparsenn_classification import (
    SparseNNBinaryClassification,
    SparseNNBinaryClassificationModuleConf,
)
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch_lightning import LightningDataModule, LightningModule
from stl.lightning.conf.trainer import TrainerConf
from torchrec import EmbeddingBagCollection
from torchrec.datasets.criteo import DEFAULT_CAT_NAMES
from torchrec.modules.embedding_configs import EmbeddingBagConfig


defaults: List[Dict[str, str]] = [
    {"trainer": "rec_cpu"},
]


class SparseNNBinaryClassificationTrainApp(BaseTrainApp):
    """
    Train App for torchrec classification
    """

    datamodule: CriteoDataModule

    def __init__(
        self,
        module: ModuleConf,
        trainer: TrainerConf,
        datamodule: Optional[DataModuleConf] = None,
        num_embeddings: int = 100000,
    ) -> None:
        self.num_embeddings = num_embeddings
        super().__init__(module, trainer, datamodule)

    def get_lightning_module(self) -> LightningModule:
        keys = DEFAULT_CAT_NAMES
        embedding_dim = 64

        eb_configs = [
            EmbeddingBagConfig(
                name=f"t_{feature_name}",
                embedding_dim=embedding_dim,
                num_embeddings=self.num_embeddings,
                feature_names=[feature_name],
            )
            for feature_name in keys
        ]
        return SparseNNBinaryClassification(EmbeddingBagCollection(tables=eb_configs))

    def get_data_module(self) -> LightningDataModule:
        return CriteoDataModule(
            num_days=10,
            num_days_test=3,
            num_embeddings=self.num_embeddings,
        )

    # TODO: find a better way to deal with lazy modules in lightning w/o disabling weights_summary


@dataclass
class SparseNNBinaryClassificationTrainAppConf(BaseTrainAppConf):
    _target_: str = get_class_name_str(SparseNNBinaryClassificationTrainApp)
    # pyre-ignore [4]: Attribute `defaults` of class `SparseNNBinaryClassificationTrainAppConf` is used as type `List[Dict[str, str]]` and must have a type that does not contain `Any`.
    defaults: List[Any] = field(default_factory=lambda: defaults)
    trainer: TrainerConf = TrainerConf()
    # Dummy conf. overridden in get_lightning_module()
    module: SparseNNBinaryClassificationModuleConf = (
        SparseNNBinaryClassificationModuleConf()
    )


cs: ConfigStore = ConfigStore.instance()

cs.store(
    name="rec_classification_train_app_conf",
    node=SparseNNBinaryClassificationTrainAppConf,
)
