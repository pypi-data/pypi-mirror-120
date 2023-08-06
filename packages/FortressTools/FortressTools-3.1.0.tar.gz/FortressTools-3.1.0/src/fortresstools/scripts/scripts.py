from pathlib import Path
import importlib.resources as resources
from ..utils.settings import Settings

class Scripts:
    def __init__(self):
        self._settings = Settings()

    def _get_script_from_path(self, name):
        script_file = Path(name)
        if script_file.is_file():
            return script_file
        else:
            return None

    def _get_script_from_config(self, name):
        script_file = self._settings.config_directory / f"{name}.yaml"
        if script_file.is_file():
            return script_file
        else:
            return None

    def _get_script_from_package(self, name):
        package = "%s.scripts" % __name__.split('.')[0]
        with resources.path(package, f"{name}.yaml") as script:
            return script

    def get_script(self, name):
        getters = [self._get_script_from_path, self._get_script_from_config, self._get_script_from_package]
        for x in getters:
            script = x(name)
            if script is not None:
                return script
