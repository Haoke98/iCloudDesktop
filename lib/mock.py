# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/2/23
@Software: PyCharm
@disc:
======================================="""
import json

import requests


def images(page: int = 1, limit: int = 100, nsfw: str = None, sort: str = None, period: str = None):
    """
    :param page: number The page from which to start fetching creators
    :param limit: The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 100 results.
    :param sort: enum (Most Reactions, Most Comments, Newest) The order in which you wish to sort the results
    :param nsfw: boolean | enum (None, Soft, Mature, X) Filter to images that contain mature content flags or not (undefined returns all)
    :param period: enum (AllTime, Year, Month, Week, Day) The time frame in which the images will be sorted
    :return:
    """
    url = "https://civitai.com/api/v1/images?page={}".format(page)
    if limit is not None:
        url += "&limit={}".format(limit)
    if nsfw is not None:
        url += "&nsfw={}".format(nsfw)
    if sort is not None:
        url += "&sort={}".format(sort)
    if period is not None:
        url += "&period={}".format(period)

    resp = requests.get(url)
    items = resp.json()["items"]
    res = []
    for item in items:
        master_fields = {"fields": {"resJPEGThumbRes": {"value": {"downloadURL": item["url"]}}}}
        master_fields_str = json.dumps(master_fields)
        asset_fields_str = json.dumps({})
        res.append((str(item["id"]), "size", ".jpeg", "created", "modified", master_fields_str, asset_fields_str))
    return res
