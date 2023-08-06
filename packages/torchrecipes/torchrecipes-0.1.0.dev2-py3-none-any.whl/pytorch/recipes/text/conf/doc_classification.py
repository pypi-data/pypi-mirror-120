#!/usr/bin/env python3

# pyre-strict

# Components to register with this config
from pytorch.recipes.text import register_components

# Register all Text DataModules and Modules so they are available for this config
register_components()
