from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from bitness import Bitness
from platform import Platform
from version import Version


class LoveDownloader:
    def __init__(self, platform: Platform, bitness: Bitness=Bitness.ThirtyTwo):
        self.platform: Platform = platform
        self.bitness_preference: Bitness = bitness

    def check_version_downloaded(self, folder: str) -> bool:
        """ Checks for the existance of the love version folder and love.exe
            within it
        """
        path = Path("love") / folder

        return path.exists() and path.is_dir() and (path / "love.exe").exists()

    def download(self, version: Version) -> bool:
        """ Downloads the specified version to /love, if it hasn't already been
            downloaded.
        """
        path = Path("love")

        if not path.exists():
            path.mkdir()

        folder = self.get_version_folder_name(version)

        if self.check_version_downloaded(folder):
            return True
        else:
            url = self.construct_url(version, folder)

            print(url)

            with urlopen(url) as response:
                with ZipFile(BytesIO(response.read())) as zipfile:
                    zipfile.extractall(path)

        return True

    def get_version_folder_name(self, version: Version) -> str:
        """ Works out what the folder should be called from the version
            number

            Returns 'love-0.10.1-win32', for instance.
        """
        name = "love-{version}-{platform}{bitness}"

        if self.bitness_preference == Bitness.ThirtyTwo:
            bitness = "32"
        elif self.bitness_preference == Bitness.SixtyFour:
            bitness = "64"

        if self.platform == Platform.Windows:
            platform = "win"

        return name.format(version=version, bitness=bitness, platform=platform)

    def construct_url(self, version: Version, folder: str) -> str:
        """ Returns the bitbucket zip file for the specified folder name.
        """
        url = ("https://bitbucket.org/rude/love/downloads/{folder}.zip")

        return url.format(folder=folder)
