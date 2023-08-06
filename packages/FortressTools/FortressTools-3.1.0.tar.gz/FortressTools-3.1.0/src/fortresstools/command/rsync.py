from .base import BaseCommand


class RsyncFromRemoteCommand(BaseCommand):
    def execute(self):
        rsync = "rsync -az --delete"
        source = f"{self.login}@{self.remote}:{self.directory}/"
        destination = self.directory
        cmd = f"{rsync} {source} {destination} {self.options}"
        return self._executor.run(cmd)


class RsyncToRemoteCommand(BaseCommand):
    def execute(self):
        rsync = "rsync -az --delete"
        source = f"{self.directory}/"
        destination = f"{self.login}@{self.remote}:{self.directory}"
        cmd = f"{rsync} {source} {destination} {self.options}"
        return self._executor.run(cmd)
