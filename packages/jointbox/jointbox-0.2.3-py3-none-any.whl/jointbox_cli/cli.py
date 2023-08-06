#    JointBox CLI
#    Copyright (C) 2021 Dmitry Berezovsky
#    The MIT License (MIT)
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc
import argparse
import logging
import os
import pathlib
import sys
from typing import List

from cli_rack import CLI, ansi
from cli_rack.modular import CliAppManager, CliExtension
from cli_rack.utils import run_executable

from jointbox_cli.yaml_tools import JointboxYamlTools
from strome.core import Pipeline, run_pipeline

from jointbox_cli.core import read_config_yaml, prepare_pipeline, write_generated_yaml
from jointbox_cli.pipeline import JointboxRuntime
from jointbox_cli.__version__ import __version__ as VERSION

LOGGER = logging.getLogger("cli")


class ConfigAwareCliExtension(CliExtension, metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flow_runtime: JointboxRuntime = None  # type: ignore
        self.pipeline: Pipeline = None  # type: ignore
        self.esphome_executable = "esphome"

    @classmethod
    def setup_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument("config_file", type=str, action="store", help="Config file (.yaml)")

    def handle(self, args: argparse.Namespace):
        # Check if config file exists
        config_path = pathlib.Path(args.config_file)
        if not config_path.exists():
            raise ValueError("Config file {} doesn't exist".format(str(config_path)))
        self.flow_runtime = read_config_yaml(str(config_path))
        self.pipeline = prepare_pipeline(self.flow_runtime)

    def process(self):
        LOGGER.info("Starting processing...")
        run_pipeline(self.pipeline, self.flow_runtime)
        LOGGER.info("Processing finished")

    def process_and_output_config_file(self) -> str:
        self.process()
        generated_file_path = os.path.join(
            os.path.dirname(self.flow_runtime.config_path), "_gen_" + os.path.basename(self.flow_runtime.config_path)
        )
        write_generated_yaml(self.flow_runtime, generated_file_path)
        LOGGER.info("Generated temporary file: " + generated_file_path)
        return generated_file_path

    def run_esphome(self, *arguments):
        LOGGER.info("")
        LOGGER.info("Starting EspHome")
        LOGGER.info("")
        run_executable(*(self.esphome_executable,) + arguments)


class ConfigExtension(ConfigAwareCliExtension):
    COMMAND_NAME = "config"
    COMMAND_DESCRIPTION = "Validates and outputs processed config into StdOut"

    def handle(self, args: argparse.Namespace):
        super().handle(args)
        config_path = self.process_and_output_config_file()
        self.run_esphome("config", config_path)


class RunExtension(ConfigAwareCliExtension):
    COMMAND_NAME = "run"
    COMMAND_DESCRIPTION = "Validate the configuration, create a binary, upload it, and start logs."

    def handle(self, args: argparse.Namespace):
        super().handle(args)
        config_path = self.process_and_output_config_file()
        self.run_esphome("run", config_path)


class CompileExtension(ConfigAwareCliExtension):
    COMMAND_NAME = "compile"
    COMMAND_DESCRIPTION = "Read the configuration and compile a program"

    def handle(self, args: argparse.Namespace):
        super().handle(args)
        config_path = self.process_and_output_config_file()
        self.run_esphome("compile", config_path)


def main(argv: List[str]):
    CLI.setup()
    CLI.debug_mode()
    CLI.print_info("\nJointBox CLI version {}\n".format(VERSION), ansi.Mod.BOLD & ansi.Fg.LIGHT_BLUE)
    app_manager = CliAppManager("jointbox")
    app_manager.parse_and_handle_global()
    app_manager.register_extension(ConfigExtension)
    app_manager.register_extension(RunExtension)
    app_manager.register_extension(CompileExtension)
    app_manager.setup()
    JointboxYamlTools.initialize()
    try:
        # Parse arguments
        parsed_commands = app_manager.parse(argv)
        # Run
        exec_manager = app_manager.create_execution_manager()
        exec_manager.run(parsed_commands)
    except Exception as e:
        CLI.print_error(e)


def entrypoint():
    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
