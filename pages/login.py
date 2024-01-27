# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/28
@Software: PyCharm
@disc:
======================================="""
import logging
import time
import tkinter as tk
from core import init_database, PyiCloudService


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # 创建用户名和密码输入框
        self.username_label = tk.Label(self, text="用户名:")
        self.username_label.grid(row=0, column=0, sticky=tk.E)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self, text="密码:")
        self.password_label.grid(row=1, column=0, sticky=tk.E)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        # 创建登录按钮
        self.login_button = tk.Button(self, text="登录", command=self.login)
        self.login_button.grid(columnspan=2)

        # 显示登录结果的标签
        self.message_label = tk.Label(self, text="")
        self.message_label.grid(columnspan=2)

    def login(self, china_account: bool = True):
        username = self.username_entry.get()
        password = self.password_entry.get()

        logging.info(f"CHINA_ACCOUNT:{china_account}")
        self.master.iService = PyiCloudService(self.master, username, password, china_account)
        while True:
            if self.master.iService.account.devices:
                print("登陆成功!")
                self.master.show_homepage(username)
                break
            else:
                print("还未登陆...")
                time.sleep(2)
