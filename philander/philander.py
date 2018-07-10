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
from .version import Version


def get_download_filename(version_string):
    version = Version(version_string)

    if version.major == 0 and version.minor <= 8:
        filename = "love-{filename}-win-x86.zip".format(filename=version)
    else:
        filename = "love-{filename}-win32.zip".format(filename=version)

    return filename


def main():
    config.read()

    parser = parser = argparse.ArgumentParser(prog="phil", description="LÖVE launcher", epilog="Additional, unrecognized arguments will be passed to the love executable.")
    parser.add_argument("--version", "-v", help="If passed, use the specified version instead of determining it from the love application.")
    parser.add_argument("game", help="The .love file or love application directory.")
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
        download_dir = config.values["philander"].get("downloadDirectory")
        download_url = config.values["philander"].get("downloadUrl")
        if platform.current == platform.Platform.Windows and download_dir is not None and download_url is not None:
            love_path = Path(download_dir) / version
            love_exe_path = love_path / "love.exe"
            if not love_path.exists() or not love_exe_path.exists():
                print("Downloading löve version '{}'..".format(version))
                download_url = download_url.format(filename=get_download_filename(version))
                download(download_url, str(love_path))
            config.values["commands"][version] = str(love_exe_path)
            config.write()
        else:
            print("löve version '{}' is not installed.".format(version))
            sys.exit(0)

    call([config.values["commands"].get(version), args.game, unknown_args])


if __name__ == '__main__':
    main()
