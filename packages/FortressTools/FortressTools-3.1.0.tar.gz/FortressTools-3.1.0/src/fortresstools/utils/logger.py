from .console import console
from rich.panel import Panel


class Logger:
    def __init__(self, raw=False):
        self._raw = raw
        self._console = console
        self._print = self._console.out if self._raw else self._console.print

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, value):
        self._raw = value
        self._print = self._console.out if self._raw else self._console.print

    def info(self, value):
        self._print(value, style="info")

    def warning(self, value):
        self._print("WARNING: {}".format(value), style="warning")

    def error(self, value):
        self._print("ERROR: {}".format(value), style="error")

    def fatal(self, value):
        msg = value if self._raw else Panel(value, title="FATAL ERROR", highlight=True, style="fatal")
        self._print(msg)
        sys.exit()

    def panel(self, value, title, style="panel"):
        msg = value if self._raw else Panel(value, title=title, highlight=True, style=style)
        self._print(msg)


logger = Logger()
