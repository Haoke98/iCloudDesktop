# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/28
@Software: PyCharm
@disc:
======================================="""
import json
import logging
import time
import tkinter as tk
from core import init_database, PyiCloudService


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # 这里使用一个简单的示例图片代替真实的用户头像
        photo = tk.PhotoImage(file="assets/41166dada6559cb93c7a4ff0ea681e52.png").subsample(2, 2)
        avatar_label = tk.Label(self, image=photo)
        avatar_label.grid(row=0, column=0, columnspan=2)
        avatar_label.photo = photo
        # avatar_label.pack(side=tk.RIGHT)

        # 创建用户名和密码输入框
        self.username_label = tk.Label(self, text="用户名:")
        self.username_label.grid(row=2, column=0, sticky=tk.E)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=2, column=1)

        self.password_label = tk.Label(self, text="密码:")
        self.password_label.grid(row=3, column=0, sticky=tk.E)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1)

        # 显示登录结果的标签
        self.load_account_btn = tk.Button(self, text="加载账号", command=self.load_account)
        self.load_account_btn.grid(row=4, column=0, columnspan=1)

        # 创建登录按钮
        self.login_button = tk.Button(self, text="登录", command=self.login)
        self.login_button.grid(row=4, column=1, columnspan=1)

        # 显示登录结果的标签
        self.message_label = tk.Label(self, text="")
        self.message_label.grid(row=5, column=0, columnspan=2)

    def login(self, china_account: bool = True):
        username = self.username_entry.get()
        password = self.password_entry.get()
        logging.info(f"[login] username: {username}, password: [{password}]")
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

    def load_account(self):
        with open("accounts.json", "r") as f:
            accounts = json.load(f)
            for account in accounts:
                self.username_entry.insert(0, account["username"])
                self.password_entry.insert(0, account["password"])
