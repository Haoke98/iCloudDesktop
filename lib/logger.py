# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/11/17
@Software: PyCharm
@disc:
======================================="""
# coding:utf-8

import datetime
import logging
import os

import colorlog


def init(filename, file_level=logging.DEBUG, console_level=logging.INFO):
    # 控制台输出不同级别日志颜色设置
    color_config = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'purple',
    }

    # 输出到控制台
    console_handler = logging.StreamHandler()
    # console_handler = logging.StreamHandler(sys.stdout)
    # 日志格化字符串
    console_handler.setFormatter(colorlog.ColoredFormatter(
        fmt='{log_color:s}[{asctime:s}][{levelname:^7s}][{threadName:s}-{filename:s}:{lineno:d}]: {message:s}',
        log_colors=color_config, style='{'))
    # 指定最低日志级别：（critical > error > warning > info > debug）
    console_handler.setLevel(console_level)

    # 输出到文件
    LOG_DIR = os.path.join(".", "logs")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    n = datetime.datetime.now()
    logFilePath = os.path.join(LOG_DIR, f"{filename}-{n.strftime('%Y%m%d%H%M')}.log")
    file_handler = logging.FileHandler(filename=logFilePath, mode='a', encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter(fmt='[{asctime:s}][{levelname:^7s}][{threadName:s}-{filename:s}:{lineno:d}]: {message:s}',
                          style='{', datefmt='%m/%d/%Y %H:%M:%S'))
    # 指定最低日志级别：（critical > error > warning > info > debug）
    file_handler.setLevel(file_level)

    logging.basicConfig(level=min(file_level, console_level), handlers=[file_handler, console_handler])
    logging.debug("日志输出文件：" + logFilePath)