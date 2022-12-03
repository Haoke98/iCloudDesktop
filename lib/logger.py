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
    logFilePath = os.path.join(LOG_DIR,
                               f"{filename}-{str(n.year).zfill(4)}{str(n.month).zfill(2)}{n.day}{str(n.hour).zfill(2)}{str(n.minute).zfill(2)}{str(n.second).zfill(2)}.log")
    file_handler = logging.FileHandler(filename=logFilePath, mode='a', encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter(fmt='[{asctime:s}][{levelname:^7s}][{threadName:s}-{filename:s}:{lineno:d}]: {message:s}',
                          style='{', datefmt='%m/%d/%Y %H:%M:%S'))
    # 指定最低日志级别：（critical > error > warning > info > debug）
    file_handler.setLevel(file_level)

    logging.basicConfig(level=min(file_level, console_level), handlers=[file_handler, console_handler])
    logging.debug("日志输出文件：" + logFilePath)


class Logger:
    def __init__(self, name=None, log_level=logging.DEBUG):
        LOG_DIR = os.path.join(".", "logs")
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        n = datetime.datetime.now()
        logFilePath = os.path.join(LOG_DIR, f"{name}-{n.strftime('%Y%m%d%H%M')}.log")
        print("日志输出文件：", logFilePath)
        # 获取logger对象
        self.logger = logging.getLogger(logFilePath)

        # 避免重复打印日志
        self.logger.handlers = []

        # 指定最低日志级别：（critical > error > warning > info > debug）
        self.logger.setLevel(log_level)

        # 日志格化字符串
        console_fmt = '%(log_color)s%(asctime)s-%(threadName)s-%(filename)s-[line:%(lineno)d]-%(levelname)s: %(message)s'
        file_fmt = '%(asctime)s-%(threadName)s-%(filename)s-[line:%(lineno)d]-%(levelname)s: %(message)s'

        # 控制台输出不同级别日志颜色设置
        color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        }

        console_formatter = colorlog.ColoredFormatter(fmt=console_fmt, log_colors=color_config)
        file_formatter = logging.Formatter(fmt=file_fmt)

        # 输出到控制台
        console_handler = logging.StreamHandler()
        # 输出到文件
        file_handler = logging.FileHandler(filename=name, mode='a', encoding='utf-8')

        # 设置日志格式
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # 处理器设置日志级别，不同处理器可各自设置级别，默认使用logger日志级别
        # console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.ERROR)  # 只有error和critical级别才会写入日志文件

        # logger添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


# if __name__ == '__main__':
#     # 控制台只会显示warning及以上级别日志信息，而log.txt文件中则会记录error及以上级别日志信息
#     log = Logger(name='logger', log_level=logging.WARNING)
#     log.debug('debug')
#     log.info('info')
#     log.warning('warning')
#     log.error('error')
#     log.critical('critical')
