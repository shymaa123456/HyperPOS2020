from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.comboBox1 = QComboBox(self.centralwidget)
        self.comboBox1.setGeometry(QtCore.QRect(310, 150, 171, 31))
        self.comboBox1.setObjectName(_fromUtf8("comboBox1"))
        self.comboBox1.addItem(_fromUtf8(""))
        self.comboBox1.addItem(_fromUtf8(""))
        self.comboBox1.addItem(_fromUtf8(""))
        self.comboBox1.addItem(_fromUtf8(""))
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(310, 240, 171, 41))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.comboBox1.setItemText(0, _translate("MainWindow", "select", None))
        self.comboBox1.setItemText(1, _translate("MainWindow", "a", None))
        self.comboBox1.setItemText(2, _translate("MainWindow", "b", None))
        self.comboBox1.setItemText(3, _translate("MainWindow", "c", None))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "select", None))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "p", None))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "q", None))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "r", None))
        self.comboBox_2.setEnabled(0)
        self.comboBox1.currentIndexChanged.connect(self.test)

    def test(self):
        s = str(self.comboBox1.currentText())
        res = ['aa', 'bb', 'cc', 'dd']

        if (s == "- - select - -"):
            self.comboBox_2.setEnabled(0)
            self.comboBox_2.setCurrentIndex(0)
        elif (len(s) == 0):
            self.comboBox_2.setEnabled(1)
            self.comboBox_2.clear()
            self.comboBox_2.addItem("- - select - -")
            self.comboBox_2.addItem("New Checklist")
        else:
            self.comboBox_2.setEnabled(1)
            self.comboBox_2.clear()
            self.comboBox_2.addItem("- - select - -")
            self.comboBox_2.addItem("New Checklist")
            self.comboBox_2.addItems(res)
            self.comboBox_2.currentIndexChanged.connect(self.test1)

    def test1(self):
        print("Hello")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
