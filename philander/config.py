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

def read():
    global values
    if _config_path.exists():
        values = ConfigParser()
        values.read(_config_path)
    else:
        set_default()
        write()

