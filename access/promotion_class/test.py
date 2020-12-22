from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from data_connection.h1pos import db1

from access.main_login_class.main import *

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QMessageBox

import sys

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.combo = QComboBox(self)
        self.combo.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.combo.addItem('Foo', 23)
        self.combo.addItem('Bar', 42)

        # self.combo.activated.connect(self.handleActivated)
        self.handleActivated(self.combo.currentIndex())
        self.combo.currentIndexChanged.connect(self.handleActivated)


    def handleActivated(self, index):
        print(self.combo.itemText(index))
        print(self.combo.itemData(index))
        # QMessageBox.about(self.combo.itemText(index), self.combo.itemData(index))
        # QMessageBox.setText(self.combo.itemData(index))
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(str(self.combo.itemData(index)))
        msgBox.setWindowTitle(" Example")
        msgBox.exec()


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
