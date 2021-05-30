# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:03:27 2021

@author: mustafa
"""

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget ,QDialog
from PyQt5.QtWidgets import *

class MyTable(QTableWidget):
        def __init__(self, vehicleFileList, *args):
                QTableWidget.__init__(self, *args)
                self.data = vehicleFileList
                #self.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.resizeColumnsToContents()
                self.resizeRowsToContents()
                self.horizontalHeader().setStretchLastSection(False)
                self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.setHorizontalHeaderLabels(['Available Vehicle Data Files','Missing Files'])

                print('Inside MyTable')
                print(vehicleFileList)

                rowCount=0

                for item in vehicleFileList :
                        print(item)
                        self.setItem(rowCount,0,QTableWidgetItem(item))
                        rowCount+=1

class MainWindow1(QWidget):

    #switch_window = QtCore.pyqtSignal(str)

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Main Window')
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #self.resizeColumnsToContents()
        #self.resizeRowsToContents()
        #self.horizontalHeader().setStretchLastSection(False)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.setHorizontalHeaderLabels(['Available Vehicle Data Files','Missing Files'])

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        #self.button.clicked.connect(self.switch)
        layout.addWidget(self.button)

        self.setLayout(layout)
        #self.show()