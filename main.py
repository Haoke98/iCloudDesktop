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
import random
import sys
import threading
import time
import tkinter as tk
from tkinter import simpledialog

import click
import webview
from webview import JavascriptException

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


class HeavyStuffAPI:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def doHeavyStuff(self):
        time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': 'Operation cancelled'}
                break
        else:
            then = time.time()
            response = {
                'message': 'Operation took {0:.1f} seconds on the thread {1}'.format(
                    (then - now), threading.current_thread()
                )
            }
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True


class NotExposedApi:
    def notExposedMethod(self):
        return 'This method is not exposed'


class Api:
    heavy_stuff = HeavyStuffAPI()
    _this_wont_be_exposed = NotExposedApi()

    def login(self):
        return {
            'token': "asjdflkajsdlkfsdjflkj"
        }

    def init(self):
        response = {'message': 'Hello from Python {0}'.format(sys.version)}
        return response

    def getRandomNumber(self):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(
                random.randint(0, 100000000)
            )
        }
        return response

    def sayHelloTo(self, name):
        response = {'message': 'Hello {0}!'.format(name)}
        return response

    def error(self):
        raise Exception('This is a Python exception')

    def log(self, value):
        print(value)


def evaluate_js(window):
    result = window.evaluate_js(
        r"""
        var h1 = document.createElement('h1')
        var text = document.createTextNode('Hello pywebview')
        h1.appendChild(text)
        document.body.appendChild(h1)

        document.body.style.backgroundColor = '#212121'
        document.body.style.color = '#f2f2f2'

        // Return user agent
        'User agent:\n' + navigator.userAgent;
        """
    )

    print(result)

    try:
        result = window.evaluate_js('syntaxerror#$%#$')
    except JavascriptException as e:
        print('Javascript exception occured: ', e)


@click.command()
@click.option("--mock", is_flag=True, default=False, help="Open the mock mode.")
@click.option("-d", "--debug", is_flag=True, default=False, help="Activate debug mode.")
def main(mock: bool, debug: bool):
    global MOCK_ACTIVE
    MOCK_ACTIVE = mock
    api = Api()
    window = webview.create_window("iCloud Desktop", 'src/index.html', width=800, height=600, js_api=api,
                                   transparent=False, frameless=False, min_size=(400, 400))
    webview.start(evaluate_js, window, debug=debug)
    # app.mainloop()


if __name__ == '__main__':
    logger.init("icloud", console_level=logging.INFO)
    main()
