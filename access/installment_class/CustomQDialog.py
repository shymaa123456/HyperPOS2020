# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 08:43:07 2021

@author: mustafa
"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget ,QDialog

class WindowTwo(QDialog):

    def __init__(self , parent):
        QDialog.__init__(self)
        self.setWindowTitle('Window Two')

        layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)
        parent.show()