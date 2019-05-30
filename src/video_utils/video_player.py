#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import ctypes
import sys
import time
# import vlc
# from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer
from vlc import (
    Instance,
    libvlc_media_player_set_hwnd,
    libvlc_media_release,
    libvlc_media_new_path,
    libvlc_video_take_snapshot
)


# VIDEO_WIDTH, VIDEO_HEIGHT = common_lib.get_video_size()
# size = VIDEO_WIDTH * VIDEO_HEIGHT * 4
# buf = (ctypes.c_ubyte * size)()
# buf_p = ctypes.cast(buf, ctypes.c_void_p)
# CorrectVideoLockCb = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))

#
# def draw_rectangle(draw, xy, color=None, width=2):
#     """绘制人脸矩形框"""
#     (x1, y1), (x2, y2) = xy
#     points = (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
#     draw.line(points, fill=color, width=width)
#
#
# class VlcPLayerByCallback(object):
#     API_RECT_FRAME = None
#     API_WITHOUT_RECT_FRAME = None
#
#     def __init__(self, url='rtsp://192.168.16.129:8554/channel=0'):
#         instance = Instance()
#         self.pl = instance.media_player_new()
#         self.libvlc_media = instance.media_new(url)
#         self.libvlc_media.add_option(":network-caching=200")
#         self.libvlc_media.get_mrl()
#         self.pl.set_media(self.libvlc_media)
#         self.pl.audio_set_mute(True)
#
#     @CorrectVideoLockCb
#     def _lockcb(opaque, planes):
#         planes[0] = buf_p
#
#     @vlc.CallbackDecorators.VideoDisplayCb
#     def _display(opaque, picture):
#
#         # if VIDEO_HEIGHT is None or VIDEO_WIDTH is None:
#         #     print('解析视频大小(VIDEO_SIZE)配置错误，VLC回调失败！')
#         #     return
#         # img = Image.frombuffer("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), buf, "raw", "BGRA", 0, 1)
#         # VlcPLayerByCallback.API_WITHOUT_RECT_FRAME = img.copy()
#         # coordinates = FaceCoordinatesReceiver.API_FACE_COORDINATES
#         # if coordinates:
#         #     draw_object = ImageDraw.Draw(img)
#         #     draw_rectangle(draw_object, ((coordinates[0], coordinates[1]), (coordinates[2], coordinates[3])),
#         #                    color='red', width=2)
#         # VlcPLayerByCallback.API_RECT_FRAME = img
#         pass
#
#     def play(self):
#         vlc.libvlc_video_set_callbacks(self.pl, self._lockcb, None, self._display, None)
#         self.pl.video_set_format("RV32", VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_WIDTH * 4)
#         self.pl.play()
#
#     def start(self):
#         self.play()
#
#     def stop(self):
#         self.pl.stop()
#
#     def is_playing(self):
#         return self.pl.is_playing()


class VlcPlayer(object):

    def __init__(self, url, winId):
        self.url = url
        self.winId = winId
        instance = Instance()
        self.player = instance.media_player_new()

        # 网络摄像头
        self.libvlc_media = instance.media_new(self.url)
        self.libvlc_media.add_option(":network-caching=300")

        # 本地摄像头
        # self.libvlc_media = instance.media_new_location('dshow://')

        self.libvlc_media.get_mrl()
        libvlc_media_player_set_hwnd(self.player, self.winId)
        self.player.set_media(self.libvlc_media)

    def start(self):
        self.player.play()
        self.player.audio_set_mute(True)

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.is_playing()

    def capture(self, path):
        ret = False
        path = bytes(path, encoding='utf-8')
        try:
            if libvlc_video_take_snapshot(self.player, 0, path, 640, 480) != 0:
                raise Exception('返回截图失败标识')
        except Exception as e:
            print('截图失败: {}'.format(e))
            return ret
        ret = True
        return ret

