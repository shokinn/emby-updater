# emby-updater

emby-updater is a small tool to keep the [Emby media server](https://emby.media/) up to date (even including beta-versions).

## Build Status

**Prod**  
[![Prod Build pipeline status](https://ci.mischaufen.de/api/v1/teams/emby_updater/pipelines/emby-updater/jobs/build/badge)](https://ci.mischaufen.de/teams/emby_updater/pipelines/emby-updater/jobs/build/builds/)

**Workspace**  
[![Workspace pipeline status](https://ci.mischaufen.de/api/v1/teams/emby_updater/pipelines/emby-updater/jobs/build/badge)](https://ci.mischaufen.de/teams/emby_updater/pipelines/emby-updater/jobs/build/builds/)

## Using emby-updater

### All in one binary

Thanks to [PyInstaller](https://www.pyinstaller.org/) you can download emby-updater without to care about any dependencies, because they are inbuilt to the binary. 

Just [head over to the releases page](https://github.com/shokinn/emby-updater/releases) and download the binary.

**Currently only Ubuntu 18.04+ (amd64) is supported.**

### Python code for maximum flexibility

Do you want to control what is running on your system?  
Grab the Python code, install the dependencies and run or modify it :)

#### Setup

```bash
sudo apt update && \
sudo apt install -y python3 python3-pip python3-apt git; \
git clone https://github.com/shokinn/emby-updater.git && \
cd emby-updater && \
pip3 install --user -r requirements.txt
```

### Usage

```
usage: emby-updater.py [-h] [--beta] [-d DOWNLOAD_PATH] [--update] [--version]
                       [-y]

emby-updater will help you to install Emby (updates) easily.

optional arguments:
  -h, --help            show this help message and exit
  --beta                installs Emby beta versions
  -d DOWNLOAD_PATH, --download-path DOWNLOAD_PATH
                        set path for downloaded binaries
  --update              update the script itself if an update is available
  --version             show program's version number and exit
  -y, --yes             automatic yes to prompts. Assume "yes" as answer to
                        all prompts and run non-interactively. If an
                        undesirable situation, such as changing a held package
                        or removing an essential package, occurs then emby-
                        updater.py will abort.

This is an unofficial update tool for the Emby media server.
It's not supported through any official Emby Support.
emby-updater is proudly presented by Philip 'ShokiNN' Henning <mail@philip-henning.com>.
```

## Building binary package

### Setup

```bash
sudo apt update && \
sudo apt install -y python3 python3-pip python3-apt git build-essential; \
git clone https://github.com/shokinn/emby-updater.git && \
cd emby-updater && \
pip3 install --user -r requirements.txt && \
pip3 install --user setuptools && \
pip3 install --user pyinstaller
```

### Build binary package

```bash
pyinstaller --onefile emby-updater.py
```

emby-updater is licensed under MIT license.