from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_editWindow(object):
    def setupUi(self, editWindow):
        editWindow.setObjectName("editWindow")
        editWindow.setEnabled(True)
        editWindow.resize(400, 350)
        editWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(editWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 20, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 270, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 270, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 67, 13))   # (10, 60, 47, 13)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 60, 113, 20)) # (70, 60, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        editWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(editWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        editWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(editWindow)
        self.statusbar.setObjectName("statusbar")
        editWindow.setStatusBar(self.statusbar)

        self.retranslateUi(editWindow)
        self.lineEdit.textEdited['QString'].connect(self.label_2.setText)
        self.pushButton.clicked.connect(self.label_2.clear)
        self.pushButton.clicked.connect(self.lineEdit.clear)                 # +++

        QtCore.QMetaObject.connectSlotsByName(editWindow)

    def retranslateUi(self, editWindow):
        _translate = QtCore.QCoreApplication.translate
        editWindow.setWindowTitle(_translate("editWindow", "MainWindow"))
        self.label.setText(_translate("editWindow", "EDIT FORM"))
        self.pushButton.setText(_translate("editWindow", "Clear"))
        self.pushButton_2.setText(_translate("editWindow", "Update"))
        self.label_2.setText(_translate("editWindow", "Coke"))
        self.lineEdit.setPlaceholderText(_translate("editWindow", "Item Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    editWindow = QtWidgets.QMainWindow()
    ui = Ui_editWindow()
    ui.setupUi(editWindow)
    editWindow.show()
    sys.exit(app.exec_())