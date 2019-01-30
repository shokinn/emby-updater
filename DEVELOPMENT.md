# Development commands and notes

## Setup dev environment

```bash
sudo apt update && \
sudo apt install -y python3 python3-pip python3-apt python3-dev git build-essential; \
git clone https://github.com/shokinn/emby-updater.git && \
cd emby-updater && \
pip3 install --user -r requirements.txt && \
pip3 install --user setuptools && \
pip3 install --user pyinstaller && \
pip3 install --user wheel && \
pip3 install --user twine && \
pip3 install --user bumpversion && \
export PATH=$HOME/.local/bin:$PATH
```

## Release new version

To publish a release use bumpversion. This will update the `version.py` and tag the commit.
Travis will then push the new release to [PyPi](https://pypi.python.org/pypi/emby-updater).

```bash
./release.sh <patch|minor|major>
``` 

## Manual steps
