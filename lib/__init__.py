# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/3
@Software: PyCharm
@disc:
======================================="""
import cv2


def export_frame(video_path, frame_number, output_path):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # 设置视频帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # 读取帧
    ret, frame = cap.read()

    # 检查帧是否成功读取
    if not ret:
        print("Error: Could not read frame.")
        return

    # 保存帧为图像文件
    cv2.imwrite(output_path, frame)

    # 关闭视频文件
    cap.release()
