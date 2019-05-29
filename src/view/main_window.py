# !python 3.6
# # -*-coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, \
    QSpacerItem, QSizePolicy, QStackedWidget
from PyQt5.QtCore import Qt

from view.view_attendance_page import AttendancePageWidget


class MainWindow(QMainWindow):
    head_button_style_select = """font-size:19px;
                                font-family:Microsoft YaHei;
                                color:#00BFF3;
                                border:none;
                                padding-top:4px;"""

    head_button_style_no_select = """font-size:19px;
                                                   font-family:Microsoft YaHei;
                                                   color:#FFFFFF;
                                                   border:none;
                                                   padding-top:4px;"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_widget = None
        self.main_layout = None
        self.tab_button_layout = None
        self.attendance_page_button = None
        self.monitor_page_button = None
        self.person_manager_button = None
        self.buttom_widget = None
        self.close_button = None

        self.init_ui()
        self.set_widgets()
        self.connect_events()

    def init_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # 顶部标题栏
        title_layout = QHBoxLayout()

        main_label = QLabel()
        main_label.setFixedHeight(100)
        # main_label.setFixedWidth(1800)
        main_label.setText("人脸识别考勤系统")
        main_label.setStyleSheet("font-size:25px; font-family:Microsoft YaHei;")
        main_label.setAlignment(Qt.AlignCenter)

        self.close_button = QPushButton("退出系统")
        self.close_button.setFixedSize(100, 30)
        self.close_button.setStyleSheet("font-size:15px; font-family:Microsoft YaHei; color:#FFFFFF;"
                                        "background-color: #445566;")

        title_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Fixed))
        title_layout.addWidget(main_label)
        title_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Fixed))
        title_layout.addWidget(self.close_button)

        # Tab页切换按钮栏
        self.tab_button_layout = QHBoxLayout()

        self.attendance_page_button = QPushButton()
        self.attendance_page_button.setFixedSize(37, 30)
        self.attendance_page_button.setStyleSheet(self.head_button_style_select)

        self.monitor_page_button = QPushButton()
        self.monitor_page_button.setFixedSize(80, 30)
        self.monitor_page_button.setStyleSheet(self.head_button_style_no_select)

        self.person_manager_button = QPushButton()
        self.person_manager_button.setFixedSize(80, 30)
        self.person_manager_button.setStyleSheet(self.head_button_style_no_select)

        self.tab_button_layout.addWidget(self.attendance_page_button)
        self.tab_button_layout.addWidget(self.monitor_page_button)
        self.tab_button_layout.addWidget(self.person_manager_button)

        # 帧布局 内容部分
        attendance_widget = AttendancePageWidget()
        # attendance_widget.setStyleSheet("background-color: blue")
        monitor_widget = QWidget()
        monitor_widget.setStyleSheet("background-color: #888888")
        person_manage_widget = QWidget()
        person_manage_widget.setStyleSheet("background-color: #cccccc")

        self.buttom_widget = QStackedWidget()
        self.buttom_widget.addWidget(attendance_widget)
        self.buttom_widget.addWidget(monitor_widget)
        self.buttom_widget.addWidget(person_manage_widget)
        self.buttom_widget.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addLayout(title_layout)
        self.main_layout.addLayout(self.tab_button_layout)
        self.main_layout.addWidget(self.buttom_widget)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def set_widgets(self):
        self.resize(1920, 1080)
        self.setStyleSheet("background-color:#2c2c2c")
        self.setGeometry(0, 0, 1920, 1080)
        self.showFullScreen()

        self.attendance_page_button.setText("考勤")
        self.monitor_page_button.setText("监控")
        self.person_manager_button.setText("员工管理")
        self.buttom_widget.setCurrentIndex(0)

    def connect_events(self):
        self.close_button.clicked.connect(self.close)
        self.attendance_page_button.clicked.connect(self.show_attendance_page)
        self.monitor_page_button.clicked.connect(self.show_monitor_page)
        self.person_manager_button.clicked.connect(self.show_person_manager_page)

    def show_attendance_page(self):
        self.attendance_page_button.setStyleSheet(self.head_button_style_select)
        self.monitor_page_button.setStyleSheet(self.head_button_style_no_select)
        self.person_manager_button.setStyleSheet(self.head_button_style_no_select)
        self.buttom_widget.setCurrentIndex(0)

    def show_monitor_page(self):
        self.attendance_page_button.setStyleSheet(self.head_button_style_no_select)
        self.monitor_page_button.setStyleSheet(self.head_button_style_select)
        self.person_manager_button.setStyleSheet(self.head_button_style_no_select)
        self.buttom_widget.setCurrentIndex(1)

    def show_person_manager_page(self):
        self.attendance_page_button.setStyleSheet(self.head_button_style_no_select)
        self.monitor_page_button.setStyleSheet(self.head_button_style_no_select)
        self.person_manager_button.setStyleSheet(self.head_button_style_select)
        self.buttom_widget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

