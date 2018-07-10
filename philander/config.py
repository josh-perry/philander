import sys
from configparser import ConfigParser
from pathlib import Path

import appdirs

from . import platform

_config_dir = Path(appdirs.user_config_dir("philander", "", roaming=True))
_config_path = _config_dir / "config.ini"

values = None

def write():
    _config_path.parent.mkdir(exist_ok=True)
    with open(_config_path, 'w') as f:
        values.write(f)
    print("Wrote default config to '{}'.".format(_config_path))

def set_default():
    global values
    values = ConfigParser()

    values["philander"] = {
        "defaultVersion": "11.1",
    }

    if platform.current == platform.Platform.Windows:
        values["philander"]["downloadDirectory"] = str(_config_dir / "love")
        values["philander"]["downloadUrl"] = "https://bitbucket.org/rude/love/downloads/{filename}"
        values["philander"]["downloadBitness"] = "32"

    values["commands"] = {}

def read(ignore_cwd_config=False):
    global values
    if _config_path.exists():
        values = ConfigParser()
        read_files = values.read(_config_path)
        if len(read_files) == 0:
            raise IOError("Could not read config.")
    else:
        set_default()
        write()

    cwd_config_path = Path("philander.ini")
    if not ignore_cwd_config and cwd_config_path.exists():
        print("Reading philander.ini in current working directory.")
        read_files = values.read(cwd_config_path)
        if len(read_files) == 0:
            raise IOError("Could not read config in current working directory.")
