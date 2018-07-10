import os
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import shutil

from . import platform
from . import config

def download(url: str, target_path: str):
    assert(platform.current == platform.Platform.Windows)

    print("Downloading '{}' to '{}'..".format(url, target_path))

    os.makedirs(target_path, exist_ok=True)

    with urlopen(url) as response:
        with ZipFile(BytesIO(response.read())) as zipfile:
            zipfile.extractall(target_path)

    # This is so horrible, but I don't know how to do it better
    dir_path = os.path.join(target_path, os.listdir(target_path)[0])
    for element in os.listdir(dir_path):
        shutil.move(os.path.join(dir_path, element), target_path)
    os.rmdir(dir_path)
