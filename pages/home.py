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
        self.welcome_label.pack()

        # 创建头像图标
        # 这里使用一个简单的示例图片代替真实的用户头像
        photo = tk.PhotoImage(file="/Users/shadikesadamu/Documents/壁纸/20231106213414735.png")
        avatar_label = tk.Label(self, image=photo)
        avatar_label.photo = photo
        avatar_label.pack(side=tk.RIGHT)

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
