import argparse
import os
import re
import subprocess as sp
import sys
from pathlib import Path
from shutil import move

import requests
from . import version

try:
    import apt
except ImportError:
    sys.exit("You have to install 'python3-apt' to use this script.\nE.g. 'apt install -y python3-apt'")


def yes_or_no(question, quiet):
    if quiet:
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
            if allow_prereleases and release["prerelease"]:
                if re.match(".*deb_.*_amd64\.deb", asset["name"]) is not None:
                    return release
            elif not allow_prereleases and not release["prerelease"]:
                if re.match(".*deb_.*_amd64\.deb", asset["name"]) is not None:
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


def download_package(asset, download_path):
    if Path(download_path + "/" + asset["name"]).is_file():
        os.remove(Path(download_path + "/" + asset["name"]))
    with open(Path(download_path + "/" + asset["name"]), "wb") as f:
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


def self_update(download_path, quiet):
    if getattr(sys, 'frozen', False):
        releases_json = requests.get("https://api.github.com/repos/shokinn/emby-updater/releases").json()
        release_json = None
        for release in releases_json:
            for asset in release["assets"]:
                if re.match("emby-updater", asset["name"]) is not None:
                    if not release["prerelease"]:
                        release_json = release
                        break
            else:
                continue
            break

        if release_json is None:
            print("Could not find any releases.")
            sys.exit(1)
        elif release_json["tag_name"] > version.version:
            print(f'''There is an update available
Installed version:    {version.version}
Update version:       {release_json["tag_name"]} ({release_json["name"]})''')
            if not yes_or_no("Do you want to update?", quiet):
                print('Update process aborted.', file=sys.stderr)
                sys.exit(1)

            asset_json = get_asset_json(release_json["assets"])
            download_package(asset_json, download_path)
            script_path = os.path.dirname(os.path.realpath(__file__))
            script_file = Path(__file__)
            move(download_path + "/" + asset_json["name"], f"{script_path}" + "/" + f"{script_file}")
            os.chmod(f"{script_path}" + "/" + f"{script_file}", 0o774)

            print("emby-updater tool successful updated.")
            sys.exit(0)
        else:
            print(f'''
NO UPDATE AVAILABLE!
Installed version:    {version.version}
Available version:    {release_json["tag_name"]} ({release_json["name"]})''')
            sys.exit(0)
    else:
        print('''You're using the script version of emby-updater.
Please update with your python package manager of choice (some examples below):
    - pipx (recommended):
        `pipx upgrade emby-updater`
        
    - pip:
        `pip install --user --upgrade emby-updater`''')
        sys.exit(0)


def updater(allow_prereleases, download_path, quiet):
    releases_json = requests.get("https://api.github.com/repos/MediaBrowser/Emby.Releases/releases").json()
    release_json = get_latest_version(releases_json, allow_prereleases)
    if release_json is None:
        sys.exit("Could not find any releases.")

    emby_version = get_emby_version("emby-server")

    if emby_version is None or release_json["tag_name"] > emby_version:
        if emby_version is None:
            if not yes_or_no(
                    f'Emby media server is not installed.\nDo you want to install Emby ({release_json["name"]})?', quiet):
                print('Installation of Emby media server aborted.', file=sys.stderr)
                sys.exit(1)
        else:
            if not allow_prereleases:
                print(f'''There is an update available
Installed version:    {emby_version}
Available version:    {release_json["tag_name"]}''')
                if not yes_or_no("Do you want to update?", quiet):
                    print('Update process aborted.', file=sys.stderr)
                    sys.exit(1)
            elif allow_prereleases:
                print(f'''There is an update available
Installed version:    {emby_version}
Available version:    {release_json["tag_name"]} (beta release)''')
                if not yes_or_no("Do you want to update?", quiet):
                    print('Update process aborted.', file=sys.stderr)
                    sys.exit(1)

        asset_json = get_asset_json(release_json["assets"])
        download_package(asset_json, download_path)
        if emby_version is not None:
            sp.call(["systemctl", "stop", "emby-server.service"])
        deb_file = download_path + "/" + asset_json["name"]
        sp.call(["dpkg", "-i", f"{deb_file}"])
        os.remove(deb_file)

        if not yes_or_no("Do you want to keep Emby Media server running?", quiet):
            sp.call(["systemctl", "stop", "emby-server.service"])
            print("Emby media server stopped.")

        if not yes_or_no("Do you want to keep the service enabled?", quiet):
            sp.call(["systemctl", "disable", "emby-server.service"])
            print("Emby media server service disabled.")

        print("Emby update successful installed.")
        sys.exit(0)
    else:
        if not allow_prereleases:
            print(f'''
NO UPDATE AVAILABLE!
Installed version:    {emby_version}
Available version:    {release_json["tag_name"]}''')
        elif allow_prereleases:
            print(f'''
NO UPDATE AVAILABLE!
Installed version:    {emby_version}
Available version:    {release_json["tag_name"]} (beta release)''')

        sys.exit(0)


def main():
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
    parser.add_argument('--version', action='version', version=f'%(prog)s {version.version}')
    parser.add_argument('-y', '--yes',
                        help='automatic yes to prompts. Assume "yes" as answer to all prompts and run '
                             'non-interactively. If an undesirable situation, such as changing a held package or '
                             'removing an essential package, occurs then %(prog)s will abort.',
                        action='store_true')
    args = parser.parse_args()

    if os.geteuid() != 0:
        print('''
##########
# You need to have root privileges to run this script.
# Please try again, this time using 'sudo'.
##########

''', file=sys.stderr)
        parser.print_help()
        print('''
Exiting.''', file=sys.stderr)
        sys.exit(1)

    if args.update:
        self_update(args.download_path, args.yes)
    else:
        updater(args.beta, args.download_path, args.yes)


