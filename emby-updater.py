#!/usr/bin/env python3

import argparse
import os
import re
import subprocess as sp
import sys
from pathlib import Path
from shutil import move

import requests

try:
    import apt
except ImportError:
    print("You have to install 'python3-apt' to use this script.\nE.g. 'apt install -y python3-apt'")
    sys.exit(1)


def yes_or_no(question):
    if args.yes:
        return True
    else:
        while "the answer is invalid":
            reply = input(question + ' (y/n): ').lower().strip()
            if reply[:1] == 'y':
                return True
            if reply[:1] == 'n':
                return False


def get_latest_version(releases, allow_prereleases):
    for release in releases:
        for asset in release["assets"]:
            if re.match(".*deb_.*_amd64\.deb", asset["name"]) is not None:
                if allow_prereleases or not release["prerelease"]:
                    return release
    return None


def get_asset_json(assets):
    for asset in assets:
        if re.match(".*deb_.*_amd64\.deb", asset["name"]) is not None:
            return asset
    return None


def get_emby_version(pkg_name):
    cache = apt.Cache()
    cache.open()

    try:
        cache[pkg_name].is_installed
    except KeyError:
        return None

    pkg = cache[pkg_name]
    versions = pkg.versions
    return versions[0].version


def download_package(asset):
    if Path(args.download_path + "/" + asset["name"]).is_file():
        os.remove(Path(args.download_path + "/" + asset["name"]))
    with open(Path(args.download_path + "/" + asset["name"]), "wb") as f:
        print(f'Downloading {asset["name"]}')
        r = requests.get(asset["browser_download_url"], stream=True)
        total_length = r.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(r.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in r.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()


def upgrade():
    releases_json = requests.get("https://api.github.com/repos/shokinn/emby-updater/releases").json()
    release_json = get_latest_version(releases_json, False)
    if release_json is None:
        print("Could not find any releases.")
        sys.exit(1)

    if release_json["tag_name"] > eu_version:
        print(f'''There is an update available
Installed version:    {eu_version}
Update version:       {release_json["name"]}''')
        if not yes_or_no("Do you want to update?"):
            print('Update process aborted.', file=sys.stderr)
            sys.exit(1)

        asset_json = get_asset_json(release_json["assets"])
        download_package(asset_json)
        script_path = os.path.dirname(os.path.realpath(__file__))
        script_file = Path(__file__)
        move(args.download_path + "/" + asset_json["name"], f"{script_path}" + "/" + f"{script_file}")
        os.chmod(f"{script_path}" + "/" + f"{script_file}", 0o774)

        print("emby-updater tool successful updated.")
        sys.exit(0)
    else:
        print("No update available.")
        sys.exit(0)


def main(allow_prereleases):
    releases_json = requests.get("https://api.github.com/repos/MediaBrowser/Emby.Releases/releases").json()
    release_json = get_latest_version(releases_json, allow_prereleases)
    if release_json is None:
        print("Could not find any releases.")
        sys.exit(1)

    emby_version = get_emby_version("emby-server")

    if emby_version is None or release_json["tag_name"] > emby_version:
        if emby_version is None:
            if not yes_or_no(
                    f'Emby media server is not installed.\nDo you want to install Emby ({release_json["name"]})?'):
                print('Installation of Emby media server aborted.', file=sys.stderr)
                sys.exit(1)
        else:
            print(f'''There is an update available
Installed version:    {emby_version}
Update version:       {release_json["name"]}''')
            if not yes_or_no("Do you want to update?"):
                print('Update process aborted.', file=sys.stderr)
                sys.exit(1)

        asset_json = get_asset_json(release_json["assets"])
        download_package(asset_json)
        if emby_version is not None:
            sp.call(["systemctl", "stop", "emby-server.service"])
        deb_file = args.download_path + "/" + asset_json["name"]
        sp.call(["sudo", "dpkg", "-i", f"{deb_file}"])
        os.remove(deb_file)

        if not yes_or_no("Do you want to keep Emby Media server running?"):
            sp.call(["systemctl", "stop", "emby-server.service"])
            print("Emby media server stopped.")

        if not yes_or_no("Do you want to keep the service enabled?"):
            sp.call(["systemctl", "disable", "emby-server.service"])
            print("Emby media server service disabled.")

        print("Emby update successful installed.")
        sys.exit(0)
    else:
        print("No update available.")
        sys.exit(0)


if __name__ == '__main__':
    if os.geteuid() != 0:
        print('''You need to have root privileges to run this script.
Please try again, this time using 'sudo'.
Exiting.''', file=sys.stderr)
        sys.exit(1)

    eu_version = "0.7.0"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='emby-updater will help you to install Emby (updates) easily.',
        epilog='''This is an unofficial update tool for the Emby media server.
It's not supported through any official Emby Support.
emby-updater is proudly presented by Philip 'ShokiNN' Henning <mail@philip-henning.com>.''')
    parser.add_argument('--beta', help='installs Emby beta versions', action='store_true')
    parser.add_argument('-d', '--download-path', help='Set path for downloaded binaries', default='/tmp',
                        action='store')
    parser.add_argument('--update', help='update the script itself if an update is available', action='store_true')
    parser.add_argument('--version', action='version', version=f'%(prog)s {eu_version}')
    parser.add_argument('-y', '--yes',
                        help='automatic yes to prompts. Assume "yes" as answer to all prompts and run '
                             'non-interactively. If an undesirable situation, such as changing a held package or '
                             'removing an essential package, occurs then %(prog)s will abort.',
                        action='store_true')
    args = parser.parse_args()

    if args.update:
        upgrade()
    else:
        main(args.beta)
