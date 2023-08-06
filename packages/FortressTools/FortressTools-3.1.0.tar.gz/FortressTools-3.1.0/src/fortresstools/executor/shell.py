from .base import BaseExecutor
from ..utils.console import console
from ..utils.logger import logger
import subprocess


class ShellExecutor(BaseExecutor):
    def __init__(self, path=None):
        self._path = path

    def _shell_cmd(self, value):
        logger.panel(value, title="SHELL COMMAND", style="bright_magenta")

    def _shell_error(self, value):
        logger.panel(value, title="SHELL ERROR", style="bright_red")

    def run(self, cmd, *cmds):
        if self._path is not None:
            cmd = "cd %s && %s" % (self._path, cmd)

        for item in cmds:
            cmd = cmd + " && " + item

        self._shell_cmd(cmd)

        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

        info = "Running shell command..."
        with console.status(info) as status:
            while True:
                output = process.stdout.readline()
                if output:
                    logger.info(output.rstrip("\n"))
                if output == '' and process.poll() is not None:
                    break
        code = process.poll()
        if code != 0:
            self._shell_error(process.stderr.read().rstrip())
            self._shell_error("Shell command returned error code: %d" % code)
        return code
