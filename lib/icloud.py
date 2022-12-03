# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/3
@Software: PyCharm
@disc:
======================================="""
import logging
import os
import sqlite3
import sys
from subprocess import call

from pyicloud import PyiCloudService as __iCloudService__


class IcloudService(__iCloudService__):
    HOME_ENDPOINT = "https://www.icloud.com.cn"
    SETUP_ENDPOINT = "https://setup.icloud.com.cn/setup/ws/1"

    def __init__(self, apple_id,
                 password=None,
                 cookie_directory=None,
                 verify=True,
                 client_id=None,
                 with_family=True, ):
        super().__init__(apple_id, password, cookie_directory, verify, client_id, with_family)
        self.two_factor_authenticate()

    def two_factor_authenticate(self):
        if self.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = self.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

            if not self.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = self.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif self.requires_2sa:
            import click

            print("Two-step authentication required. Your trusted devices are:")

            devices = self.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s" % (i, device.get('deviceName',
                                                "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not self.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not self.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)

    def download_photo(self, outputDir: str = "./Photos", recent: int = 10, auto_delete: bool = False,
                       modify_olds: bool = False):
        def __modify_create_date__():
            createdTimeStr = photo.created.strftime("%m/%d/%Y %H:%M:%S")
            command = f'SetFile -d "{createdTimeStr}" {raw_path}'
            call(command, shell=True)

        def __download__():
            download = photo.download()
            with open(raw_path, 'wb') as opened_file:
                opened_file.write(download.raw.read())

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        con = sqlite3.connect(os.path.join(outputDir, 'info.db'))
        try:
            resp = con.execute(
                'create table photos(id varchar(255) primary key, created timestamp , asset_date timestamp , added_date timestamp ,filename varchar(255), size integer, dimension_x integer, dimension_y integer )')
        except Exception as e:
            logging.info(e)
        c = con.cursor()
        _all = iter(self.photos.all)
        for i in range(1, recent + 1):
            photo = next(_all, None)
            res = c.execute("""INSERT INTO photos(id, created, asset_date, added_date, filename,size,dimension_x,dimension_y) values (?,?,?,?,?,?,?,?)
                            ON CONFLICT (id) DO NOTHING""",
                            (photo.id, photo.created, photo.asset_date, photo.added_date, photo.filename, photo.size,
                             photo.dimensions[0], photo.dimensions[1]))

            raw_path = os.path.join(outputDir, photo.filename)
            if os.path.exists(raw_path):
                statinfo = os.stat(raw_path)
                if statinfo.st_size != photo.size:
                    # 文件名一样
                    raise Exception(
                        f"出现了同名文件[{photo.filename}],\n 已有文件：[{statinfo}], \n即将下载的文件：[{photo.id, photo.created, photo.asset_date, photo.added_date, photo.filename, photo.size, photo.dimensions[0], photo.dimensions[1]}]")
                else:
                    if modify_olds:
                        __modify_create_date__()
            else:
                __download__()
            if auto_delete:
                photo.delete()
            con.commit()
            print(f"%0.2f%% ({i}/{recent}):{photo.filename}" % (i / recent * 100))
