# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:55:20 2021

@author: mustafa
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 08:16:24 2021
https://gist.github.com/MalloyDelacroix/2c509d6bcad35c7e35b1851dfc32d161
@author: mustafa
"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget ,QDialog
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QWidget):

    #switch_window = QtCore.pyqtSignal(str)

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Main Window')
        
        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        self.button.clicked.connect(self.switch)
        layout.addWidget(self.button)

        self.setLayout(layout)
        #self.show()
        
    def switch(self):
        
        #self.switch_window.emit(self.line_edit.text())
        wtwo = WindowTwo( "text" ,self )
        wtwo.setWindowFlags(wtwo.windowFlags() | Qt.Window)
        wtwo.show()    
        
        
class WindowTwo(QWidget):

    def __init__(self , text ,  *args ):
        QWidget.__init__(self, *args )
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Window Two')
        self.data = text

        layout = QtWidgets.QGridLayout()
        print(text)
        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)
        #self.show()


class Login(QWidget):

    #switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()

    def login(self):
        mainw = MainWindow(self)
        mainw.setWindowFlags(mainw.windowFlags() | Qt.Window)
        mainw.show()


def main():
        app = QApplication(sys.argv)
        window = Login()
        app.exec_()

if __name__ == '__main__':
    main()

