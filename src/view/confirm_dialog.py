
# !python 3.6
# # -*-coding: utf-8 -*-

import time
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ConfirmDialog(QDialog):

    def __init__(self):
        super(ConfirmDialog, self).__init__()
        self.top_label = None
        self.image_label = None
        self.staff_no_label = None
        self.staff_name_label = None
        self.time_label = None
        self.confirm_button = None

        self.init_ui()
        self.set_widgets()
        self.connect_events()

    def init_ui(self):
        self.top_label = QLabel()
        self.top_label.setFixedHeight(40)
        self.top_label.setAlignment(Qt.AlignCenter)
        self.top_label.setStyleSheet("font-size:20px; font-family:Microsoft YaHei; color: red;")

        self.image_label = QLabel()
        self.image_label.setFixedSize(80, 100)
        self.image_label.setStyleSheet("background-color: #445566;")

        self.staff_no_label = QLabel()
        self.staff_no_label.setFixedHeight(40)
        self.staff_no_label.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color: blue;")

        self.staff_name_label = QLabel()
        self.staff_name_label.setFixedHeight(40)
        self.staff_name_label.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color: blue;")

        self.time_label = QLabel()
        self.time_label.setFixedHeight(40)
        self.time_label.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color: blue;")

        self.confirm_button = QPushButton("确定")
        self.confirm_button.setFixedSize(100, 40)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(self.top_label)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.staff_no_label)
        main_layout.addWidget(self.staff_name_label)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.confirm_button)

        self.setLayout(main_layout)

    def set_widgets(self):
        self.top_label.setText("打卡成功！")
        self.staff_no_label.setText("工号：{}".format(1011))
        self.staff_name_label.setText("姓名：{}".format("吴宇"))
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.time_label.setText("打卡时间: {}".format(time_str))
        pix = QPixmap("E://py_projects/FaceAttendanceSystemClient/resource/face_image/35289.jpg").scaled(80, 100)
        self.image_label.setPixmap(pix)

        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #999999;")

    def connect_events(self):
        self.confirm_button.clicked.connect(self.close)

    def set_dialog_info(self, use_type, staff_no, staff_name, image_url):
        if use_type == 0:
            self.top_label.setText("打卡成功！")
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            self.time_label.setText("打卡时间: {}".format(time_str))
        else:
            self.top_label.setText("人脸采集成功！")
            self.time_label.setText("")

        self.staff_no_label.setText("工号：{}".format(staff_no))
        self.staff_name_label.setText("姓名：{}".format(staff_name))
        pix = QPixmap(image_url).scaled(80, 100)
        self.image_label.setPixmap(pix)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ConfirmDialog()
    window.show()

    sys.exit(app.exec_())

