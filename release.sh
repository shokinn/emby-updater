#! /bin/bash
set -ex

args=""
if [[ $# == 0 ]]; then
    args="patch"
else
    args=$*
fi

echo "Pull changes"
git pull -r

#echo "Run tests"
#./setup.py test

echo "Bump version"
#Bump version
bumpversion --tag --commit $args

echo "Add version changes to commit"
git add .bumpversion.cfg
git add embyupdater/version.py
git commit --amend --no-edit

#seperate commit with version in comment
#git commit -m "v$(cat .bumpversion.cfg|grep current_version|tr -d ' '|cut -f 2 -d '=')""

echo "Push to git"
git push --tag

echo "Build distribution files"
python3 setup.py sdist bdist_wheel

echo "upload to PyPI"
twine upload dist/*

# Deprecated
# echo "Build binary package"
# pyinstaller --clean --onefile --name emby-updater --distpath pyindist --workpath pyinbuild embyupdater/__main__.py