"""
LOVE version selector and downloader
"""
import sys
from pathlib import Path
from subprocess import call
import argparse

from .game import Game
from .download_love import download
from . import config
from . import platform


def main():
    config.read()

    parser = parser = argparse.ArgumentParser(description="LÖVE launcher")
    parser.add_argument("--version", help="Version override")
    parser.add_argument("game", help="The .love file")
    args, unknown_args = parser.parse_known_args()

    if len(sys.argv) < 2:
        print("No game provided!")
        sys.exit(0)

    version = args.version
    if not version:
        try:
            game = Game(Path(args.game))
            print("löve game version:", game.version)
            version = game.version
        except RuntimeError as e:
            print("Could not determine version: ", e)
            version = config.values["philander"].get("defaultVersion")
            if not version is None:
                print("Assuming default version: '{}'".format(version))
            else:
                sys.exit(0)

    if config.values["commands"].get(version) is None:
        if platform.current == platform.Platform.Windows and not config.values["philander"].get("downloadUrl") is None:
            love_path = Path(config.values["philander"].get("loveDirectory")) / version
            love_exe_path = love_path / "love.exe"
            if not love_path.exists() or not love_exe_path.exists():
                print("Downloading löve version '{}'..".format(version))
                download_url = config.values["philander"].get("downloadUrl").format(version=version)
                download(download_url, str(love_path))
            config.values["commands"][version] = str(love_exe_path)
            config.write()
        else:
            print("löve version '{}' is not installed.".format(version))
            sys.exit(0)

    call([config.values["commands"].get(version), args.game, unknown_args])


if __name__ == '__main__':
    main()
