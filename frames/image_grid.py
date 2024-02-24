# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/22
@Software: PyCharm
@disc:
======================================="""
import datetime
import json
import logging
import os.path
import threading
import time
import tkinter as tk

import requests
from PIL import Image, ImageTk, UnidentifiedImageError

from lib.mock import mock_images
from lib import export_frame

MOCK_ACTIVE = True


class ScrollableImageGrid(tk.Frame):
    def __init__(self, master, column_num, width=800, height=600, cnf={}, **kw):
        tk.Frame.__init__(self, master, width=width, height=height, cnf=cnf, **kw)

        self.labels = []
        self.canvas = tk.Canvas(self, width=width, height=height, background="black")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, background="black")

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.assets = []
        self.master = master
        self.cols = column_num
        # self.create_widgets()
        self.assets_caches = {}
        self.default_img = tk.PhotoImage(
            file="/Users/shadikesadamu/Projects/icloud-killer/assets/1c11f0fa22d4e93f8dc179b8ff84791d.png").subsample(4,
                                                                                                                      4)

        threading.Thread(target=self.cache_assets_thumb).start()
        threading.Thread(target=self.update_labels).start()

    def create_widgets(self):
        pass

    def _add_label(self, i: int, img: ImageTk.PhotoImage):
        r = int(i / self.cols)
        c = int(i % self.cols)
        if i < self.labels.__len__():
            label = self.labels[i]
            logging.debug("Optimized label (row=%d, col=%d)", r, c)
            label.config(image=img)
            label.image = img
        else:
            logging.debug("Adding label (row=%d, col=%d)", r, c)
            label = tk.Label(self.scrollable_frame, image=img, background="black")
            label.image = img
            label.grid(row=r, column=c, sticky="nsew")
            self.labels.append(label)

    def set_data(self, assets: list[slice]):
        self.assets = assets

    def cache_assets_thumb(self):
        createdAt = datetime.datetime.now()
        if MOCK_ACTIVE:
            _mock_images = mock_images("Soft", 1, 200, )
        while True:
            dlt = datetime.datetime.now() - createdAt
            if len(self.assets) == 0:
                logging.info("Waiting for assets to be set[{}]....{}".format(len(self.assets), dlt))
                time.sleep(2)
            else:
                for i, asset_info in enumerate(self.assets):
                    recordName, size, file_type, created, modified, master_record_str, asset_record_str = asset_info
                    if not self.assets_caches.__contains__(recordName):
                        master_record = json.loads(master_record_str)
                        asset_record = json.loads(asset_record_str)
                        thumbURL = master_record["fields"]["resJPEGThumbRes"]["value"]["downloadURL"]
                        cache_dir = os.path.join(".", "caches")
                        fn = recordName.replace("/", "_") + file_type
                        if MOCK_ACTIVE:
                            if i == 200:
                                _mock_images + mock_images("Soft", (i // 200) + 1, 200)
                            target = _mock_images[i]
                            thumbURL = target["url"]
                            # 对mock数据单独进行缓存π
                            cache_dir = os.path.join(".", "caches", "mock")
                            fn = str(target["id"]) + ".jpeg"
                        logging.info("{}. {} --> {}".format(i, recordName, fn, thumbURL))
                        if not os.path.exists(cache_dir):
                            os.makedirs(cache_dir)
                        fp = os.path.join(cache_dir, fn)
                        try:
                            if not os.path.exists(fp):
                                # 如果没有缓存,则先下载下来先产生缓存
                                response = requests.get(thumbURL)
                                contentType = response.headers.get("Content-Type")

                                if contentType in ["video/mp4"]:
                                    video_fp = fp + ".mp4"
                                    with open(video_fp, "wb") as f:
                                        f.write(response.content)
                                    export_frame(video_fp, 1, fp)
                                else:
                                    # if contentType in ["image/jpeg", "image/png"]:
                                    with open(fp, "wb") as f:
                                        f.write(response.content)

                            # 打开
                            img = Image.open(fp)
                            img.thumbnail((100, 100))  # Resize image while preserving aspect ratio
                            img = ImageTk.PhotoImage(img)

                            self.assets_caches[recordName] = img
                        except FileNotFoundError as e:
                            logging.error("Could not find file: {}".format(fp), exc_info=True)
                        except UnidentifiedImageError as e:
                            logging.error("FileReadException: {},{}".format(e, response), exc_info=True)
                        except requests.exceptions.SSLError as e:
                            logging.error("NetworkException: {}".format(e), exc_info=True)

    def update_labels(self):
        epoch_num = 1
        createdAt = datetime.datetime.now()
        while True:
            a = 0
            b = 0
            if len(self.assets) == 0:
                dlt = datetime.datetime.now() - createdAt
                logging.info("Waiting for assets to be set....{} ".format(dlt))
                time.sleep(5)
                continue
            for i, asset_info in enumerate(self.assets):
                recordName, size, file_type, created, modified, master_record_str, asset_record_str = asset_info
                if self.assets_caches.__contains__(recordName):
                    img = self.assets_caches[recordName]
                    self._add_label(i, img)
                    a += 1
                else:
                    b += 1
                    self._add_label(i, None)
            epoch_num += 1
            logging.info("Epoch: {} thumb:{}".format(epoch_num, a))

    def _on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
