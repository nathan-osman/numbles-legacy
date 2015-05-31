"""
Settings for Numbles.

Settings are divided into two files - base.py stores global settings that are
always the same across installations. local.py stores settings that are specific
to a particular installation.

When setting up Numbles, copy the local.py.default file to local.py and modify
the values as necessary. The local.py file is included in .gitignore.
"""

# First import the global settings
from .base import *

# Next, import the local settings, allowing them to override global values
from .local import *
