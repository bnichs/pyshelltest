import json
import logging
import os
import tempfile
from pathlib import Path
from pprint import pprint
from unittest import TestCase

import pytest
import toml

from pyshelltest import PyShellTestGenerator
from tests.config import CONFIG_FILE

logger = logging.getLogger(__name__)


def new_config_path(path: str, new_ext: str):
    if not new_ext.startswith('.'):
        new_ext = f".{new_ext}"
    p, _ = os.path.splitext(path)

    return f"{p}{new_ext}"


def dump_json(json_path=None, toml_path=CONFIG_FILE):
    # json_path = tmp_path / "test-config.json"
    if not json_path:
        tmp_path = tempfile.mkdtemp()
        json_path = Path(tmp_path) / "test-config.json"
    logger.debug("Saving test json file to %s", json_path)

    with open(toml_path) as toml_f:
        with open(json_path, 'w') as json_f:
            toml_d = toml.load(toml_f)
            json.dump(toml_d, json_f, indent=4)
    return json_path


class TestPyShellGenerator(TestCase):
    def test_load_bad_json_config(self):
        with pytest.raises(FileNotFoundError):
            _ = PyShellTestGenerator.from_json("foo.bar.com.json")

    def test_load_bad_toml_config(self):
        with pytest.raises(FileNotFoundError):
            _ = PyShellTestGenerator.from_toml("foo.bar.com.toml")

    def test_load_toml_config(self):
        generator = PyShellTestGenerator.from_toml(CONFIG_FILE)

    # Fixture to inject tmp_path
    def test_load_json_config(self):
        json_path = dump_json()
        generator = PyShellTestGenerator.from_json(json_path)

    def test_toml_equals_json(self):
        json_path = dump_json()
        json_generator = PyShellTestGenerator.from_json(json_path)

        toml_generator = PyShellTestGenerator.from_toml(CONFIG_FILE)

        pprint(toml_generator)
        pprint(json_generator)

        assert toml_generator == json_generator

        # Make sure our equals is sane
        toml_generator.commands = toml_generator.commands[:-1]
        assert toml_generator != json_generator
