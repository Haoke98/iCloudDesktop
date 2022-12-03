#!/usr/bin/env python3
# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/3
@Software: PyCharm
@disc:
======================================="""
import click

from lib import icloud

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS, options_metavar="<options>")
# @click.argument(
@click.option(
    "-d", "--directory",
    help="Local directory that should be used for download",
    type=click.Path(exists=True),
    metavar="<directory>")
@click.option(
    "-u", "--username",
    help="Your iCloud username or email address",
    metavar="<username>",
    prompt="iCloud username/email",
)
@click.option(
    "-p", "--password",
    help="Your iCloud password "
         "(default: use PyiCloud keyring or prompt for password)",
    metavar="<password>",
)
@click.option(
    "--recent",
    help="Number of recent photos to download (default: download all photos)",
    type=click.IntRange(0),
)
@click.version_option()
# pylint: disable-msg=too-many-arguments,too-many-statements
# pylint: disable-msg=too-many-branches,too-many-locals
def main(username, password, directory, recent):
    iService = icloud.IcloudService(username, password)
    iService.download_photo(directory, recent=recent, modify_olds=True)


if __name__ == "__main__":
    main()
