def register_components() -> None:
    """
    Imports all python files in the folder to trigger the
    code to register them to Hydra's ConfigStore.
    """
    import pytorch.recipes.text.datamodule.doc_classification  # noqa
