# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/23
@Software: PyCharm
@disc:
======================================="""
import requests


def mock_images(nsfw: str, page: int = 1, limit: int = 100):
    """

    :param page:
    :param nsfw: boolean | enum (None, Soft, Mature, X) Filter to images that contain mature content flags or not (undefined returns all)
    :param limit: The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 100 results.
    :return:
    """
    resp = requests.get(
        "https://civitai.com/api/v1/images?&limit=" + str(limit) + "&page=" + str(page) + "&nsfw=" + nsfw)
    items = resp.json()["items"]
    return items
