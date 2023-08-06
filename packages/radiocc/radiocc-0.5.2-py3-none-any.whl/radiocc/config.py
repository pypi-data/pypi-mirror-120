#!/usr/bin/env python3

"""
Configurate parameters.
"""

from pathlib import Path
from typing import Optional  # noqa: F401

import ruamel.yaml
import yaml
from dotmap import DotMap
from pudb import set_trace as bp  # noqa: F401

import radiocc


class Cfg:
    """Structure representation of the configurable parameters."""

    # Configurable parameters default values.
    __DEFAULT_TO_PROCESS = Path("./to_process")
    __DEFAULT_RESULTS = Path("./results")

    # Path to the folder containing the data to be processed.
    __to_process = __DEFAULT_TO_PROCESS

    # Path to the folder where you want the outputs to be saved.
    __results = __DEFAULT_RESULTS

    def __init__(self) -> None:
        pass

    def from_config_file(self) -> None:
        """Load the config file."""
        CFG_FILE = read_config_file()
        self.__parse_config_file(CFG_FILE)

    def __parse_config_file(self, CFG_FILE: DotMap) -> None:
        """Check that the config file is correct."""
        # Create the config.
        if CFG_FILE["to_process"] is not None:
            self.to_process = Path(CFG_FILE["to_process"])

        if CFG_FILE["results"] is not None:
            self.results = Path(CFG_FILE["results"])

    @property
    def to_process(self) -> Path:
        """Get to_process folder path."""
        return self.__to_process

    @to_process.setter
    def to_process(self, PATH: Path) -> None:
        """Set to_process folder path."""
        self.__to_process = PATH

    @property
    def results(self) -> Path:
        """Get results folder path."""
        return self.__results

    @results.setter
    def results(self, PATH: Path) -> None:
        """Set results folder path."""
        self.__results = PATH


def read_config_file() -> DotMap:
    """Load the config file."""
    CFGF_DICT, IND, BSI = ruamel.yaml.util.load_yaml_guess_indent(
        open(radiocc.CFG_PATH)
    )
    return DotMap(CFGF_DICT)


def generate_config() -> None:
    """Generate a config file `config.yaml` in the current directory."""
    # Create empty config.
    CFG = dict(to_process=None, results=None)

    # Change all None to empty.
    radiocc.util.yaml_add_representer_none()

    # Check whether config should be saved.
    save = True
    if radiocc.CFG_PATH.is_file():
        save = radiocc.util.form_yes_or_no(f"Overwrite {radiocc.CFG_PATH}?")

    # Save as a new config file.
    if save:
        with open(radiocc.CFG_PATH, "w") as fp:
            yaml.dump(CFG, fp)
