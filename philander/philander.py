"""
LOVE version selector and downloader
"""
import sys
from pathlib import Path
from subprocess import call

from .game import Game
from .love_downloader import LoveDownloader

from .platform import Platform


def main():
    if len(sys.argv) < 2:
        print("No game provided!")
        sys.exit(0)

    game = Game(Path(sys.argv[1]))

    downloader = LoveDownloader(Platform.Windows)
    downloader.download(game.version)

    binary = Path(downloader.get_version_folder_name(game.version))/"love.exe"

    call([str("love" / binary), str(game.path)])


if __name__ == '__main__':
    main()
