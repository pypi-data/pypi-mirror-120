from pathlib import Path
import yaml
import re


class Settings:
    def __init__(self):
        self._global_file = Path("~/.config/fortresstools/config.cfg").expanduser()
        self._project_file = "project.ft"

    @property
    def config_directory(self):
        return self._global_file.parent

    def _find_project_config_file(self):
        pattern = re.compile(self._project_file)
        settings_file = None
        current = Path.cwd()
        for path in [current] + [x for x in current.parents]:
            for f in path.iterdir():
                if f.is_file():
                    if re.search(pattern, str(f)):
                        settings_file = f
                        break
            if settings_file is not None:
                break
        return settings_file

    def _get_project_settings(self):
        settings_file = self._find_project_config_file()
        settings = None
        if settings_file is not None:
            settings = yaml.load(open(settings_file, 'r'), Loader=yaml.FullLoader)
        return settings

    def _get_global_settings(self):
        settings = yaml.load(open(self._global_file, 'r'), Loader=yaml.FullLoader)
        return settings

    def get_settings(self):
        settings = self._get_global_settings()
        project_settings = self._get_project_settings()
        if project_settings is not None:
            settings.update(project_settings)
        return settings
