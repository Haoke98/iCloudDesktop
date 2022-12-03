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

    def __init__(self, apple_id,
                 password=None,
                 china_account=None,
                 cookie_directory=None,
                 verify=True,
                 client_id=None,
                 with_family=True, ):
        if china_account:
            self.HOME_ENDPOINT = "https://www.icloud.com.cn"
            self.SETUP_ENDPOINT = "https://setup.icloud.com.cn/setup/ws/1"
        super().__init__(apple_id, password, cookie_directory, verify, client_id, with_family)
        self.two_factor_authenticate()

    def two_factor_authenticate(self):
        if self.requires_2fa:
            logging.info("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = self.validate_2fa_code(code)
            logging.info("Code validation result: %s" % result)

            if not result:
                logging.error("Failed to verify security code")
                sys.exit(1)

            if not self.is_trusted_session:
                logging.warning("Session is not trusted. Requesting trust...")
                result = self.trust_session()
                logging.info("Session trust result %s" % result)

                if not result:
                    logging.error(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif self.requires_2sa:
            import click

            logging.info("Two-step authentication required. Your trusted devices are:")

            devices = self.trusted_devices
            for i, device in enumerate(devices):
                logging.info(
                    "  %s: %s" % (i, device.get('deviceName',
                                                "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not self.send_verification_code(device):
                logging.error("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not self.validate_verification_code(device, code):
                logging.info("Failed to verify verification code")
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
        _all = iter(self.photos.all)
        for i in range(1, recent + 1):
            photo = next(_all, None)
            con.execute(
                'INSERT OR IGNORE INTO photos(id, created, asset_date, added_date, filename,size,dimension_x,dimension_y) values (?,?,?,?,?,?,?,?)',
                (photo.id, photo.created, photo.asset_date, photo.added_date, photo.filename, photo.size,
                 photo.dimensions[0], photo.dimensions[1]))
            _ext_ = str(photo.filename).split(".")[1]
            _file_name_ = f"{photo.id.replace('/', '-')}.{_ext_}"
            raw_path = os.path.join(outputDir, _file_name_)
            if os.path.exists(raw_path):
                statinfo = os.stat(raw_path)
                if photo.size > statinfo.st_size:
                    logging.warning(f"文件[{raw_path}]已损坏,正在重新下载....")
                    __download__()
                    logging.warning(f"文件[{raw_path}]重新下载成功.")
                elif photo.size < statinfo.st_size:
                    # cur = con.execute(f"SELECT id FROM photos WHERE filename='{photo.filename}'")
                    # values = cur.fetchall()
                    # 文件名一样
                    raise Exception(
                        f"出现了同名文件[{photo.filename}],\n 已有文件：[{statinfo}], \n即将下载的文件：[{photo.id, photo.created, photo.asset_date, photo.added_date, photo.filename, photo.size, photo.dimensions}]")
                else:
                    if modify_olds:
                        __modify_create_date__()
            else:
                __download__()
            con.commit()
            logging.info(f"%0.2f%% ({i}/{recent}):{photo.id}, {photo.filename}, {raw_path}" % (i / recent * 100))
            if auto_delete:
                photo.delete()
