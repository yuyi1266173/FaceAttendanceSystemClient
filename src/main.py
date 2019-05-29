# !python 3.6
# -*-coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from model import init_data_database, add_staff_fun_test
from view.main_window import MainWindow


def run_app():
    init_data_database()
    # add_staff_fun_test()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
