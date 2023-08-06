#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Any, List, Optional

from omegaconf import MISSING
from pytorch.recipes.core.conf import ModuleConf


@dataclass
class EmbeddingConf:
    channel_name: str = MISSING
    # pyre-ignore
    embedding_args: Any = MISSING


@dataclass
class EncoderConf:
    channel_name: str = MISSING
    # pyre-ignore
    encoder_args: Any = MISSING
    dict_input: bool = True


@dataclass
class FusionConf:
    fusion_name: str = MISSING
    input_encoder_names: List[str] = MISSING
    # pyre-ignore
    fusion_args: Any = MISSING


@dataclass
class MixupConf:
    alpha: float = MISSING
    scheme: str = MISSING


@dataclass
class MultimodalModuleConf(ModuleConf):
    embeddings: List[EmbeddingConf] = field(default_factory=list)
    encoders: List[EncoderConf] = field(default_factory=list)
    fusion: List[FusionConf] = field(default_factory=list)
    # pyre-ignore
    optim: Any = MISSING
    freeze_prefixes: List[str] = field(default_factory=list)
    mixup: Optional[MixupConf] = None


def register_components() -> None:
    """
    Imports all python files in the folder to trigger the
    code to register them to Hydra's ConfigStore.
    """

    import pytorch.recipes.multimodal.module.multimodal_classification  # noqa
    import pytorch.recipes.multimodal.module.multimodal_two_tower  # noqa
