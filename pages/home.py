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
import sqlite3
import threading
import time
import tkinter as tk
from tkinter import ttk

from requests.exceptions import SSLError

from frames import ScrollableImageGrid
from lib import mock


class HomePage(tk.Frame):
    def __init__(self, master, mock_is_active: bool = False):
        super().__init__(master)
        self.master = master
        self.mock_is_active = mock_is_active
        self.username = None
        self.status_message = None
        self.progress_message = None
        self.progress_bar = None
        self.avatar_label = None
        self.main_block = None
        self.welcome_label = None
        self.image_grid = None
        self.create_widgets()

    def create_widgets(self):
        # 在主页上显示用户信息和头像
        user_block = tk.Frame(self)
        user_block.pack()

        self.welcome_label = tk.Label(user_block, text="")
        self.welcome_label.pack(side=tk.LEFT)

        tk.Button(user_block, text="注销", command=self.master.logout).pack(side=tk.LEFT)

        self.main_block = tk.Frame(self, background="black")
        self.main_block.pack(fill=tk.BOTH, expand=True)
        # 创建头像图标
        # 这里使用一个简单的示例图片代替真实的用户头像
        photo = tk.PhotoImage(file="/Users/shadikesadamu/Documents/壁纸/20231106213414735.png").subsample(4, 4)
        self.avatar_label = tk.Label(self.main_block, image=photo)
        self.avatar_label.photo = photo
        self.avatar_label.pack(expand=True, anchor="center")

        # 图床
        self.image_grid = ScrollableImageGrid(self.main_block, 11, width=600, height=590, background="black")

        # 登陆栏
        footer = tk.Frame(self)
        footer.pack(side=tk.BOTTOM)
        # 创建登录按钮
        # tk.Button(footer, text="开始同步", command=self.start_sync).pack(side=tk.LEFT)
        # tk.Button(footer, text="展示照片", command=self.show_assets).pack(side=tk.RIGHT)

        # 创建一个进度条
        self.progress_bar = ttk.Progressbar(footer, orient="horizontal", length=300, mode="determinate")
        self.status_message = tk.Label(footer)
        self.progress_message = tk.Label(footer)

    def create_menus(self):
        # 创建下拉菜单
        # menu_bar = tk.Menu(self)
        # self.config(menu=menu_bar)

        # 用户菜单
        # user_menu = tk.Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label=username, menu=user_menu)
        # user_menu.add_command(label="个人信息")
        # user_menu.add_separator()
        # user_menu.add_command(label="注销", command=lambda: self.logout())
        pass

    def show(self, username):
        self.username = username
        self.start_sync()
        self.after(1 * 60 * 60, self.show_assets)  # 延迟40秒执行
        self.welcome_label.config(text=f"欢迎回来，{username}！")
        self.pack(fill=tk.BOTH, expand=True)

    def start_sync(self):
        threading.Thread(target=self.sync).start()

    def sync(self):
        """
            同步数据
            :return:
            """
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        self.status_message.pack(pady=10, side=tk.LEFT)
        self.progress_bar.pack(pady=10, side=tk.LEFT)
        self.progress_message.pack(pady=10, side=tk.LEFT)
        iService = self.master.iService
        # for i, album_name in enumerate(iService.photos.albums):
        #     album = iService.photos.albums[album_name]
        #     print(i, album_name, len(album))
        all_photos = iService.photos.all
        total = len(all_photos)
        print(total)
        self.progress_bar["maximum"] = total
        for i, p in enumerate(all_photos):
            progress = (i + 1) / total * 100
            document = vars(p)
            # 移除'_service'字段
            document.pop('_service', None)
            # 目前只有大小字段参与排序, 所以只需把它单独拿出来存储到特定的字段中
            # TODO: 如果后期有需要可以挨个从master_record和asset_record中解析出来
            values = [
                document["_master_record"]["recordName"],
                document["_master_record"]["fields"]["resOriginalRes"]["value"]["size"],
                document["_master_record"]["fields"]["resOriginalFileType"]["value"],
                document["_master_record"]["created"]["timestamp"],
                document["_master_record"]["modified"]["timestamp"],
                json.dumps(document["_master_record"], ensure_ascii=False),
                json.dumps(document["_asset_record"], ensure_ascii=False),
            ]
            # print(f"{progress:.2f}%({i + 1}/{total})", values)
            # , p.id, p.filename, p.size, p.dimensions,
            #                   p.created,
            #                   p.asset_date,
            #                   p.added_date, p.versions
            # 插入文档
            cursor.execute(
                "INSERT OR REPLACE INTO assets (recordName, size, file_type,created,modified,master_fields, asset_fields) VALUES (?, ?, ?, ?, ?, ?, ?)",
                values)
            conn.commit()

            self.status_message.config(text="正在进行资源同步")
            self.progress_message.config(text=f"{progress:.2f}% ( {i + 1} / {total} )")
            self.progress_bar["value"] = i + 1
            self.update_idletasks()  # 更新Tkinter窗口
            if p.created != p.asset_date:
                raise Exception("异常数据")
            pass
        pass

    def show_assets(self):
        self.avatar_label.pack_forget()
        self.image_grid.pack(fill=tk.X, expand=False)
        threading.Thread(target=self.async_show).start()

    def async_show(self):
        self.image_grid.set_username(self.username)
        if self.mock_is_active:
            _mock_images = []
        else:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
        n = 1
        while True:

            if self.mock_is_active:
                try:
                    _mock_images += mock.images(1, 200, "Soft", "Most Comments")
                    rows = _mock_images
                    n += 1
                except SSLError as e:
                    logging.error("SSL Error: %s", e)
                    time.sleep(2)
                    continue

            else:
                cursor.execute(
                    "SELECT recordName, size, file_type,created,modified,master_fields, asset_fields FROM assets ORDER BY created DESC")
                rows = cursor.fetchall()
            logging.debug(f"从数据库提取图片成功!:{len(rows)}")
            self.image_grid.set_data(rows)
            time.sleep(1)
