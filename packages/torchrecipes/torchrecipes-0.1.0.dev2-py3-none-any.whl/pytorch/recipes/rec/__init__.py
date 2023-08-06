def register_components() -> None:
    """
    Calls register_components() for all subfolders so we can register
    subcomponents to Hydra's ConfigStore.
    """
    import pytorch.recipes.rec.datamodules.criteo_datamodule  # noqa
    import pytorch.recipes.rec.datamodules.random_rec_datamodule  # noqa
    import pytorch.recipes.rec.modules.sparsenn_classification  # noqa
    import pytorch.recipes.rec.sparsenn_binary_classification_train_app  # noqa
