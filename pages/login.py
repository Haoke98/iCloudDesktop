# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/28
@Software: PyCharm
@disc:
======================================="""
import logging
import sqlite3
import threading
import time
import tkinter as tk
from tkinter import font as tkFont

from core import PyiCloudService


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.update_view_th = None
        self.title_label = None
        self.users = None
        self.message_label = None
        self.login_button = None
        self.load_account_btn = None
        self.password_entry = None
        self.password_label = None
        self.username_entry = None
        self.username_label = None
        self.remember_password = tk.BooleanVar()
        self.remember_password.set(False)
        self.master = master
        self.create_widgets()
        self.login_processing = False  # 登陆正在进行
        self.login_start_at = None  # 登陆开始

        self._stop_event = threading.Event()

    def create_widgets(self):
        # 创建Logo
        photo = tk.PhotoImage(file="assets/41166dada6559cb93c7a4ff0ea681e52.png").subsample(2, 2)
        logo_label = tk.Label(self, image=photo, background="white")
        logo_label.photo = photo
        logo_label.pack()

        # 设置字体
        custom_font = tkFont.Font(family="Arial", size=24, weight="bold")
        self.title_label = tk.Label(self, text="iCloud", font=custom_font, foreground="white")
        self.title_label.pack(side=tk.TOP)

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

        self.load_account_btn = tk.Button(button_frame, text="加载已存账号", command=self.load_account)

        self.master.db_cursor.execute("SELECT username,password FROM users;")
        self.users = self.master.db_cursor.fetchall()
        if len(self.users) > 0:
            self.load_account_btn.pack(side=tk.LEFT)

        tk.Checkbutton(button_frame, text="记住密码", variable=self.remember_password).pack(side=tk.LEFT)

        self.login_button = tk.Button(button_frame, text="登录", command=self.login)
        self.login_button.pack(side=tk.LEFT)

        # 显示登录结果的标签
        self.message_label = tk.Label(self, text="")
        self.message_label.pack()

    def async_update_view(self):
        while not self._stop_event.is_set():
            if self.login_processing:
                dlt = time.time() - self.login_start_at
                self.message_label.config(text=f"正在登陆...{dlt:0.0f}s")
                # 设置登陆超时
                max_dlt = 60 * 60 * 60
                compare_result = dlt > max_dlt
                # logging.debug(f"正在登陆.....{dlt}s, 超时:{compare_result}")
        self.message_label.config(text="")

    def show(self):
        self.update_view_th = threading.Thread(target=self.async_update_view)
        self.update_view_th.start()
        self.pack(expand=True, fill=tk.BOTH)

    def pack_forget(self):
        self._stop_event.set()
        super().pack_forget()

    def login(self):
        threading.Thread(target=self.async_login).start()

    def async_login(self, china_account: bool = True):
        self.login_start_at = time.time()
        self.login_processing = True
        username = self.username_entry.get()
        password = self.password_entry.get()
        logging.info(f"[login] username: {username}, password: [{password}]")
        logging.info(f"CHINA_ACCOUNT:{china_account}")
        self.master.iService = PyiCloudService(self.master, username, password, china_account)
        while True:
            dlt = time.time() - self.login_start_at
            if self.master.iService.account.devices:
                print("登陆成功!")
                if self.remember_password.get():
                    # 如果用户勾选了记住密码, 则就保存密码
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)",
                                   (username, password))
                    conn.commit()
                break
            else:
                print("还未登陆...")
                time.sleep(1)
            # 设置登陆超时
            max_dlt = 60 * 60 * 60
            compare_result = dlt > max_dlt
            print(f"正在登陆.....{dlt}s, 超时:{compare_result}")
            if compare_result:
                self.message_label.config(text="登陆超时")

        # 最终
        self.master.show_homepage(username)

    def load_account(self):
        for user in self.users:
            print(user)
            self.username_entry.delete(0, tk.END)  # 删除旧文本
            self.username_entry.insert(0, user[0])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, user[1])
