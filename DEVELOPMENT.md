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

After building the binary it has to be released manually on github.

## Manual steps

These steps assumes that you are in the cloned directory

```bash
bumpversion --tag --commit <patch|minor|major>

git add .bumpversion.cfg
git add embyupdater/version.py
git commit --amend --no-edit

#git commit -m "v$(cat .bumpversion.cfg|grep current_version|tr -d ' '|cut -f 2 -d '=')""

git push --tag

python3 setup.py sdist bdist_wheel

twine upload dist/*

pyinstaller --clean --onefile --name emby-updater --distpath pyindist --workpath pyinbuild embyupdater/__main__.py
```

After building the binary it has to be released manually on github.