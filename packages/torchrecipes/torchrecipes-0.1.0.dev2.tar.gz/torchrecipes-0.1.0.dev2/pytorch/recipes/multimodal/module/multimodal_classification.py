#!/usr/bin/env python3

import random
from dataclasses import dataclass, field
from typing import Union, Any, Dict, List, Mapping, Optional, Tuple

import hydra
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, OmegaConf
from pytorch.recipes.multimodal.module import (
    MultimodalModuleConf,
    EmbeddingConf,
    EncoderConf,
    FusionConf,
)
from pytorch.recipes.multimodal.utils import (
    build_encoders,
    build_fusion,
    validate_multimodal_config,
    MultimodalClassificationMixupScheme,
)
from pytorch.recipes.utils.config_utils import get_class_name_str
from pytorch.recipes.utils.mixup_utils import MixupParams, MixupUtil
from pytorch_lightning.utilities import rank_zero_info
from torchmetrics import MetricCollection
from torchmetrics.classification import Recall


@dataclass
class ClassifierConf:
    input_fusion_name: str = MISSING
    task_name: str = "single_task"
    in_features: int = MISSING
    out_features: int = MISSING
    # pyre-ignore
    loss: Any = MISSING


class MultimodalClassificationModel(torch.nn.Module):
    def __init__(
        self,
        encoders: Mapping[str, torch.nn.Module],
        fusions: Mapping[str, torch.nn.Module],
        fusion_inputs: Mapping[str, List[str]],
        classifiers: Mapping[str, torch.nn.Linear],
        classifier_input_fusion: Mapping[str, str],
        mixup_params: Optional[MixupParams] = None,
    ) -> None:
        super().__init__()
        self.encoders = encoders
        self.fusions = fusions
        self.fusion_inputs = fusion_inputs
        self.classifiers = classifiers
        self.classifier_input_fusion = classifier_input_fusion
        self.nonlinearity: torch.nn.Module = torch.nn.Softmax()
        self.mixup_params = mixup_params

    def forward(self, input: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        output = {}

        for encoder in self.encoders.values():
            encoder_output = encoder(input)
            output.update(encoder_output)
        for fusion_name, fusion in self.fusions.items():
            fusion_input = {key: output[key] for key in self.fusion_inputs[fusion_name]}
            output.update(fusion(fusion_input))

        model_out = {}
        for task_name, classifier in self.classifiers.items():
            model_out[task_name] = classifier(
                output[self.classifier_input_fusion[task_name]]
            )
            if not self.training:
                model_out[task_name] = self.nonlinearity(model_out[task_name])

        return model_out

    def _mixup_input(
        self,
        input: Dict[str, torch.Tensor],
        mixup_scheme: MultimodalClassificationMixupScheme,
        mixup_util: MixupUtil,
    ) -> Dict[str, torch.Tensor]:
        """Mixes up the input if required"""
        input_copy = {}
        if mixup_scheme == MultimodalClassificationMixupScheme.INPUT:
            for channel_name in self.encoders:
                input_copy[channel_name] = mixup_util.mixup(input[channel_name])
        else:
            input_copy = input
        return input_copy

    def _mixup_encoder_forward(
        self,
        input: Dict[str, torch.Tensor],
        mixup_scheme: MultimodalClassificationMixupScheme,
        mixup_util: MixupUtil,
    ) -> Dict[str, torch.Tensor]:
        """Does a forward pass on the encoders and mixes up the
        encoder output (if required)
        """
        output = {}
        for modality, encoder in self.encoders.items():
            encoder_output = encoder(input)
            if mixup_scheme == MultimodalClassificationMixupScheme.AFTERENCODING:
                encoder_output[modality] = mixup_util.mixup(encoder_output[modality])
            output.update(encoder_output)
        return output

    def _mixup_fusion_forward(
        self,
        input: Dict[str, torch.Tensor],
        mixup_scheme: MultimodalClassificationMixupScheme,
        mixup_util: MixupUtil,
    ) -> Dict[str, torch.Tensor]:
        """Dose a forward pass on the fusion layers and
        mixes up the output of the fusion layers (if required)
        """
        for fusion_name, fusion in self.fusions.items():
            fusion_input = {key: input[key] for key in self.fusion_inputs[fusion_name]}
            fusion_output = fusion(fusion_input)
            if mixup_scheme == MultimodalClassificationMixupScheme.AFTERFUSION:
                for modality in fusion_output:
                    fusion_output[modality] = mixup_util.mixup(fusion_output[modality])
            input.update(fusion_output)
        return input

    def _mixup_classifier_forward(
        self,
        input: Dict[str, torch.Tensor],
        mixup_scheme: MultimodalClassificationMixupScheme,
        mixup_util: MixupUtil,
    ) -> Dict[str, torch.Tensor]:
        """Does a forward pass on the classifiers and mixup the output of
        classifiers (if required)"""
        model_out = {}
        for task_name, classifier in self.classifiers.items():
            model_out[task_name] = classifier(
                input[self.classifier_input_fusion[task_name]]
            )
            if mixup_scheme == MultimodalClassificationMixupScheme.AFTERCLASSIFIER:
                model_out[task_name] = mixup_util.mixup(model_out[task_name])
            if not self.training:
                model_out[task_name] = self.nonlinearity(model_out[task_name])
        return model_out

    def mixup_forward(
        self,
        input: Dict[str, torch.Tensor],
        mixup_util: MixupUtil,
    ) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
        # pyre-ignore[16]
        mixup_scheme = self.mixup_params.scheme
        if mixup_scheme == MultimodalClassificationMixupScheme.RANDOM:
            mixup_scheme = random.choice(
                MultimodalClassificationMixupScheme.get_all_except_RANDOM()
            )

        input_copy = self._mixup_input(input, mixup_scheme, mixup_util)
        # Forward passes
        encoder_out = self._mixup_encoder_forward(input_copy, mixup_scheme, mixup_util)
        fusion_out = self._mixup_fusion_forward(encoder_out, mixup_scheme, mixup_util)
        model_out = self._mixup_classifier_forward(fusion_out, mixup_scheme, mixup_util)

        # mixup the lables
        mixed_target = {}
        for task in model_out:
            mixed_target[task] = mixup_util.mixup_labels(input[task])

        return model_out, mixed_target


class MultimodalClassification(pl.LightningModule):
    def __init__(
        self,
        encoders: Mapping[str, torch.nn.Module],
        fusions: Mapping[str, torch.nn.Module],
        fusion_inputs: Mapping[str, List[str]],
        classifiers: Mapping[str, torch.nn.Linear],
        classifier_input_fusion: Mapping[str, str],
        losses: Mapping[str, torch.nn.Module],
        optimizer: torch.optim.Optimizer,
        freeze_prefixes: Optional[List[str]] = None,
        mixup_params: Optional[MixupParams] = None,
    ) -> None:
        """
        Args:
            encoders: Mapping of channel name to encoder that should be applied to each
                input modality.
            fusions: Mapping of unique fusion identifier to fusion module
            fusion_inputs: Mapping of fusion identifier to the list of input channel names
                that should be passed to the fusion
            classifiers: Mapping of unique task names to Linear layers for classification
            classifier_input_fusion: Mapping of task name to the input fusion name for the
                task
            losses: Mapping of task name to the loss module for the task
            optimizer: torch.optim.Optimizer object for training
            freeze_prefixes: list of prefixes. Any weights that start with these will be
                frozen before training.
            mixup_params: Parameters that specify how and where to apply mixup
        """
        super().__init__()

        self.model = MultimodalClassificationModel(
            encoders=encoders,
            fusions=fusions,
            fusion_inputs=fusion_inputs,
            classifiers=classifiers,
            classifier_input_fusion=classifier_input_fusion,
            mixup_params=mixup_params,
        )
        self.mixup_params = mixup_params
        self.losses = losses
        self.optimizer = optimizer
        self.freeze_prefixes: List[str] = freeze_prefixes or []
        # pyre-fixme[4]: Attribute must be annotated.
        self.example_input_array = None

        self.build_metrics()

    def get_tasks_model(self, task_list: List[str]) -> MultimodalClassificationModel:
        """
        Return MultimodalClassificationModel for specfied tasks
        """
        encoders = torch.nn.ModuleDict()
        fusions = torch.nn.ModuleDict()
        fusion_inputs = {}
        classifiers = torch.nn.ModuleDict()
        classifier_input_fusion = {}

        fusion_names = set()
        encoder_names = set()
        for task in task_list:
            classifiers[task] = self.model.classifiers[task]
            classifier_input_fusion[task] = self.model.classifier_input_fusion[task]
            fusion_names.add(classifier_input_fusion[task])

        for fusion_name in fusion_names:
            fusions[fusion_name] = self.model.fusions[fusion_name]
            fusion_inputs[fusion_name] = self.model.fusion_inputs[fusion_name]
            encoder_names.update(fusion_inputs[fusion_name])

        for encoder_name in encoder_names:
            encoders[encoder_name] = self.model.encoders[encoder_name]

        return MultimodalClassificationModel(
            encoders=encoders,
            fusions=fusions,
            fusion_inputs=fusion_inputs,
            classifiers=classifiers,
            classifier_input_fusion=classifier_input_fusion,
        )

    def build_metrics(self) -> None:
        for phase in ("train", "val", "test"):
            task_metrics = torch.nn.ModuleDict()
            for task in self.model.classifiers:
                task_metrics[task] = MetricCollection(
                    {"recall": Recall(self.model.classifiers[task].out_features)}
                )
            setattr(self, f"{phase}_metrics", task_metrics)

    def setup(self, stage: Optional[str] = None) -> None:
        if stage != "fit" or not self.freeze_prefixes:
            return
        trainable_params = []
        frozen_params = []
        for name, param in self.named_parameters():
            should_be_frozen = any(
                name.startswith(prefix) for prefix in self.freeze_prefixes
            )
            if should_be_frozen:
                frozen_params.append(name)
                param.requires_grad = False
            else:
                trainable_params.append(name)

        rank_zero_info(
            f"Frozen params: {frozen_params}\nTrainable params: {trainable_params}"
        )

    # Do not remove.  Needed to maintain torchscriptability, see https://fburl.com/wiki/b5f028m0
    # pyre-ignore[14] - `forward` overrides method defined in `pl.core.lightning.LightningModule`
    # inconsistently. Could not find parameter `Variable(unknown)` [`Keywords(unknown)`] in overriding signature.
    def forward(self, input: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        return self.model(input)

    def compute_loss_with_mixup(
        self,
        mixup_util: MixupUtil,
        model_out: Dict[str, torch.Tensor],
        original_target: Dict[str, torch.Tensor],
        mixedup_target: Dict[str, torch.Tensor],
    ) -> torch.Tensor:
        loss = []
        for task_name in model_out:
            if task_name in original_target:
                criterion = self.losses[task_name]
                loss.append(
                    mixup_util.compute_loss(
                        criterion,
                        model_out[task_name],
                        original_target[task_name],
                        mixedup_target[task_name],
                    )
                )

        return sum(loss) / len(loss)

    def compute_loss(
        self, model_out: Dict[str, torch.Tensor], target: Dict[str, torch.Tensor]
    ) -> torch.Tensor:
        loss = []
        for task_name in model_out:
            if task_name in target:
                loss.append(
                    self.losses[task_name](model_out[task_name], target[task_name])
                )

        return sum(loss) / len(loss)

    def update_and_compute_metrics(
        self,
        model_out: Dict[str, torch.Tensor],
        target: Dict[str, torch.Tensor],
        phase_type: str,
    ) -> Dict[str, Any]:
        metrics = getattr(self, f"{phase_type}_metrics")
        metric_dict = {}
        for task_name, metrics in metrics.items():
            if task_name not in target:
                continue
            preds = model_out[task_name]
            if phase_type == "train":
                preds = F.softmax(preds)
            value = metrics(preds, target[task_name])
            for metric_name in value:
                metric_dict[f"{phase_type}/{task_name}/{metric_name}"] = value[
                    metric_name
                ]
        return metric_dict

    def reset_metrics(self, phase_type: str) -> None:
        metrics = getattr(self, f"{phase_type}_metrics")
        for _, metric in metrics.items():
            metric.reset()

    # pyre-fixme[2]: Parameter must be annotated.
    def calculate_epoch_end_loss(self, outputs, phase_type: str) -> None:
        losses = [output["loss"] for output in outputs]
        avg_loss = torch.mean(torch.stack(losses))
        self.log(f"Losses/{phase_type}_loss", avg_loss)

    def mixup_forward(
        self, input: Dict[str, torch.Tensor], mixup_util: MixupUtil
    ) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
        return self.model.mixup_forward(input, mixup_util)

    @staticmethod
    def _get_mixup_util(batch: Dict[str, torch.Tensor]) -> MixupUtil:
        batch_size = batch[list(batch)[0]].shape[0]
        return MixupUtil(batch_size)

    def _step(
        self,
        batch: Dict[str, torch.Tensor],
        batch_idx: int,
        phase_type: str,
    ) -> Dict[str, torch.Tensor]:
        if phase_type == "train" and self.mixup_params:
            mixup_util = self._get_mixup_util(batch)
            model_out, mixed_up_target = self.mixup_forward(batch, mixup_util)
            loss = self.compute_loss_with_mixup(
                mixup_util, model_out, batch, mixed_up_target
            )
        else:
            model_out = self.forward(batch)
            loss = self.compute_loss(model_out, batch)
        self.log(f"{phase_type}_loss", loss)
        metric_dict = self.update_and_compute_metrics(
            model_out, batch, phase_type=phase_type
        )
        self.log_dict(metric_dict)
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

    def training_epoch_end(
        self, outputs: List[Union[Dict[str, Any], torch.Tensor]]
    ) -> None:
        self.calculate_epoch_end_loss(outputs, "train")
        self.reset_metrics("train")

    def validation_epoch_end(
        self, outputs: List[Union[Dict[str, Any], torch.Tensor]]
    ) -> None:
        self.calculate_epoch_end_loss(outputs, "val")
        self.reset_metrics("val")

    def test_epoch_end(
        self, outputs: List[Union[Dict[str, Any], torch.Tensor]]
    ) -> None:
        self.calculate_epoch_end_loss(outputs, "test")
        self.reset_metrics("test")

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return self.optimizer


@dataclass
class MultimodalClassificationModuleConf(MultimodalModuleConf):
    _target_: str = get_class_name_str(MultimodalClassification)
    classifier: List[ClassifierConf] = field(default_factory=list)


cs: ConfigStore = ConfigStore.instance()


cs.store(
    group="schema/module",
    name="multimodal_classification",
    node=MultimodalClassificationModuleConf,
    package="module",
)


def validate_multimodal_classification_config(
    embeddings_conf: List[EmbeddingConf],
    encoders_conf: List[EncoderConf],
    fusion_conf: List[FusionConf],
    classifier_conf: List[ClassifierConf],
) -> None:
    """
    Validate input configurations for MultimodalClassification
    """

    # validate common multimodal components here
    validate_multimodal_config(
        embeddings_conf=embeddings_conf,
        encoders_conf=encoders_conf,
        fusion_conf=fusion_conf,
    )

    # check if classifier input fusion names exist
    fusion_names = [fusion.fusion_name for fusion in fusion_conf]
    for classifier in classifier_conf:
        if classifier.input_fusion_name not in fusion_names:
            raise AssertionError(
                f"{classifier.input_fusion_name} not found in fusion configuration"
            )


def convert_hydra_conf_to_module(
    module_conf: MultimodalClassificationModuleConf, validate_config: bool = True
) -> MultimodalClassification:
    """
    Args:
        module_conf: Config to build MultimodalClassification module. Following
            keys are expected to be in the module_conf.
            embeddings: word embeddings to be used with corresponding channel name
            encoders: This is a list of model configs that should be applied to each
                input modality. Each model config contains 3 keys:
                channel_name: input channel_name that will be processed via this encoder
                encoder_args: constructor parameters for the encoder
                dict_input: boolean value to control whether the encoder expects a
                    dict input or a tensor input.
            fusion: This is a list of fusion modules which define how the outputs of the
                encoders are fused. Each fusion config contains three keys:
                fusion_name: A unique name to identify this fusion module
                input_encoder_names: The encoder outputs that should be passed to this
                    fusion module
                fusion_args: constructor parameters for the fusion module
            classifier: This is a list of parameters to define the linear laers, one
                for each task. Each classifier config contains 5 keys:
                input_fusion_name: The identifier for the fusion module whose output
                    is passed to the classifier
                task_name: A unique name for the classifier. For a single task, this could be "single_task"
                in_features: The input dimension for the linear layer
                out_features: The output classes for the task
                loss: The loss function for the task
            optim: the optimizer to be used
            freeze_prefixes: list of prefixes. Any weights that start with these will be
                frozen before training.
        validate_config: boolean to control whether the input config should be validated
            before building.
    """

    # build embeddings and encoders if provided
    # both embeddings and encoders have channel_name to identify correspondence.

    if validate_config:
        validate_multimodal_classification_config(
            embeddings_conf=module_conf.embeddings,
            encoders_conf=module_conf.encoders,
            fusion_conf=module_conf.fusion,
            classifier_conf=module_conf.classifier,
        )
    encoders = build_encoders(
        encoders_conf=module_conf.encoders, embeddings_conf=module_conf.embeddings
    )

    # build fusion modules
    fusions, fusion_inputs = build_fusion(
        fusion_conf=module_conf.fusion, encoders=encoders
    )

    # build classifiers
    classifiers = torch.nn.ModuleDict()
    classifier_input_fusion = {}
    losses = torch.nn.ModuleDict()

    for classifier in module_conf.classifier:
        in_features = (
            classifier.in_features or fusions[classifier.input_fusion_name].output_dim
        )
        classifiers[classifier.task_name] = torch.nn.Linear(
            in_features, classifier.out_features
        )
        classifier_input_fusion[classifier.task_name] = classifier.input_fusion_name

        losses[classifier.task_name] = hydra.utils.instantiate(classifier.loss)

    parameters = (
        # pyre-ignore
        list(encoders.parameters())
        + list(fusions.parameters())
        + list(classifiers.parameters())
    )
    optimizer = hydra.utils.instantiate(module_conf.optim, parameters)
    mixup_params = None
    if module_conf.mixup:
        mixup_params = OmegaConf.to_container(module_conf.mixup)
        # pyre-ignore
        mixup_params["scheme"] = MultimodalClassificationMixupScheme[
            # pyre-ignore
            mixup_params["scheme"]
        ]
        # pyre-ignore
        mixup_params = MixupParams(**mixup_params)

    return MultimodalClassification(
        encoders=encoders,
        fusions=fusions,
        fusion_inputs=fusion_inputs,
        classifiers=classifiers,
        classifier_input_fusion=classifier_input_fusion,
        losses=losses,
        optimizer=optimizer,
        freeze_prefixes=module_conf.freeze_prefixes,
        mixup_params=mixup_params,
    )
