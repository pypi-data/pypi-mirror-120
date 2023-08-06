from rich.traceback import install as traceback
from rich import print
from fortresstools.commander import Commander, NoScriptDefinition
from fortresstools.utils.settings import Settings
from fortresstools.utils.logger import logger
from fortresstools.scripts.scripts import Scripts
from pathlib import Path
import argparse
import sys
import importlib.resources as resources


def main():
    traceback()

    description = "FortressTools - use at your own risk."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-r", "--raw", action="store_true", help="Print raw output strings")

    description = "Run -h/--help for subcommand to see detailed help"
    subparser = parser.add_subparsers(dest="cmd", description=description)

    cmd_init = subparser.add_parser("init", help='Initialize new project')
    cmd_init.add_argument("script", help="Script file. Can be build in name or path to file.")

    cmd_make = subparser.add_parser("make", help='Execute commands on FortressTools project')
    cmd_make.add_argument("command", nargs="+",  help='List of the commands to execute.')

    args = parser.parse_args()

    logger.raw = args.raw

    settings = Settings().get_settings()

    if args.cmd == "init":
        script = args.script
        settings.update({"script": script})
        commands = ["NewProject"]
    else:
        script = settings["script"]
        commands = args.command

    script_file = Scripts().get_script(script)
    commander = Commander(script_file, settings)

    for cmd in commands:
        try:
            commander.make(cmd)
        except NoScriptDefinition:
            logger.error(f"In [yellow]{args.script}[/yellow] script file there is no [yellow]{cmd}[/yellow] script definition!")
            sys.exit(1)


if __name__ == "__main__":
    main()
