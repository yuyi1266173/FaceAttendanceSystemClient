# !python 3.6
# # -*-coding: utf-8 -*-

import time
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QFormLayout, QLineEdit
from PyQt5.QtCore import Qt

from config import LOG
from model import Staff, init_data_database
from view.confirm_dialog import ConfirmDialog
from protoc.grpc_collect_face_client import start_collect_face


class CollectInfoDialog(QDialog):

    def __init__(self):
        super(CollectInfoDialog, self).__init__()
        self.staff_no_edit = None
        self.staff_name_edit = None
        self.start_collect_button = None
        self.tip_label = None
        self.confirm_dialog = None

        self.init_ui()
        self.set_widgets()
        self.connect_events()

    def init_ui(self):
        head_label = QLabel()
        head_label.setFixedHeight(40)
        head_label.setText("员工信息录入")
        head_label.setStyleSheet("font-size:25px; font-family:Microsoft YaHei;")

        self.tip_label = QLabel()
        self.tip_label.setFixedHeight(30)
        self.tip_label.setStyleSheet("font-size:20px; font-family:Microsoft YaHei; color:red;")

        staff_no_label = QLabel()
        staff_no_label.setFixedSize(100, 30)
        staff_no_label.setText("工号")
        staff_no_label.setStyleSheet("font-size:20px; font-family:Microsoft YaHei;")

        self.staff_no_edit = QLineEdit()
        self.staff_no_edit.setFixedHeight(30)

        staff_name_label = QLabel()
        staff_name_label.setFixedSize(100, 30)
        staff_name_label.setText("姓名")
        staff_name_label.setStyleSheet("font-size:20px; font-family:Microsoft YaHei;")

        self.staff_name_edit = QLineEdit()
        self.staff_name_edit.setFixedHeight(30)

        self.start_collect_button = QPushButton()
        self.start_collect_button.setFixedSize(100, 40)

        main_layout = QFormLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addRow(head_label)
        main_layout.addRow(self.tip_label)
        main_layout.addRow(staff_no_label, self.staff_no_edit)
        main_layout.addRow(staff_name_label, self.staff_name_edit)
        main_layout.addRow(self.start_collect_button)
        self.setLayout(main_layout)

    def set_widgets(self):
        self.start_collect_button.setText("开始人脸采集")
        # self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #999999;")

    def connect_events(self):
        self.start_collect_button.clicked.connect(self.start_collect_fun)
        # self.staff_no_edit.textEdited.connect(self.clear_tip_info)
        # self.staff_name_edit.textEdited.connect(self.clear_tip_info)
        self.staff_no_edit.selectionChanged.connect(self.clear_tip_info)
        self.staff_name_edit.selectionChanged.connect(self.clear_tip_info)

    def start_collect_fun(self):
        print(self.staff_no_edit.text(), self.staff_name_edit.text())

        staff_no = self.staff_no_edit.text()
        staff_name = self.staff_name_edit.text()

        if len(staff_no.strip()) == 0:
            self.tip_label.setText("请输入员工工号！")
            return

        if len(staff_name.strip()) == 0:
            self.tip_label.setText("请输入员工姓名！")
            return

        the_staff = Staff.get_staff_by_no(staff_no)
        if the_staff is None or len(the_staff) == 0:
            staff_id, err_str = Staff.add_staff(staff_no=int(staff_no), name=staff_name)

            if err_str is not None:
                self.tip_label.setText(err_str)
                return
        else:
            if len(the_staff) != 1:
                self.tip_label.setText("异常：数据库中已存在{}个工号为{}的员工".format(len(the_staff), staff_no))
                return
            elif the_staff[0].is_collect_face_image is True:
                self.tip_label.setText("异常：数据库中已存在{}个工号为{}的员工(已采集完人脸数据)".
                                       format(len(the_staff), staff_no))
                return

        try:
            face_image_path = start_collect_face(int(staff_no))
        except Exception as e:
            LOG.error("采集人脸异常：{}".format(e))
            self.tip_label.setText("采集人脸异常：连接服务器错误。")
            return

        self.staff_no_edit.setText("")
        self.staff_name_edit.setText("")
        self.close()

        print("face_image_path ----- ", face_image_path)

        if self.confirm_dialog is None:
            self.confirm_dialog = ConfirmDialog()
        self.confirm_dialog.set_dialog_info(use_type=1, staff_no=staff_no, staff_name=staff_name,
                                            image_url=face_image_path)
        self.confirm_dialog.show()

        try:
            Staff.update_is_collect_face_image(staff_no=staff_no, is_collect_face_image=True)
        except Exception as e:
            LOG.error("update_is_collect_face_image Error:{}".format(e))

    def clear_tip_info(self):
        self.tip_label.setText("")


if __name__ == "__main__":
    import os
    os.chdir("../")
    print(os.getcwd())

    import sys
    from PyQt5.QtWidgets import QApplication

    # from model import Staff, init_data_database

    init_data_database()

    app = QApplication(sys.argv)
    window = CollectInfoDialog()
    window.show()

    sys.exit(app.exec_())

