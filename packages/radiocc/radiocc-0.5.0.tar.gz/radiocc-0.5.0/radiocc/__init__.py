#!/usr/bin/env python3

"""
radiocc
"""

import logging
import os
from pathlib import Path

from radiocc import config
from radiocc.core import run

from .model import Bands, Layers

__all__ = [
    "Bands",
    "Layers",
    "run",
]

# Project variables.
NAME = "radiocc"
VERSION = "0.5.0"

# Logging settings.
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(name)s[%(levelname)s]: %(message)s"
LOG_DATEFMT = "%m/%d/%Y %I:%M:%S %p"

# Runtime variables.
SRC_PATH = Path(os.path.realpath(__file__)).parent
ASSETS_PATH = SRC_PATH / "assets"
CFG_PATH = Path("radiocc.yaml")
LOG_PATH = Path(f"{NAME}.log")
INFORMATION_PATH = ASSETS_PATH / "information"

# Start logging.
logging.basicConfig(
    filename=LOG_PATH,
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATEFMT,
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
LOGGER = logging.getLogger(NAME)
LOGGER.info("Logging enabled.")

# Configurable parameters definition.
cfg = config.Cfg()
