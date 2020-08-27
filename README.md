# emby-updater

emby-updater is a small tool to keep the [Emby media server](https://emby.media/) up to date (even including beta-versions).

## Using emby-updater

### All in one binary

Thanks to [PyInstaller](https://www.pyinstaller.org/) you can download emby-updater without to care about any dependencies, because they are inbuilt to the binary. 

Just [head over to the releases page](https://github.com/shokinn/emby-updater/releases) and download the binary.

**Currently only Ubuntu 18.04+ (amd64) is supported.**

### Python code for maximum flexibility

Do you want to control what is running on your system?  
Grab the Python code, install the dependencies and run or modify it :)

#### Setup

##### with pipx (recommended)

[Install pipx](https://github.com/pipxproject/pipx#install-pipx)

```bash
pipx install emby-updater
```

##### with pip in the user environment

```bash
sudo apt update && \
sudo apt install -y python3 python3-pip python3-apt; \
pip3 install --user emby-updater
```

##### from binary distribution

1. Go to the [latest release page](https://github.com/shokinn/emby-updater/releases/latest).
2. Download the binary distribution package to `~/Downloads`.
3. make it executable with `chmod +x ~/Downloads/emby-updater`.
4. move it to `/usr/local/sbin`.

```bash
sudo mv ~/Downloads/emby-updater /usr/local/sbin/
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

emby-updater is licensed under MIT license.