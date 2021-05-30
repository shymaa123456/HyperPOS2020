# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 11:37:47 2021
https://codeloop.org/pyqt5-open-second-dialog-by-clicking-button/
@author: mustafa
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout
import sys

from CustomQDialog import WindowTwo 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        self.title = "PyQt5 Window"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
 
 
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        vbox = QVBoxLayout()
 
 
 
        self.btn = QPushButton("Open Second Dialog")
        self.btn.setFont(QtGui.QFont("Sanserif", 15))
        self.btn.clicked.connect(self.openSecondDialog)
        #self.btn.clicked.connect(self.openSecondCustomDialog)

        vbox.addWidget(self.btn)
 
        self.setLayout(vbox)

        self.show()
        #parent.show()
 
    
    def openSecondDialog(self):
        mydialog = QDialog(self)
        #mydialog.setModal(True)
        #mydialog.exec()
 
        mydialog.show()
    """
    def openSecondCustomDialog(self):
        mydialog = WindowTwo(self)
        #mydialog.setModal(True)
        #mydialog.exec()
        mydialog.show()
   """
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())