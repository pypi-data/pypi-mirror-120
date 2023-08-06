

class BaseRunner():
    def __init__(self):
        self._commands = []

    def add_command(self, cmd):
        if type(cmd) is list:
            self._commands.extend(cmd)
        else:
            self._commands.append(cmd)

    def execute(self):
        while self._commands:
            cmd = self._commands.pop(0)
            cmd.execute()
