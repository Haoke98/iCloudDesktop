# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/27
@Software: PyCharm
@disc:
======================================="""
import logging
import queue
import tkinter as tk
from tkinter import simpledialog

import click

from core import init_database
from lib import logger
from pages import HomePage, LoginPage

iService = None

MOCK_ACTIVE = False
MOCK_USERNAME = "demo@mock.com"


class PyICloudClient(tk.Tk):

    def __init__(self):
        # 创建主窗口
        super().__init__()
        self.iService = None
        self.db_conn, self.db_cursor = init_database()
        self.authCodeQueue = queue.Queue()

        # 绑定到主窗口中的某处初始化代码，比如__init__
        self.bind('<<Request2FA>>', lambda e: self.handle_2fa_request())
        self.page_home = HomePage(self, MOCK_ACTIVE)
        self.page_login = LoginPage(self)
        self.title("PyICloudClient")
        self.show_login_page()

    def reset_size(self, width: int, height: int):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_login_page(self):
        """
        显示登录页
        """
        self.page_home.pack_forget()  # 隐藏主页面
        self.reset_size(300, 400)
        self.title("PyICloudClient | 登陆页")
        self.page_login.show()

    def show_homepage(self, username):
        """
        显示主页
        :param username:用户名
        """
        self.page_login.pack_forget()  # 隐藏登录页面
        if MOCK_ACTIVE:
            username = MOCK_USERNAME
        self.page_home.show(username)
        self.reset_size(1200, 700)
        self.title("PyICloudClient | 登陆页")

    def logout(self):
        self.page_home.pack_forget()  # 关闭主页窗口
        self.show_login_page()

    def handle_2fa_request(self):
        """
        两步验证处理方法(由于tk的线程不安全性, 必须在主线程上运行)
        :return:
        """
        verification_code = simpledialog.askstring("Two Factor Authentication", "Enter Verification Code:")
        logging.info("Verification Code: {}".format(verification_code))
        self.authCodeQueue.put(verification_code)  # Put the user input back into the queue


@click.command()
@click.option("--mock", is_flag=True, default=False, help="Open the mock mode.")
def main(mock: bool):
    global MOCK_ACTIVE
    MOCK_ACTIVE = mock
    app = PyICloudClient()
    app.mainloop()


if __name__ == '__main__':
    logger.init("icloud", console_level=logging.INFO)
    main()
