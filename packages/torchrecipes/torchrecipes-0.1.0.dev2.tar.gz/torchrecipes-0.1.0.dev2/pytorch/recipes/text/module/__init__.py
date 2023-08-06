#!/usr/bin/env python3


def register_components() -> None:
    """
    Imports all python files in the folder to trigger the
    code to register them to Hydra's ConfigStore.
    """

    import pytorch.recipes.text.module.doc_classification  # noqa
    import pytorch.recipes.text.module.doc_classification_demo  # noqa
