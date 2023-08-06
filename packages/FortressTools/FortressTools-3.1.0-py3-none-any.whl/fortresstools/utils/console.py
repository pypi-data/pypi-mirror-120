from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "info" : "bright_white",
    "warning": "bright_yellow",
    "error": "bright_red",
    "fatal": "bold red",
    "debug": "bright_blue",
    "panel": "bright_white",
    "shell_cmd" : "bright_white",
    "shell_error": "bright_red",
})

console = Console(theme=custom_theme)
