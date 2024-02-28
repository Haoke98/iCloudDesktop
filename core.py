# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/27
@Software: PyCharm
@disc:
======================================="""
import logging
import sqlite3
import tkinter.messagebox

from PIL import Image
from lib.icloud import IcloudService as __iCloudService__
from tkinter import simpledialog

images = [
    "/Users/shadikesadamu/Documents/壁纸/20230731161643225.jpg",
    "/Users/shadikesadamu/Documents/壁纸/20230731163829912.png",
    "/Users/shadikesadamu/Documents/壁纸/20230731164217189.jpg",
    "/Users/shadikesadamu/Documents/壁纸/20231106201443283.jpg",
    "/Users/shadikesadamu/Documents/壁纸/20231106213414735.png"]


class PyiCloudService(__iCloudService__):
    COMPLETED_OF_DOWNLOAD_PHOTO = 0

    def __init__(self, tk_ctx, apple_id,
                 password=None,
                 china_account=None,
                 cookie_directory=None,
                 verify=True,
                 client_id=None,
                 with_family=True, ):
        self.tk_ctx = tk_ctx
        if china_account:
            self.HOME_ENDPOINT = "https://www.icloud.com.cn"
            self.SETUP_ENDPOINT = "https://setup.icloud.com.cn/setup/ws/1"
        print(apple_id, password)
        super().__init__(apple_id, password, china_account, cookie_directory, verify, client_id, with_family)
        self.two_factor_authenticate()

    def two_factor_authenticate(self):
        if self.requires_2fa:
            logging.warning("Two-factor authentication required.")
            # 第一步：向用户请求输入第一个验证代码 (由于tk的线程不安全性, 必须在主线程上运行, 所以需要用线程通信和间接触发的形式转交给主线程处理)
            # 使用主线程的方法来获取用户输入
            self.tk_ctx.event_generate('<<Request2FA>>', when="tail")
            # 等待用户输入的结果
            verification_code = self.tk_ctx.authCodeQueue.get()  # This will block until the item is available
            logging.info("Verification Code: {}".format(verification_code))
            result = self.validate_2fa_code(verification_code)
            logging.info("Code validation result: %s" % result)

            if not result:
                logging.error("Failed to verify security code.")
                tkinter.messagebox.showinfo("Two Factor Authentication", "Failed to verify security code.")

            if not self.is_trusted_session:
                logging.warning("Session is not trusted. Requesting trust...")
                result = self.trust_session()
                logging.info("Session trust result %s" % result)
                tkinter.messagebox.showinfo("Two Factor Authentication", "Session trust result %s." % result)

                if not result:
                    logging.error(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks")
                    tkinter.messagebox.showinfo("Two Factor Authentication",
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

            code = click.prompt('Please enter validation code')
            if not self.validate_verification_code(device, code):
                logging.info("Failed to verify verification code")


def load_images():
    # 使用PIL库加载图片
    res = []
    for img_path in images:
        res.append(Image.open(img_path).convert("RGB").resize((100, 100)))
    return res


def sync(ctx):
    """
    同步数据
    :return:
    """
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
    pass


def login(ctx, username, password):
    pass


def init_database():
    # 连接到数据库（如果不存在则会创建）
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    # 创建用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT unique , password TEXT)''')

    # 删除旧表格（如果存在）
    c.execute('''DROP TABLE IF EXISTS assets''')
    # 创建媒体资源表
    c.execute('''CREATE TABLE assets
                                      (
                                        recordName TEXT PRIMARY KEY, 
                                        master_fields TEXT,
                                        asset_fields TEXT,
                                        size INTEGER,
                                        file_type TEXT,
                                        created INTEGER,
                                        modified INTEGER
                                        )
                                      ''')
    # 添加索引
    c.execute('''CREATE INDEX IF NOT EXISTS size_index ON assets (size)''')
    c.execute('''CREATE INDEX IF NOT EXISTS file_type_index ON assets (file_type)''')
    c.execute('''CREATE INDEX IF NOT EXISTS created_time_index ON assets (created)''')
    c.execute('''CREATE INDEX IF NOT EXISTS modified_time_index ON assets (modified)''')
    return conn, c
