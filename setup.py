#!/usr/bin/env python3

from setuptools import setup
from embyupdater import version


def readme():
    with open("README.md") as fd:
        return fd.read()


setup(
    name="emby-updater",
    version=version.version,
    url="https://github.com/shokinn/emby-updater",
    license="MIT",
    author="Philip Henning",
    author_email="mail@philip-henning.com",
    description="A little tool to keep your emby media server up to date.",
    long_description_content_type="text/markdown",
    long_description=readme(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities"
    ],
    keywords=["emby", "updater", "ubuntu"],
    packages=["embyupdater", ],
    entry_points={"console_scripts": ["emby-updater=embyupdater:main", ]},
    install_requires=["requests~=2.20", ],
    python_requires="~=3.6"
)
