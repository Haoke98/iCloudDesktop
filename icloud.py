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
from prettytable import PrettyTable

from lib import icloud, logger


@click.group()
@click.option(
    "-u", "--username",
    help="Your iCloud username or email address",
    metavar="<username>",
    prompt="iCloud username(mobile/email)",
    required=True
)
@click.option(
    "-p", "--password",
    help="Your iCloud password "
         "(default: use PyiCloud keyring or prompt for password)",
    metavar="<password>",
    prompt="iCloud password",
    required=True
)
@click.option(
    "--china-account",
    help='Specify the "HOME_ENDPOINT" and "SETUP_ENDPOINT" for the "China Mainland Accounts". ',
    is_flag=True,
    prompt="isChinaAccount?"
)
@click.version_option()
def main(username, password, china_account):
    global iService
    logging.info(f"CHINA_ACCOUNT:{china_account}")
    iService = icloud.IcloudService(username, password, china_account)


@main.command(options_metavar="<options>",
              help="Manage Photos on your icloud. (Transform Album, Download recent photos.)")
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
    iService.download_photo(directory, recent=recent, transfer_album=transfer_album, modify_olds=modify_olds,
                            auto_delete=auto_delete,
                            max_thread_count=workers)


@main.command(options_metavar="<options>",
              help="Device and Location, Find device Location, Get device Status, Show message on device, Remote lock device.")
def device():
    table = PrettyTable()
    table.field_names = ["序号", "设备名称", "型号", "探索ID", "状态", "能否获取位置信息？", "是否可以在锁定后擦除？", "是否已开启家人分享?", "能否标记为丢失？", "电池水平",
                         "丢失时间", "ID"]
    devices = iService.devices
    for i, device in enumerate(devices):
        data = device.data
        table.add_row(
            [i, data.get("name"), data.get("deviceModel"), data.get("deviceDiscoveryId"), data.get("deviceStatus"),
             data.get("locationEnabled"), data.get("canWipeAfterLock"), data.get("fmlyShare"),
             data.get("lostModeCapable"), data.get("batteryLevel"), data.get("lostTimeStamp"), data.get("id")])
        pass
    print(table)
    while True:
        i = click.prompt('Which device would you like to use?', type=int, default=0)
        row = table._rows[i]
        device_id = row[-1]
        device = devices[device_id]
        print("CurrentStatus：", device.status())
        print("CurrentLocation：", device.location())
        isOk = click.prompt("Do you want to show some message on your device?", type=bool, default=False)
        if isOk:
            msg = click.prompt("Please input some message here.", default="Don't do anything on my device.")
            device.display_message(message=msg)
            print("Its Done@!")


@main.command(options_metavar="<options>", help="Do some experimental tes.")
def test():
    global iService
    for i, album_name in enumerate(iService.photos.albums):
        album = iService.photos.albums[album_name]
        print(i, album_name, len(album))
    all_photos = iService.photos.all
    print(len(all_photos))
    for i, p in enumerate(all_photos):
        print(i, p.id, p.filename, p.size, p.dimensions, p.created, p.asset_date, p.added_date, p.versions)
        if p.created != p.asset_date:
            raise Exception("异常数据")
        pass


if __name__ == "__main__":
    logger.init("icloud", console_level=logging.INFO)
    main()
