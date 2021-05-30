# -*- coding: utf-8 -*-
"""
Created on Sun May 23 15:36:01 2021

@author: mustafa
"""

from PyQt5 import QtCore, QtGui, QtWidgets 
from editForm import Ui_editWindow


class Ui_MainWindow(object):
#    def openWindow(self):
#        self.window = QtWidgets.QMainWindow()
#        self.ui = Ui_editWindow()
#        self.ui.setupUi(self.window)
#        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(641, 661)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_3.setHorizontalSpacing(5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy(). hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.widget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 595, 554))
        self.scrollAreaWidgetContents_2.setObjectName ("scrollAreaWidgetContents_2")
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit.setGeometry(QtCore.QRect(135, 527, 133, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButton.setGeometry(QtCore.QRect(515, 526, 75, 23))
        self.pushButton.setObjectName("pushButton")

#        self.pushButton.clicked.connect(self.openWindow)

        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label.setGeometry(QtCore.QRect(20, 10, 69, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setGeometry(QtCore.QRect(150, 10, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 210, 113, 20))
        self.lineEdit_2.setPlaceholderText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 595, 554))
        self.scrollAreaWidgetContents.setObjectName ("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 641, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Automated System Inventory"))
        self.pushButton.setText(_translate("MainWindow", "Edit"))
        self.label_2.setText(_translate("MainWindow", "RC Small"))
        self.label.setText(_translate("MainWindow", "Item Name"))
        self.label_3.setText(_translate("MainWindow", "Number of Stocks"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Stocks and Price"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Profit"))


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):              # ++++
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.openWindow)

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui     = Ui_editWindow()
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.pushButton_2.clicked.connect(self.updateWindow)

    def updateWindow(self): 
        self.lineEdit.setText(self.ui.lineEdit.text())
# or ???
        self.lineEdit_2.setText(self.ui.lineEdit.text())     


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow)
    MainWindow = MyWindow()
    MainWindow.show()
    sys.exit(app.exec_())    