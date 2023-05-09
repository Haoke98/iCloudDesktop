# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/5/9
@Software: PyCharm
@disc:
======================================="""
import logging

import piexif


def get_gps_info(raw_path):
    # 读取图片的exif信息
    exif_dict = piexif.load(raw_path)
    # 获取GPS信息
    gps_dict = exif_dict['GPS']

    # 判断是否包含GPS信息
    if not gps_dict:
        # print('该照片没有GPS信息')
        return False, None, None
    else:
        # 根据经纬度获取地理位置信息
        lat = gps_dict.get(piexif.GPSIFD.GPSLatitude)
        lat_ref = gps_dict.get(piexif.GPSIFD.GPSLatitudeRef)
        lng = gps_dict.get(piexif.GPSIFD.GPSLongitude)
        lng_ref = gps_dict.get(piexif.GPSIFD.GPSLongitudeRef)

        if lat and lat_ref and lng and lng_ref:
            lat = float(lat[0][0]) / float(lat[0][1]) + float(lat[1][0]) / (60 * float(lat[1][1])) + float(
                lat[2][0]) / (3600 * float(lat[2][1]))
            lng = float(lng[0][0]) / float(lng[0][1]) + float(lng[1][0]) / (60 * float(lng[1][1])) + float(
                lng[2][0]) / (3600 * float(lng[2][1]))

            if lat_ref.decode('utf-8') == 'S':
                lat = -lat
            if lng_ref.decode('utf-8') == 'W':
                lng = -lng
            logging.info(f'照片拍摄地点:{(lat, lng)}')
            return True, lat, lng
        else:
            return False, None, None
            # print('该照片没有经纬度信息')
