#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import grpc
import numpy as np
import cv2,base64
from protoc import face_attendance_pb2_grpc, face_attendance_pb2

_HOST = '192.168.1.109'
_PORT = '8082'


def base64_2_cv2(encoded_data):
    """
    :param encoded_data: string base64编码后的图片字符串
    :return: ndarray
    """
    ret = None
    try:
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        ret = img
    except Exception as e:
        print('%s' % (e,))
        return ret
    return ret


def base64_2_cv2(encoded_data):

    """
    :param encoded_data: string base64编码后的图片字符串
    :return: ndarray
    """
    ret = None
    try:
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        ret = img
    except Exception as e:
        print('[no.%d] %s' % (100, e))
        return ret
    return ret


def start_face_attendance():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = face_attendance_pb2_grpc.DetectFaceStub(channel=conn)
    response = client.DoDetectFace(face_attendance_pb2.DetectFaceRequest(state=0))
    print("---", response)

    # print("response:{}".format(response.info))
    print(type(response.info), len(response.info))

    if len(response.info) == 0:
        return None, None

    print(response.info[0].staff_id)

    image_path = os.path.abspath("../resource/attendance_image/{}.jpg".format(response.info[0].staff_id))
    print(image_path)

    if os.path.exists(image_path):
        os.remove(image_path)

    with open(image_path, 'wb') as f:
        f.write(response.info[0].image.raw_data)

    return response.info[0].staff_id, image_path


if __name__ == '__main__':
    os.chdir("../")
    print(os.getcwd())

    start_face_attendance()
