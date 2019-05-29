#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import grpc
import numpy as np
import cv2,base64
from protoc import collect_face_pb2_grpc, collect_face_pb2

_HOST = '192.168.1.109'
_PORT = '8081'


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


def start_collect_face(staff_id):
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = collect_face_pb2_grpc.CollectFaceStub(channel=conn)

    response = client.DoCollectFace(collect_face_pb2.CollectFaceRequest(staff_id=staff_id))

    print("received.staff_id:{} ".format(str(response.staff_id)))
    print("received.width:{} ".format(str(response.image.width)))
    print("received.high:{} ".format(str(response.image.high)))
    print("received.channel:{} ".format(str(response.image.channel)))

    image_path = os.path.abspath("../resource/face_image/{}.jpg".format(staff_id))
    print(image_path)

    with open(image_path, 'wb') as f:
        f.write(response.image.raw_data)

    return image_path

    # base64 mode
    # data = base64_2_cv2(response.image.raw_data)
    #
    # print(type(data))
    #
    # cv2.imwrite("test123456.png", data)


if __name__ == '__main__':
    import os
    os.chdir("../")
    print(os.getcwd())

    start_collect_face(35289)
