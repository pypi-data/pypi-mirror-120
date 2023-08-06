from .base import BaseCommand

class Test1Command(BaseCommand):
    def execute(self):
        cmd = "echo %s" % self.path
        self._executor.run(cmd)


class Test2Command(BaseCommand):
    def execute(self):
        cmd = "echo %s" % self.path
        self._executor.run(cmd)


class Test3Command(BaseCommand):
    def execute(self):
        cmd = "echo %s" % self.path
        self._executor.run(cmd)
