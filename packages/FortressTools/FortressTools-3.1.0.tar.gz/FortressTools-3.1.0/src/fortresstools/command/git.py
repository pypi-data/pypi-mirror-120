from .base import BaseCommand


class GitInitCommand(BaseCommand):
    def execute(self):
        cmd = f"git init {self.path} {self.options}"
        self._executor.run(cmd)


class GitCloneCommand(BaseCommand):
    def execute(self):
        cmd = f"git clone {self.url} {self.path} {self.options}"
        self._executor.run(cmd)


class GitFetchCommand(BaseCommand):
    def execute(self):
        cmd = f"git -C {self.path} fetch {self.remote} {self.target} {self.options}"
        self._executor.run(cmd)


class GitRemoteAddCommand(BaseCommand):
    def execute(self):
        cmd = f"git -C {self.path} remote add {self.name} {self.template} {self.options}"
        self._executor.run(cmd)


class GitMergeCommand(BaseCommand):
    def execute(self):
        cmd = f"git -C {self.path} merge {self.target} {self.options}"
        self._executor.run(cmd)


class GitInitFromTemplateCommand(BaseCommand):
    def execute(self):
        GitInitCommand(self._executor, path=self.path, options=self.options).execute()
        GitRemoteAddCommand(self._executor, path=self.path, name="template", template=self.template, options=self.options).execute()
        GitFetchCommand(self._executor, path=self.path, target="main", remote="template", options=self.options).execute()
        GitMergeCommand(self._executor, path=self.path, target="template/main", options=self.options).execute()
