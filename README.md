# philander
Launcher for [löve](https://love2d.org/) games, that will choose a löve executable depending on the version specified in `conf.lua` inside the löve application.

If the appropriate version is not yet installed, it will be downloaded automatically (Windows only for now).

# Installation
Just call `pip install -e .` (`-e` - *editable* for easier updating via git) in the root of this repository and start the application once to initialize the configuration file.

# Usage
When starting a löve application via the command line, just replace `love` (or `love.exe`) with `philander`, i.e.:
```console
$ philander game.love

$ philander game.love --foo

$ philander --version 0.10.2 game.love
```

Additional arguments are passed to löve as well and you may override the version (especially useful if the version can not be determined, but you know the correct version).

# Configuration
This is my current configuration:
```ini
[philander]
lovedirectory = C:\Users\Joel\AppData\Roaming\philander\love
defaultversion = 11.1
downloadurl = https://bitbucket.org/rude/love/downloads/love-{version}-win32.zip

[commands]
11.1 = C:\Users\Joel\AppData\Roaming\philander\love\11.1\love.exe
0.10.2 = C:\Users\Joel\AppData\Roaming\philander\love\0.10.2\love.exe
0.9.2 = C:\Users\Joel\AppData\Roaming\philander\love\0.9.2\love.exe
```

* `lovedirectory` is the directory the löve versions are saved in.
* `defaultversion` will be used if the version can not be determined (e.g. because of a missing conf.lua)
* `downloadurl` is the url that will be used for downloading missing löve versions. Adjust this if you want 64-bit löve (32-bit is default) instead.

The values in `[commands]` are the executables that should be used for each löve version.

