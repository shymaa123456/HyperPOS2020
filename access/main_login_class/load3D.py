from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from pathlib import Path
class load3(object):
    def __init__(self, x):
        self.x = 0
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        filename = self.dirname + '/test.ui'
        loadUi(filename, self)
        self.buttonBox.accepted.connect(self.accept)
        #     #self.buttonBox.accepted.connect(MainWindow.close)
        self.buttonBox.rejected.connect(self.close)
        #
        #     self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self)
    # def setupUi(self, MainWindow):
    #
    #     MainWindow.setObjectName("MainWindow")
    #     MainWindow.resize(283, 340)
    #     self.centralwidget = QtWidgets.QWidget(MainWindow)
    #     self.centralwidget.setObjectName("centralwidget")
    #     self.label = QtWidgets.QLabel(self.centralwidget)
    #     self.label.setGeometry(QtCore.QRect(20, 40, 71, 31))
    #     font = QtGui.QFont()
    #     font.setPointSize(18)
    #     self.label.setFont(font)
    #     self.label.setAlignment(QtCore.Qt.AlignCenter)
    #     self.label.setObjectName("label")
    #     self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
    #     self.lineEdit.setGeometry(QtCore.QRect(90, 47, 113, 20))
    #     self.lineEdit.setObjectName("lineEdit")
    #     font = QtGui.QFont()
    #     font.setPointSize(18)
    #     self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
    #     self.buttonBox.setGeometry(QtCore.QRect(120, 260, 156, 23))
    #
    #     self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    #     self.buttonBox.setObjectName("buttonBox")
    #     MainWindow.setCentralWidget(self.centralwidget)
    #     self.menubar = QtWidgets.QMenuBar(MainWindow)
    #     self.menubar.setGeometry(QtCore.QRect(0, 0, 283, 26))
    #     self.menubar.setObjectName("menubar")
    #     MainWindow.setMenuBar(self.menubar)
    #     self.statusbar = QtWidgets.QStatusBar(MainWindow)
    #     self.statusbar.setObjectName("statusbar")
    #     MainWindow.setStatusBar(self.statusbar)
    #
    #     self.buttonBox.accepted.connect(self.accept)
    #     #self.buttonBox.accepted.connect(MainWindow.close)
    #     self.buttonBox.rejected.connect(MainWindow.close)
    #
    #     self.retranslateUi(MainWindow)
    #     QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def accept(self):
        try:
            self.x = self.lineEdit.text()
        #self.close()
        except Exception as err:
            print(err)

    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "Image properties"))
    #     self.label.setText(_translate("MainWindow", "X:"))