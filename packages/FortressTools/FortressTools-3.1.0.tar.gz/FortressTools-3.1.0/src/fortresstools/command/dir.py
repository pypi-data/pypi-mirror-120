from .base import BaseCommand
from pathlib import Path
import yaml


class MkdirCommand(BaseCommand):
    def execute(self):
        cmd = "mkdir -p %s" % self.path
        self._executor.run(cmd)


class CreateProjectConfigCommand(BaseCommand):
    def execute(self):
        project_config_file = Path(self.path) / Path("project.ft")
        project_config_file = project_config_file.expanduser()
        with open(project_config_file, "w") as f:
            yaml.dump(self.settings, f)
