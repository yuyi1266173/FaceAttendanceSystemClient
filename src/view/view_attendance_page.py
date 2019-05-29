# !python 3.6
# -*-coding: utf-8 -*-

import time
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, \
    QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from video_utils.video_player import VlcPlayer

from view.collect_info_dialog import CollectInfoDialog
from view.confirm_dialog import ConfirmDialog


class AttendancePageWidget(QWidget):

    def __init__(self):
        super(AttendancePageWidget, self).__init__()
        self.tip_label = None
        self.collect_info_button = None
        self.start_button = None
        self.collect_info_dialog = None
        self.confirm_dialog = None
        self.video_label = None
        self.video_player = None

        url = "rtsp://admin:hzkj12345@192.168.1.64:554/11"

        self.init_ui()
        self.set_widgets()
        self.init_video_player(url=url)
        self.connect_events()
        self.video_player.start()

    def init_ui(self):
        self.video_label = QLabel()
        self.video_label.setFixedSize(800, 600)
        self.video_label.setText("视频区域")
        self.video_label.setStyleSheet("background-color: #665599;")
        self.video_label.setAlignment(Qt.AlignCenter)

        video_layout = QHBoxLayout()
        video_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Fixed))
        video_layout.addWidget(self.video_label)
        video_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.tip_label = QLabel()
        self.tip_label.setFixedHeight(30)
        self.tip_label.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color:#FFFFFF;")
        self.tip_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton()
        self.start_button.setFixedSize(100, 40)
        self.start_button.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color:#FFFFFF;"
                                        "background-color: #445566;")

        self.collect_info_button = QPushButton()
        self.collect_info_button.setFixedSize(100, 40)
        self.collect_info_button.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color:#FFFFFF;"
                                               "background-color: #445566;")

        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Expanding))
        button_layout.addWidget(self.collect_info_button)
        button_layout.addWidget(self.start_button)
        button_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Expanding))

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(video_layout)
        main_layout.addItem(QSpacerItem(20, 5, QSizePolicy.Fixed, QSizePolicy.Fixed))
        main_layout.addWidget(self.tip_label)
        main_layout.addItem(QSpacerItem(20, 5, QSizePolicy.Fixed, QSizePolicy.Fixed))
        main_layout.addLayout(button_layout)
        # main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

    def set_widgets(self):
        self.tip_label.setText("请正视摄像头，点击下方按钮")
        self.start_button.setText("开始打卡")
        self.collect_info_button.setText("采集人脸")
        self.setStyleSheet("background-color: #222222;")
        # self.setFixedSize(1200, 800)

    def init_video_player(self, url):
        self.video_player = VlcPlayer(url, int(self.video_label.winId()))

    def connect_events(self):
        self.start_button.clicked.connect(self.start_button_fun)
        self.collect_info_button.clicked.connect(self.collect_info__fun)

    def start_button_fun(self):
        if self.confirm_dialog is None:
            self.confirm_dialog = ConfirmDialog()
        self.confirm_dialog.set_dialog_info(use_type=0, staff_no=1011, staff_name="wuyu",
                                            image_url="E://py_projects/FaceAttendanceSystemClient/src/rose_logo.png")
        self.confirm_dialog.show()

    def collect_info__fun(self):
        if self.collect_info_dialog is None:
            self.collect_info_dialog = CollectInfoDialog()
        self.collect_info_dialog.show()


if __name__ == "__main__":
    import os
    os.chdir("../")
    print(os.getcwd())

    import sys
    from PyQt5.QtWidgets import QApplication

    from model import init_data_database

    init_data_database()

    app = QApplication(sys.argv)
    window = AttendancePageWidget()
    window.show()

    sys.exit(app.exec_())
