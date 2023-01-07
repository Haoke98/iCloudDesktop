# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/6
@Software: PyCharm
@disc:
======================================="""
import time
from concurrent.futures import ThreadPoolExecutor


def child(index):
    print(f"{index}号员工上班")
    time.sleep(5)
    print(f"{index}号员工下班")


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=3)
    for i in range(1, 101, 1):
        pool.submit(child, i)
    pool.shutdown(wait=True)
