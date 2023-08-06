from .base import BaseCommand


class VenvCreateCommand(BaseCommand):
    def execute(self):
        cmd = f"{self.python} -m venv {self.path} {self.options}"
        return self._executor.run(cmd)
