#! /usr/bin/env python
# -*- coding: utf-8 -*-

import grpc
import numpy as np
import cv2, base64
from protoc import face_attendance_pb2_grpc, face_attendance_pb2

_HOST = '192.168.1.109'
_PORT = '8083'


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


def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = face_attendance_pb2_grpc.DetectFaceStub(channel=conn)
    response = client.DoDetectFace(face_attendance_pb2.DetectFaceRequest(state=0))

    print("response:{}".format(len(response.info)))


if __name__ == '__main__':
    run()
