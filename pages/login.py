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
from tkinter import font as tkFont
from core import PyiCloudService


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.message_label = None
        self.login_button = None
        self.load_account_btn = None
        self.password_entry = None
        self.password_label = None
        self.username_entry = None
        self.username_label = None
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # 创建Logo
        photo = tk.PhotoImage(file="assets/41166dada6559cb93c7a4ff0ea681e52.png").subsample(2, 2)
        logo_label = tk.Label(self, image=photo, background="white")
        logo_label.photo = photo
        logo_label.pack()

        # 设置字体
        custom_font = tkFont.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(self, text="iCloud", font=custom_font, foreground="white")
        title_label.pack(side=tk.TOP)

        # 创建用户名和密码输入框
        username_frame = tk.Frame(self)
        username_frame.pack()
        self.username_label = tk.Label(username_frame, text="用户名:")
        self.username_label.pack(side=tk.LEFT)
        self.username_entry = tk.Entry(username_frame)
        self.username_entry.pack(side=tk.RIGHT)

        password_frame = tk.Frame(self)
        password_frame.pack()
        self.password_label = tk.Label(password_frame, text="密   码:")
        self.password_label.pack(side=tk.LEFT)
        self.password_entry = tk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.RIGHT)

        # 创建加载账号按钮和登录按钮
        button_frame = tk.Frame(self)
        button_frame.pack()
        self.load_account_btn = tk.Button(button_frame, text="加载账号", command=self.load_account)
        self.load_account_btn.pack(side=tk.LEFT)
        self.login_button = tk.Button(button_frame, text="登录", command=self.login)
        self.login_button.pack(side=tk.LEFT)

        # 显示登录结果的标签
        self.message_label = tk.Label(self, text="")
        self.message_label.pack()

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
