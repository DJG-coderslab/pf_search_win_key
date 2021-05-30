#!python
# encoding: utf-8

# Created by Preload at 2020-09-24

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

from designe_about import Ui_MainWindow


class About(Ui_MainWindow, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(About, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("About")
        self.pushButton.clicked.connect(self.close_window)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape:
            self.close_window()

    def close_window(self) -> None:
        self.close()
