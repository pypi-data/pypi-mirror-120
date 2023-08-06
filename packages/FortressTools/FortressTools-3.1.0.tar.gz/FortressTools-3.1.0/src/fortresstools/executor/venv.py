from .base import BaseExecutor
from ..utils.logger import logger
import os


class VenvExecutor(BaseExecutor):
    def __init__(self, path, executor):
        self._path = path
        self._executor = executor

    def run(self, cmd, *cmds):
        logger.info("Running command in virtualenv %s" % self._path)
        vex = "vex --path %s" % (self._path)
        cmd = "%s %s" % (vex, cmd)
        for item in cmds:
            cmd = cmd + " && " + "%s %s" % (vex, item)
        return self._executor.run_command(cmd)
