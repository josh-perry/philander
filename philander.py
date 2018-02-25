"""
LOVE version selector and downloader
"""
import sys
from pathlib import Path

from game import Game
from love_downloader import LoveDownloader

from platform import Platform


def main():
    if len(sys.argv) < 2:
        print("No game provided!")
        exit(0)

    game = Game(Path(sys.argv[1]))

    downloader = LoveDownloader(Platform.Windows)
    downloader.download(game.version)


if __name__ == '__main__':
    main()
