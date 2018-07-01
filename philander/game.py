from zipfile import ZipFile
from pathlib import Path
import re

from .version import Version


class Game:
    """Represents a LÖVE game"""
    def __init__(self, path: Path) -> None:
        """Constructor"""
        self.path: Path = path

        self.is_love_file: bool = self.get_is_love_file()

        if self.is_love_file:
            self.archive = ZipFile(self.path, 'r')

        self.has_main: bool = self.get_has_main()
        self.has_conf: bool = self.get_has_conf()
        self.version: Version = None

        if self.has_conf:
            self.version = self.get_version_from_conf()
        else:
            raise Exception("No conf.lua found!")

    def get_is_love_file(self) -> bool:
        return self.path.is_file() and str(self.path).endswith(".love")

    def get_has_main(self) -> bool:
        """Checks for main.lua and returns whether or not it exists"""
        if self.is_love_file:
            return "main.lua" in [f.filename for f in self.archive.infolist()]

        main_path: Path = self.path / "main.lua"
        return main_path.exists()

    def get_has_conf(self) -> bool:
        """Checks for conf.lua and returns whether or not it exists"""
        if self.is_love_file:
            return "conf.lua" in [f.filename for f in self.archive.infolist()]

        conf_path: Path = self.path / "conf.lua"
        return conf_path.exists()

    def get_version_from_conf(self) -> Version:
        """Returns the version string from conf.lua"""

        # Assert that we should even be trying to read conf.lua
        assert(self.has_conf)

        conf_data = []

        if self.is_love_file:
            with self.archive.open("conf.lua") as f:
                for line in f:
                    conf_data.append(line.decode('utf-8'))
        else:
            with open(self.path / "conf.lua") as f:
                for line in f:
                    conf_data.append(line)

        # Match only the version string and not 't.version = '
        regex = r'(?:version = "(.*)")'

        # Get matches and remove empty ones
        matches = [re.findall(regex, line) for line in conf_data]
        matches = list(filter(None, matches))

        if len(matches) > 1:
            raise Exception("More than one version found in conf.lua!")

        if len(matches) == 0:
            raise Exception("No version found in conf.lua!")

        return Version(matches[0][0])
