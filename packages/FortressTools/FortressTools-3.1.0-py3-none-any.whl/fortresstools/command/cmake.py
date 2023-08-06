from .base import BaseCommand


class CmakeGenerateCommand(BaseCommand):
    def execute(self):
        cmd = f"cmake -G \"{self.generator}\" -S {self.source} -B {self.path} {self.options}"
        return self._executor.run(cmd)


class CmakeBuildCommand(BaseCommand):
    def execute(self):
        cmd = f"cmake --build {self.path} --target {self.target} {self.options}"
        return self._executor.run(cmd)
