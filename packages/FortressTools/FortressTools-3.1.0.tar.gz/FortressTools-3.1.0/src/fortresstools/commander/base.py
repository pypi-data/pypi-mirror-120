from ..runner import BaseRunner
from ..command import *
from ..executor import *
import yaml
import os
import re

from rich import print

class NoScriptDefinition(Exception):
    def __init__(self, name):
        self.name = name


class WrongArgument(Exception):
    def __init__(self, name):
        self.name = name


class Commander:
    def __init__(self, script, settings):
        super().__init__()
        self._script = yaml.load(open(script, 'r'), Loader=yaml.FullLoader)
        self._settings = settings
        self._runner = BaseRunner()
        self._args_pattern = re.compile(r"\${(.*?)}")

    def _get_input(self, items):
        settings = {}
        for arg, info in items.items():
            settings[arg] = input(f"{info}: ")
        return settings

    def _check_script(self, script):
        if script not in self._script:
            raise NoScriptDefinition(script)

    def _get_command(self, name):
        cmd = globals()[f"{name}Command"]
        return cmd

    def _get_variable(self, value, data):
        split = value.split(".")
        for item in split:
            if type(data) is dict:
                if item in data:
                    data = data[item]
                elif item == "all":
                    pass
                else:
                    raise WrongArgument(item)
        return data

    def _parse_variables(self, variables, **data):
        for key, value in variables.items():
            for match in re.finditer(self._args_pattern, value):
                replace = self._get_variable(match.group(1), data)
                if type(replace) is str:
                    pattern = re.compile(match.group().replace("$", "\$").replace(".", "\."))
                    variables[key] = re.sub(pattern, replace, variables[key])
                else:
                    variables[key] = replace
        return variables

    def _get_executor(self, name):
        executor = None
        if name == "shell":
            executor = ShellExecutor()
        elif name == "ssh":
            executor = SshExecutor(self._settings["remote"], self._settings["sshkey"])
        elif name == "venv":
            executor = VenvExecutor(self._settings["venv"], self._get_executor(self._settings["venvExecutor"]))
        return executor

    def make(self, script):
        self._check_script(script)
        script = self._script[script]
        iargs = self._get_input(script["input"]) if "input" in script else []
        self._settings.update(iargs)
        commands = script["commands"]
        env = self._parse_variables(script["env"], settings=self._settings)
        for cmd in commands:
            name = cmd["name"]
            executor = self._get_executor(cmd["executor"])
            args = self._parse_variables(cmd["args"], settings=self._settings, input=iargs, env=env)
            self._runner.add_command(self._get_command(name)(executor, **args))
        self._runner.execute()
