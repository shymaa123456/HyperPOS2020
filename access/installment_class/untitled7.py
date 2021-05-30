# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:23:13 2021

@author: mustafa
"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget ,QDialog  ,qApp
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        login_widget = LoginWidget(self)
        login_widget.button.clicked.connect(self.login)
        self.central_widget.addWidget(login_widget)
    def login(self):
        logged_in_widget = LoggedWidget(self)
        self.central_widget.addWidget(logged_in_widget)
        self.central_widget.setCurrentWidget(logged_in_widget)


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.button = QPushButton('Login')
        layout.addWidget(self.button)
        self.setLayout(layout)
        # you might want to do self.button.click.connect(self.parent().login) here


class LoggedWidget(QWidget):
    def __init__(self, parent=None):
        super(LoggedWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.label = QLabel('logged in!')
        layout.addWidget(self.label)
        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()