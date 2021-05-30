#!python
# encoding: utf-8

# Created by Preload at 2020-08-31

import os
import re
import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar,
                             QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from about import About
from designe_gui import Ui_MainWindow
from search_key import SearchKey


class UI(Ui_MainWindow, QMainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
        self.my_version = "2.1.2.0"
        self.my_release_date = "28.09.2020"
        self.my_author = "jg@pwr.pl"
        self.search_key = SearchKey()
        self.setupUi(self)
        self.setWindowTitle("Windows Search Key")
        self.setWindowIcon(QIcon(self.rel_path("icons/main.ico")))
        self.setup_button()
        self.setup_line_edit()
        self.validated_key = False
        toolbar = QToolBar("My toolbar")
        self.addToolBar(toolbar)
        open_action = QAction(QIcon(self.rel_path("icons/folder-open.png")),
                              "Open", self)
        open_action.setStatusTip("Open file")
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        save_action = QAction(QIcon(self.rel_path("icons/disk.png")),
                              "Save", self)
        save_action.setStatusTip("Save")
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)
        # toolbar.addAction(save_action)
        save_as_action = QAction(
            QIcon(self.rel_path("icons/disk--pencil.png")),
            "Save as", self)
        save_as_action.setStatusTip("Save as")
        save_as_action.triggered.connect(self.save_as)
        toolbar.addAction(save_as_action)
        about_action = QAction(
            QIcon(self.rel_path("icons/book-question.png")), "About", self)
        about_action.setStatusTip("About")
        about_action.triggered.connect(self.about)
        toolbar.addAction(about_action)

    def setup_button(self):
        self.pushButton.setText("Change key")
        self.pushButton.clicked.connect(self.btn_action)

    def setup_line_edit(self):
        # TODO move the focus to another widget
        self.lineEdit.setPlaceholderText("Enter the new win key")
        self.lineEdit.setMaxLength(29)
        self.lineEdit.textEdited.connect(self.validating_key)

    def btn_action(self):
        if self.validated_key:
            self.search_key.replace_key(self.lineEdit.text())
            self.statusbar.showMessage("A file was modified")
        else:
            self.statusbar.showMessage("A new key is not property")

    def about(self):
        self.about_window = About()
        tmp = self.about_window.label.text().replace('{}', self.my_version)
        self.about_window.label.setText(tmp)
        self.about_window.show()

    def open_file(self):
        win_key = b''
        directory = str(Path.cwd())
        file_name = QFileDialog.getOpenFileName(self, "Open file", directory)
        if file_name[0]:
            # print(file_name)
            self.search_key.open_file(file_name[0])
            win_key = self.search_key.search_key()
        if win_key:
            self.lineEdit_2.setText(win_key.decode("utf-8"))
        else:
            self.lineEdit_2.setText("Key not found")

    def save(self):
        print("Saved")

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save as:", "")
        if filename:
            self.search_key.save_file(filename)

    def validating_key(self):
        pattern = (r'[A-Z\d]{5}-[A-Z\d]{5}-[A-Z\d]{5}-[A-Z\d]{5}-[A-Z\d]{5}')
        p = re.compile(pattern)
        tmp_str = self.lineEdit.text().upper()
        self.lineEdit.setText(tmp_str)
        if p.search(self.lineEdit.text()):
            self.lineEdit.setStyleSheet("color: black")
            self.validated_key = True
        else:
            self.lineEdit.setStyleSheet("color: red")
            self.validated_key = False

    def rel_path(self, relative_path):
        """ Get absolute path to resource, works for dev
        and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape:
            self.close()


app = QApplication(sys.argv)
window = UI()
window.show()
app.exec_()
