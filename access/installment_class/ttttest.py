import sys
from PyQt5 import QtCore, QtWidgets

from PyQt5.QtWidgets import QWidget ,QDialog


class MainWindow(QDialog):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('Main Window')

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        self.button.clicked.connect(self.switch(self.line_edit.text()))
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()
        
    #def switch(self):
    #    self.switch_window.emit(self.line_edit.text())

    def switch(self, text):
        self.window_two = WindowTwo(text)
        self.window_two.switch_window.connect(self.show_window_two)

        #self.window.close()
        #self.window_two.show()
        #ex = self.login
        self.window_two.setModal(True)
        self.window_two.exec()


class WindowTwo(QDialog):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, text):
        QDialog.__init__(self)
       
        self.setWindowTitle('Window Two')

        layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        #self.window.close()
        #self.window_two.show()
        #ex = self.login
        self.window_two.setModal(True)
        self.window_two.exec()
        
class Login(QDialog):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)


        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()
        
    def login(self):
        #self.switch_window.emit()
        #window = MainWindow()
        #self.window.switch_window.connect(self.show_window_two)
       # self.login.close()
        #self.window.show()
        #window.setModal(True)
        #window.exec()
        self.mydialog = MainWindow()
        self.mydialog.switch_window.connect(self.show_main)
        self.mydialog.setModal(True)
        self.mydialog.exec()


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        #self.login.show()
        self.login.setModal(True)
        self.login.exec()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_window.connect(self.show_window_two)
       # self.login.close()
        #self.window.show()
        self.window.setModal(True)
        self.window.exec()
        
    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        #self.window.close()
        #self.window_two.show()
        #ex = self.login
        self.window_two.setModal(True)
        self.window_two.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()