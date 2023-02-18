#!/usr/bin/env python3
# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/3
@Software: PyCharm
@disc:
======================================="""
import logging

import click

from lib import icloud, logger


@click.group()
@click.option(
    "-u", "--username",
    help="Your iCloud username or email address",
    metavar="<username>",
    prompt="iCloud username/email",
    required=True
)
@click.option(
    "-p", "--password",
    help="Your iCloud password "
         "(default: use PyiCloud keyring or prompt for password)",
    metavar="<password>",
    required=True
)
@click.option(
    "--china-account",
    help='Specify the "HOME_ENDPOINT" and "SETUP_ENDPOINT" for the "China Mainland Accounts". ',
    is_flag=True,
)
@click.version_option()
def main(username, password, china_account):
    global iService
    logging.info(f"CHINA_ACCOUNT:{china_account}")
    iService = icloud.IcloudService(username, password, china_account)


@main.command(options_metavar="<options>")
@click.option(
    "-d", "--directory",
    help="Local directory that should be used for download",
    type=click.Path(exists=True),
    metavar="<directory>")
@click.option(
    "--recent",
    help="Number of recent photos to download (default: download all photos)",
    type=click.IntRange(0),
)
@click.option(
    "--auto-delete",
    help='Scans the "Recently Deleted" folder and deletes any files found in there. '
         + "(If you restore the photo in iCloud, it will be downloaded again.)",
    is_flag=True,
)
@click.option(
    "--modify-olds",
    help='Modify the "Created Time" of the old files that already been in the folder.',
    is_flag=True,
)
@click.option(
    "--workers",
    help="Number of the thread to download photo.(Default is 3)",
    type=click.IntRange(1),
)
@click.option(
    "--transfer-album",
    help="Determine the album that will be downloaded.",
    metavar="<album_name>"
)
# pylint: disable-msg=too-many-arguments,too-many-statements
# pylint: disable-msg=too-many-branches,too-many-locals
def photo_download(directory, transfer_album, recent, auto_delete, modify_olds, workers):
    global iService
    logging.info(f"PHOTO DOWNLOAD DIRECTORY:[{directory}]")
    logging.info(f"TRANSFER ALBUM:[{transfer_album}]")
    logging.info(f"RECENT:{recent}")
    logging.info(f"AUTO_DELETE: {auto_delete}")
    logging.info(f"MODIFY_OLDS: {modify_olds}")
    iService.download_photo(directory, recent=recent, transfer_album=transfer_album, modify_olds=modify_olds, auto_delete=auto_delete,
                            max_thread_count=workers)


if __name__ == "__main__":
    logger.init("icloud")
    main()
