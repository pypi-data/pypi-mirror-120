#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

import hydra
import pytorch_lightning as pl
import torch
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, OmegaConf
from pytorch.recipes.multimodal.module import MultimodalModuleConf
from pytorch.recipes.multimodal.utils import (
    build_encoders,
    build_fusion,
)
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch_lightning.utilities import rank_zero_info


@dataclass
class TowerConf:
    input_fusion_name: List[str] = MISSING
    task_name: str = "single_task"
    # pyre-ignore
    output_fusion: Any = MISSING
    # pyre-ignore
    loss: Any = MISSING


class MultimodalTwoTowerModel(torch.nn.Module):
    def __init__(
        self,
        encoders: Mapping[str, torch.nn.Module],
        fusions: Mapping[str, torch.nn.Module],
        fusion_inputs: Mapping[str, List[str]],
        towers: Mapping[str, torch.nn.Module],
        tower_input_fusion: Mapping[str, List[str]],
    ) -> None:
        super().__init__()
        self.encoders = encoders
        self.fusions = fusions
        self.fusion_inputs = fusion_inputs
        self.towers = towers
        self.tower_input_fusion = tower_input_fusion

    def forward(self, input: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        output = {}
        for encoder in self.encoders.values():
            encoder_output = encoder(input)
            output.update(encoder_output)
        for fusion_name, fusion in self.fusions.items():
            fusion_input = {key: output[key] for key in self.fusion_inputs[fusion_name]}
            output.update(fusion(fusion_input))

        model_out = {}
        for task_name, tower in self.towers.items():
            tower_input = [
                output[fusion_name]
                for fusion_name in self.tower_input_fusion[task_name]
            ]
            model_out[task_name] = tower(tower_input)

        return model_out


class MultimodalTwoTower(pl.LightningModule):
    def __init__(
        self,
        encoders: Mapping[str, torch.nn.Module],
        fusions: Mapping[str, torch.nn.Module],
        fusion_inputs: Mapping[str, List[str]],
        towers: Mapping[str, torch.nn.Module],
        tower_input_fusion: Mapping[str, List[str]],
        losses: Mapping[str, torch.nn.Module],
        optimizer: torch.optim.Optimizer,
        freeze_prefixes: Optional[List[str]] = None,
    ) -> None:

        super().__init__()
        self.model = MultimodalTwoTowerModel(
            encoders=encoders,
            fusions=fusions,
            fusion_inputs=fusion_inputs,
            towers=towers,
            tower_input_fusion=tower_input_fusion,
        )
        self.losses = losses
        self.optimizer = optimizer
        self.freeze_prefixes: List[str] = freeze_prefixes or []
        # pyre-fixme[4]: Attribute must be annotated.
        self.example_input_array = None

    def get_tasks_model(self, task_list: List[str]) -> MultimodalTwoTowerModel:
        """
        Return MultimodalClassificationModel for specfied tasks
        """
        encoders = torch.nn.ModuleDict()
        fusions = torch.nn.ModuleDict()
        fusion_inputs = {}
        towers = torch.nn.ModuleDict()
        tower_input_fusion = {}

        fusion_names = set()
        encoder_names = set()
        for task in task_list:
            towers[task] = self.model.towers[task]
            tower_input_fusion[task] = self.model.tower_input_fusion[task]
            fusion_names.update(tower_input_fusion[task])

        for fusion_name in fusion_names:
            fusions[fusion_name] = self.model.fusions[fusion_name]
            fusion_inputs[fusion_name] = self.model.fusion_inputs[fusion_name]
            encoder_names.update(fusion_inputs[fusion_name])

        for encoder_name in encoder_names:
            encoders[encoder_name] = self.model.encoders[encoder_name]

        return MultimodalTwoTowerModel(
            encoders=encoders,
            fusions=fusions,
            fusion_inputs=fusion_inputs,
            towers=towers,
            tower_input_fusion=tower_input_fusion,
        )

    def setup(self, stage: Optional[str] = None) -> None:
        if stage != "fit" or not self.freeze_prefixes:
            return
        frozen_params = []
        for name, param in self.named_parameters():
            should_be_frozen = any(
                name.startswith(prefix) for prefix in self.freeze_prefixes
            )
            if should_be_frozen:
                frozen_params.append(name)
                param.requires_grad = False

        rank_zero_info(f"Frozen params: {frozen_params}")

    # Do not remove.  Needed to maintain torchscriptability, see https://fburl.com/wiki/b5f028m0
    # pyre-ignore[14] - `forward` overrides method defined in `pl.core.lightning.LightningModule`
    # inconsistently. Could not find parameter `Variable(unknown)` [`Keywords(unknown)`] in overriding signature.
    def forward(self, input: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        return self.model(input)

    def compute_loss(
        self, model_out: Dict[str, torch.Tensor], target: Dict[str, torch.Tensor]
    ) -> torch.Tensor:
        loss = []
        for task_name in model_out:
            loss.append(self.losses[task_name](model_out[task_name], target[task_name]))

        return sum(loss) / len(loss)

    def _step(
        self,
        batch: Dict[str, torch.Tensor],
        batch_idx: int,
        phase_type: str,
    ) -> Dict[str, torch.Tensor]:
        model_out = self.forward(batch)
        loss = self.compute_loss(model_out, batch)
        self.log(f"{phase_type}_loss", loss, on_epoch=True)
        return {"loss": loss}

    def training_step(
        self,
        batch: Dict[str, torch.Tensor],
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, torch.Tensor]:
        return self._step(batch, batch_idx, "train")

    def validation_step(
        self,
        batch: Dict[str, torch.Tensor],
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, torch.Tensor]:
        return self._step(batch, batch_idx, "val")

    def test_step(
        self,
        batch: Dict[str, torch.Tensor],
        batch_idx: int,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, torch.Tensor]:
        return self._step(batch, batch_idx, "test")

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return self.optimizer


@dataclass
class MultimodalTwoTowerModuleConf(MultimodalModuleConf):
    _target_: str = get_class_name_str(MultimodalTwoTower)
    towers: List[TowerConf] = field(default_factory=list)


cs: ConfigStore = ConfigStore.instance()


cs.store(
    group="schema/module",
    name="multimodal_two_tower",
    node=MultimodalTwoTowerModuleConf,
    package="module",
)


def convert_hydra_conf_to_module(
    module_conf: MultimodalTwoTowerModuleConf,
) -> MultimodalTwoTower:
    # build embeddings and encoders if provided
    # both embeddings and encoders have channel_name to identify correspondence.
    encoders = build_encoders(
        encoders_conf=module_conf.encoders, embeddings_conf=module_conf.embeddings
    )

    # build fusion modules
    fusions, fusion_inputs = build_fusion(
        fusion_conf=module_conf.fusion, encoders=encoders
    )

    # build towers
    tower_input_fusion = {}
    towers = torch.nn.ModuleDict()
    losses = torch.nn.ModuleDict()
    for tower in module_conf.towers:
        towers[tower.task_name] = hydra.utils.instantiate(tower.output_fusion)

        tower_input_fusion[tower.task_name] = OmegaConf.to_container(
            tower.input_fusion_name
        )

        losses[tower.task_name] = hydra.utils.instantiate(tower.loss)

    parameters = (
        # pyre-ignore
        list(encoders.parameters())
        + list(fusions.parameters())
        + list(towers.parameters())
    )
    optimizer = hydra.utils.instantiate(module_conf.optim, parameters)

    return MultimodalTwoTower(
        encoders=encoders,
        fusions=fusions,
        fusion_inputs=fusion_inputs,
        towers=towers,
        tower_input_fusion=tower_input_fusion,
        losses=losses,
        optimizer=optimizer,
        freeze_prefixes=module_conf.freeze_prefixes,
    )
