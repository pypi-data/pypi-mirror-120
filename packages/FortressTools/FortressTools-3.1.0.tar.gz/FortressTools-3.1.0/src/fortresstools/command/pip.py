from .base import BaseCommand


class PipInstallPkgCommand(BaseCommand):
    def execute(self):
        cmd = f"python3 -m pip install {self.pkg} {self.options}"
        return self.run(cmd)