#
# class VlcFilePlayer(object):
#
#     def __init__(self, winId):
#         self.winId = winId
#         self.libvlc_instance_ = Instance()
#         self.player = self.libvlc_instance_.media_player_new()
#         self.libvlc_media = None
#         self.duration = 0
#         libvlc_media_player_set_hwnd(self.player, self.winId)
#
#     def start(self):
#         self.player.play()
#         self.player.audio_set_volume(50)
#
#     def stop(self):
#         self.player.stop()
#
#     def pause(self):
#         """0 means play or resume, non zero means pause"""
#         self.player.set_pause(1)
#
#     def is_playing(self):
#         return self.player.is_playing()
#
#     def set_time(self, time_in_ms):
#         if time_in_ms <= 0:
#             return
#         self.player.set_time(time_in_ms)
#
#     def get_time(self):
#         return self.player.get_time()
#
#     def get_progress(self):
#         progress = 0
#         self.duration = self.player.get_length()
#
#         if self.duration == 0:
#             return progress
#
#         try:
#             progress = self.player.get_time() / self.duration
#         except Exception as e:
#             LOG.error("get progress error %s" % str(e))
#
#         return progress
#
#     def get_duration(self):
#         """
#         :return: duration of the video in ms
#         """
#         self.duration = self.player.get_length()
#         return self.duration
#
#     def play_file(self, file_path):
#         if self.libvlc_media:
#             libvlc_media_release(self.libvlc_media)
#             self.libvlc_media = None
#         self.libvlc_media = libvlc_media_new_path(self.libvlc_instance_, file_path.encode("utf-8"))
#         if self.libvlc_media:
#             self.player.set_media(self.libvlc_media)
#             self.duration = self.player.get_length()
#
#
# class VlcFileAudioPlayer(object):
#     def __init__(self):
#         self.libvlc_instance_ = Instance()
#         self.player = self.libvlc_instance_.media_player_new()
#         self.libvlc_media = None
#
#     def play_file(self, file_path):
#         if self.libvlc_media:
#             libvlc_media_release(self.libvlc_media)
#             self.libvlc_media = None
#         self.libvlc_media = libvlc_media_new_path(self.libvlc_instance_, file_path.encode("utf-8"))
#         if self.libvlc_media:
#             self.player.set_media(self.libvlc_media)
#             self.duration = self.player.get_length()
#
#     def start(self):
#         self.player.play()
#         self.player.audio_set_volume(50)
#
#     def stop(self):
#         self.player.stop()
#
#     def pause(self):
#         self.player.pause()
#
#     def is_playing(self):
#         """0 means stop, 1 means playing"""
#         return self.player.is_playing()


class VlcVideoRecorder(object):

    def __init__(self, url, path):
        self.url = url
        instance = Instance()
        self.player = instance.media_player_new()
        self.libvlc_media = instance.media_new(self.url)
        options = "sout=#transcode{vcodec=h264,scale=自动,acodec=mpga,ab=128,channels=2,samplerate=44100,scodec=none}:std{access=file{no-overwrite},mux=mp4,dst=%s}" % str(path)
        print(options)
        self.libvlc_media.add_option(options)
        self.libvlc_media.get_mrl()
        self.player.set_media(self.libvlc_media)

    def start(self):
        self.player.play()
        self.player.audio_set_mute(True)

    def stop(self):
        self.player.stop()


def test(player):
    tt = player.get_time()
    print(tt)
    player.set_time(tt + 100)


if __name__ == "__main__":
    url = "rtsp://admin:hzkj12345@192.168.1.64:554/11"
    path = "'E:/projects/icas_server_proj/media/tt4234678.mp4'"
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(400, 400)
    # timer = QTimer()
    #
    window.show()
    p = VlcPlayer(url, int(window.winId()))
    # p = VlcFileAudioPlayer()
    # p.play_file("14.20180926162456.mp3")
    p.start()
    # "14.20180926162456.mp3"
    # p.start()
    # time.sleep(10)
    # while True:
    #     time.sleep(1)
    #     p.pause()
    #     print("is playing:", p.is_playing())
    #     time.sleep(1)
    #     p.start()
    # # p.capture('.')
    sys.exit(app.exec_())

    # TODO test vlc record video
    # recorder = VlcVideoRecorder(url, path)
    #
    # recorder.start()
    #
    # time.sleep(15)
    # recorder.stop()
