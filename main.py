# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/27
@Software: PyCharm
@disc:
======================================="""
import logging
import tkinter as tk

from core import init_database
from lib import logger
from pages import HomePage, LoginPage

iService = None


class PyICloudClient(tk.Tk):

    def __init__(self):
        # 创建主窗口
        super().__init__()
        self.iService = None
        self.page_home = HomePage(self)
        self.page_login = LoginPage(self)
        self.title("PyICloudClient")

        init_database()
        self.reset_size(300, 400)
        self.title("PyICloudClient | 登陆页")
        self.page_login.pack(expand=True, fill=tk.BOTH)

    def reset_size(self, width: int, height: int):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_homepage(self, username):
        self.page_login.pack_forget()  # 隐藏登录页面
        self.page_home.show(username)
        # 创建主页窗口
        self.reset_size(1200, 600)
        self.title("PyICloudClient | 登陆页")

    def logout(self):
        self.page_home.destroy()  # 关闭主页窗口
        self.ctx.deiconify()  # 显示登录窗口


if __name__ == '__main__':
    logger.init("icloud", console_level=logging.INFO)
    app = PyICloudClient()
    app.mainloop()
