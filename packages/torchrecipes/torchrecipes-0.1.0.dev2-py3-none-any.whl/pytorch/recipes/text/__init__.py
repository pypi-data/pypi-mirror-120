#!/usr/bin/env python3

# pyre-strict


def register_components() -> None:
    """
    Calls register_components() for all subfolders so we can register
    subcomponents to Hydra's ConfigStore.
    """

    from pytorch.recipes.text.datamodule import (
        register_components as datamodule_components,
    )

    datamodule_components()

    from pytorch.recipes.text.module import register_components as module_components

    module_components()

    import pytorch.recipes.text.doc_classification_train_app  # noqa
