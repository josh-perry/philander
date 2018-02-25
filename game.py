from pathlib import Path
import re


class Game:
    """Represents a LÖVE game"""
    def __init__(self, path: Path) -> None:
        """Constructor"""
        self.path: Path = path
        self.has_main: bool = self.get_has_main()
        self.has_conf: bool = self.get_has_conf()
        self.version: str = None

        if self.has_conf:
            self.version = self.get_version_from_conf()

    def get_has_main(self) -> bool:
        """Checks for main.lua and returns whether or not it exists"""
        main_path: Path = self.path / "main.lua"

        return main_path.exists()

    def get_has_conf(self) -> bool:
        """Checks for conf.lua and returns whether or not it exists"""
        conf_path: Path = self.path / "conf.lua"

        return conf_path.exists()

    def get_version_from_conf(self):
        """Returns the version string from conf.lua"""

        # Assert that we should even be trying to read conf.lua
        assert(self.has_conf)

        conf_path = self.path / "conf.lua"

        # Match only the version string and not 't.version = '
        regex = r'(?:version = "(.*)")'

        # Get matches and remove empty ones
        matches = [re.findall(regex, line) for line in open(conf_path)]
        matches = list(filter(None, matches))

        if len(matches) > 1:
            raise Exception("More than one version found in conf.lua!")

        if len(matches) == 0:
            raise Exception("No version found in conf.lua!")

        return matches[0][0]
