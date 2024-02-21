# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/28
@Software: PyCharm
@disc:
======================================="""
import tkinter as tk


class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # 在主页上显示用户信息和头像
        self.welcome_label = tk.Label(self, text="")
        self.welcome_label.grid(row=0, column=1, columnspan=2)

        # 创建头像图标
        # 这里使用一个简单的示例图片代替真实的用户头像
        photo = tk.PhotoImage(file="/Users/shadikesadamu/Documents/壁纸/20231106213414735.png").subsample(4, 4)
        avatar_label = tk.Label(self, image=photo)
        avatar_label.photo = photo
        avatar_label.grid(row=1, column=1, columnspan=2)

        # 创建登录按钮
        self.login_button = tk.Button(self, text="开始同步", command=self.sync)
        self.login_button.grid(row=2, column=1, columnspan=2)

        # 创建下拉菜单
        # menu_bar = tk.Menu(self)
        # self.config(menu=menu_bar)

        # 用户菜单
        # user_menu = tk.Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label=username, menu=user_menu)
        # user_menu.add_command(label="个人信息")
        # user_menu.add_separator()
        # user_menu.add_command(label="注销", command=lambda: self.logout())

    def show(self, username):
        self.welcome_label.config(text=f"欢迎回来，{username}！")
        self.pack()

    def sync(self):
        """
            同步数据
            :return:
            """
        iService = self.master.iService
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
