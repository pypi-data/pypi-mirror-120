from . import fb_multimodal_imports  # noqa # @fb-only


def register_components() -> None:
    """
    Calls register_components() for all subfolders so we can register
    subcomponents to Hydra's ConfigStore.
    """

    from pytorch.recipes.multimodal.datamodule import (
        register_components as datamodule_components,
    )

    datamodule_components()

    from pytorch.recipes.multimodal.module import (
        register_components as module_components,
    )

    module_components()

    import pytorch.recipes.multimodal.multimodal_train_app  # noqa
