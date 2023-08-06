from .base import BaseCommand


class SvnCheckoutCommand(BaseCommand):
    def execute(self):
        cmd = f"svn checkout {self.url} {self.path} {self.options}"
        self._executor.run(cmd)

