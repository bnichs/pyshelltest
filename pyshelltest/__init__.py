import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from pydoc import locate
from subprocess import PIPE, Popen, CompletedProcess
from typing import List, Union
from unittest import TestCase

import toml

logger = logging.getLogger(__name__)


DEFAULT_COMMAND_TIMEOUT = 20


class ExceptionForTesting(Exception):
    """A custom exception class used for unit tests of this module, should never be raised otherwise"""
    pass
    # def __init__(self):
    #     super().__init__("fooooo")


@dataclass
class PyShellCommand(object):
    name: str
    command: List[str]
    extra: dict

    @classmethod
    def from_d(cls, name: str, command: List[str], **d):
        return PyShellCommand(name, command, extra=d)

    @property
    def config(self):
        return dict(name=self.name,
                    command=self.command,
                    **self.extra)

    def check_returncode(self, process: Popen):
        logger.debug("Got return code %d", process.returncode)
        if process.returncode != self.expected_return_code:
            logger.debug("Return code %d didn't match expected %d", process.returncode, self.expected_return_code)
            assert False, f"Bad return code, expected 0 and got {process.returncode}."
        else:
            logger.debug("Return code matched expected %d", self.expected_return_code)
            assert True, "Command ran successfully"

    def check_output(self, process: Popen, stdout: str, stderr: str):
        if self.stdout_contains is not None:
            assert self.stdout_contains in stdout, f"Expected stdout to contain {self.stdout_contains}"

        if self.stderr_contains is not None:
            assert self.stderr_contains in stderr, f"Expected stderr to contain {self.stderr_contains}"

    def gen_test(self):
        logger.debug("Generating test with config: %s", self.config)
        def the_test(self_for_test):
            try:
                process = Popen(self.command, stdout=PIPE, stderr=PIPE)
                process.wait(timeout=self.timeout)

                stdout, stderr = process.stdout.read(), process.stderr.read()
                stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")

                if self.print_output:
                    out = process.stdout.read().decode("utf-8")
                    print(out)

                self.check_returncode(process)
                self.check_output(process, stdout, stderr)

                if self.raise_exception_for_testing:
                    raise ExceptionForTesting()
            except Exception as e:
                # Naked so we can compare to possible self.error.error_class
                logger.debug("Failed to run script, got %s", e.__class__)
                if self.error and self.error_class:
                    assert isinstance(e, self.error_class), f"Expected error class {self.error_class} but instead got {e.__class__}"
                else:
                    # Raise the caught exception
                    raise
        return the_test

    def get(self, name: str, default=None):
        return self.extra.get(name, default)

    @property
    def raise_exception_for_testing(self):
        return self.extra.get("_raise_testing_exception", False)

    @property
    def expected_return_code(self):
        return self.error.get("returncode", 0)

    @property
    def stdout_contains(self):
        return self.get("stdout_contains", None)

    @property
    def stderr_contains(self):
        return self.get("stderr_contains", None)

    @property
    def error_class(self) -> type:
        # If no class was specified just grab a generic exception since all should fall under that
        class_name = self.error.get("error_class", "Exception")
        logger.debug("Loading class %s", class_name)
        kls = locate(class_name)

        if kls is None:
            raise ValueError(f"Couldn't load class {class_name}")
        return kls

    @property
    def error(self):
        return self.get("error", {})

    @property
    def timeout(self):
        return self.get("timeout", default=DEFAULT_COMMAND_TIMEOUT)

    @property
    def print_output(self):
        return self.get("print_output", False)

    @property
    def test_name(self):
        return f"test_{self.name}"


@dataclass
class PyShellTestGenerator(object):
    commands: List[PyShellCommand]

    @classmethod
    def from_toml(cls, path: Union[str, Path]) -> "PyShellTestGenerator":
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path) as f:
            settings = toml.load(f)

        return cls.from_d(settings)

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "PyShellTestGenerator":
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path) as f:
            settings = json.load(f)

        return cls.from_d(settings)

    @classmethod
    def from_d(cls, settings: dict):
        comms = []
        for d in settings['command']:
            com = PyShellCommand.from_d(**d)
            comms.append(com)

        return PyShellTestGenerator(comms)

    def generate(self):
        cls = type('A', (TestCase,),
                   {'__doc__': f'class generated by {self.__class__.__name__}'}
                   )
        for com in self.commands:
            t = com.gen_test()
            setattr(cls, com.test_name, t)
        return cls

