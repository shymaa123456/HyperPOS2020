# -*- coding: utf-8 -*-
"""
Created on Mon May 17 09:57:36 2021

@author: mustafa
"""

from PyQt5 import QtCore, QtGui, QtWidgets

value = 0

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(890, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 100, 500, 250))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 370, 500, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        ############
        self.pushButton.clicked.connect(self.OpenInput)
        ############

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Value"))
        self.pushButton.setText(_translate("MainWindow", "Go to input window"))


    ##############################
    # Show second window for input

    def OpenInput(self, MainWindow):
        Dialog.show()

    ##############################

    # +++    
    def labelText(self, MainWindow, value):
        self.label.setText(str(value)) 


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(889, 598)

        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(210, 170, 471, 141))
        font = QtGui.QFont()
        font.setPointSize(33)
        self.spinBox.setFont(font)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox.setObjectName("spinBox")

        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(209, 360, 471, 61))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(310, 460, 271, 71))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        ############
        self.pushButton.clicked.connect(self.CloseAndRefresh)
        ############

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(210, 40, 471, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.horizontalSlider.valueChanged['int'].connect(self.spinBox.setValue)
        self.spinBox.valueChanged['int'].connect(self.horizontalSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Back to first Window"))
        self.label.setText(_translate("Dialog", "Value"))


    #######################################################
    # Close second window and refresh label on first window

    def CloseAndRefresh(self):
        global value
        value = self.spinBox.value()
        print(value) #checking input

        # +++
        ui.labelText(MainWindow, value)

        ##################################################
        # The refresh of the outputting label on the     #
        # MainWindow should be started at this position. #
        ##################################################

        #Dialog.close()

    #######################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    Dialog = QtWidgets.QDialog()
    dia = Ui_Dialog()
    dia.setupUi(Dialog)

    sys.exit(app.exec_())