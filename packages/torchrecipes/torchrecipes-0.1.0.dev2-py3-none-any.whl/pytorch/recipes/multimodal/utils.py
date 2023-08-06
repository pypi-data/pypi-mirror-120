#!/usr/bin/env python3
from functools import lru_cache
from typing import Dict, Tuple, List, Mapping

import hydra
import torch
from omegaconf import OmegaConf
from pytorch.recipes.multimodal.module import EmbeddingConf, EncoderConf, FusionConf
from pytorch.recipes.utils.mixup_utils import MixupScheme


class DictEncoderWrap(torch.nn.Module):
    """
    Wraps an encoder to make it input and output tensor dicts.

    The wrapped encoder has single-tensor input and return type.
    """

    def __init__(self, module: torch.nn.Module, channel_name: str) -> None:
        super().__init__()
        self.module = module
        self.channel_name = channel_name
        # pyre-fixme[4]: Missing attribute annotation [4]: Attribute `output_dim` of class
        # `DictEncoderWrap` has type `Union[torch.Tensor, torch.nn.Module]` but no type is specified.
        self.output_dim = getattr(self.module, "output_dim", None)

    def forward(self, in_batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        input = in_batch[self.channel_name]
        output = self.module(input)
        return {self.channel_name: output}


def validate_multimodal_config(
    embeddings_conf: List[EmbeddingConf],
    encoders_conf: List[EncoderConf],
    fusion_conf: List[FusionConf],
) -> None:
    """
    Validate input configurations for embeddings, encoders and fusions
    """

    # check encoder channel names are unique
    encoders_channel_names = set()
    for encoder in encoders_conf:
        if encoder.channel_name in encoders_channel_names:
            raise AssertionError(
                f"Duplicate Channel name {encoder.channel_name} in encoders list"
            )
        encoders_channel_names.add(encoder.channel_name)

    # check whether an encoder exists for each embedding
    for embedding in embeddings_conf:
        if embedding.channel_name not in encoders_channel_names:
            raise AssertionError(
                f"Embedding {embedding.channel_name} has no corresponding encoder"
            )

    # check dag of components is correctly configured
    fusion_names = set()
    for fusion in fusion_conf:
        for input_name in fusion.input_encoder_names:
            if (
                input_name not in encoders_channel_names
                and input_name not in fusion_names
            ):
                raise AssertionError(
                    f"Input name {input_name} not found in encoders list. "
                    "If you are using a fusion as input to another fusion, please make "
                    "sure the order is correct"
                )
        fusion_names.add(fusion.fusion_name)


def build_encoders(
    encoders_conf: List[EncoderConf],
    embeddings_conf: List[EmbeddingConf],
) -> Dict[str, torch.nn.Module]:
    """
    Builds encoders given conf objects for encoders and corresponding
    embeddings (if applicable).

    Returns a module dict of encoders keyed on the channel name
    """
    embeddings = {}
    if embeddings_conf:
        embeddings = {
            embedding.channel_name: hydra.utils.instantiate(embedding.embedding_args)
            for embedding in embeddings_conf
        }
    encoders = torch.nn.ModuleDict()
    for encoder in encoders_conf:
        if encoder.channel_name in embeddings:
            encoders[encoder.channel_name] = hydra.utils.instantiate(
                encoder.encoder_args, embedding=embeddings[encoder.channel_name]
            )

        else:
            encoders[encoder.channel_name] = hydra.utils.instantiate(
                encoder.encoder_args
            )

        if not encoder.dict_input:
            encoders[encoder.channel_name] = DictEncoderWrap(
                encoders[encoder.channel_name], encoder.channel_name
            )

    return encoders


def build_fusion(
    fusion_conf: List[FusionConf],
    encoders: Mapping[str, torch.nn.Module],
) -> Tuple[Dict[str, torch.nn.Module], Dict[str, List[str]]]:
    """
    Builds fusion modules given conf objects for fusion and
    module dict of encoders.

    Returns a module dict of fusion modules keyed on unique fusion name
    and a dict mapping fusion to input encoder names.
    """

    fusions = torch.nn.ModuleDict()
    fusion_inputs = {}
    for fusion in fusion_conf:
        fusion_inputs[fusion.fusion_name] = OmegaConf.to_container(
            fusion.input_encoder_names
        )
        if "encoders_dim_dict" in fusion.fusion_args:
            fusions[fusion.fusion_name] = hydra.utils.instantiate(fusion.fusion_args)
        else:
            encoders_dim_dict = {}
            for encoder_name in fusion.input_encoder_names:
                encoders_dim_dict[encoder_name] = encoders[encoder_name].output_dim
            fusions[fusion.fusion_name] = hydra.utils.instantiate(
                fusion.fusion_args, encoders_dim_dict=encoders_dim_dict
            )
    return fusions, fusion_inputs


class MultimodalClassificationMixupScheme(MixupScheme):
    INPUT = "INPUT"
    AFTERENCODING = "AFTERENCODING"
    AFTERFUSION = "AFTERFUSION"
    AFTERCLASSIFIER = "AFTERCLASSIFIER"
    RANDOM = "RANDOM"

    @classmethod
    @lru_cache
    def get_all_except_RANDOM(cls) -> List[MixupScheme]:
        return [scheme for scheme in list(cls) if scheme is not cls.RANDOM]
