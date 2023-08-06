from .base import BaseExecutor
from ..utils.console import console
from ..utils.logger import logger
from contextlib import contextmanager
import paramiko


class SshExecutor(BaseExecutor):
    def __init__(self, remote, key, port=22, path=None):
        self._key = self._get_key(key)
        self._remote = remote
        self._port = port
        self._path = path

    def _ssh_info(self, value):
        logger.panel(value, title="SSH", style="white")

    def _ssh_cmd(self, value):
        logger.panel(value, title="SSH COMMAND", style="bright_magenta")

    def _ssh_error(self, value):
        logger.panel(value, title="SSH ERROR", style="bright_red")

    def _get_key(self, key):
        if key["type"] == "ed25519":
            key = paramiko.Ed25519Key.from_private_key_file(key["path"])
        elif key["type"] == "rsa":
            key = paramiko.RSAKey.from_private_key_file(key["path"])
        return key

    @contextmanager
    def _ssh_connection(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self._remote,
                           port=self._port,
                           pkey=self._key,
                           look_for_keys=True,
                           timeout=60,
                           auth_timeout=60)
            self._ssh_info("Connected to %s on port %d" % (self._remote, self._port))
            yield client
        finally:
            client.close()
            self._ssh_info("Disconnected from %s" % (self._remote))

    def run(self, cmd, *cmds):
        if self._path is not None:
            cmd = "cd %s && %s" % (self._path, cmd)

        for item in cmds:
            cmd = cmd + " && " + item

        with self._ssh_connection() as client:
            stdin, stdout, stderr = client.exec_command(cmd)
            self._ssh_cmd(cmd)
            info = "Running command throught SSH..."
            with console.status(info) as status:
                while True:
                    line = stdout.readline()
                    if not line:
                        break
                    else:
                        logger.info(line.rstrip("\n"))
            status = stdout.channel.recv_exit_status()
            if status != 0:
                self._ssh_error(stderr.read().decode().rstrip())
                self._ssh_error("SSH command returned error code: %d" % status)
            return status
