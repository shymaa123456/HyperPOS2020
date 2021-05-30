from PyQt5 import QtWidgets, uic, QtCore
import sys

from PyQt5.QtWidgets import QWidget ,QDialog  ,qApp
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ui(QtWidgets.QMainWindow):
    status="opened"
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Login1.ui', self)
        self.show()

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.textEdit = self.findChild(QtWidgets.QTextEdit, 'textEdit')

        self.button.clicked.connect(self.on_click)
        

    #         self.w.hide()

    def on_click(self):
        status="ioeccccccc"
        self.w = Ui2(parent=self)
        mytext = self.textEdit.toPlainText()
        #         print(mytext)
        if not self.w.isVisible():
            self.w.label.setText(mytext)
            self.w.setWindowFlag(QtCore.Qt.Tool)
            self.w.show()
            self.status="opened"
        else:
            self.w.label.setText(mytext)
            self.status="update"

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                #                 print('changeEvent: Minimised')
                self.w.close()
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                self.w.show()
        #       print('changeEvent: Normal/Maximised/FullScreen')
        QtWidgets.QWidget.changeEvent(self, event)
        

class Ui2(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(Ui2, self).__init__()
        uic.loadUi('Login2.ui', self)
        self.setWindowTitle('Main Window')

        self.label = self.findChild(QtWidgets.QLabel, 'label')
        
        self.parent = parent
       
        print(self.parent.status)
        
        if self.parent.status == "opened":
            self.parent.status = "if opened"
            #self.show()
        elif self.parent.status == "opend" :
            print("reload")
            self.parent.status == "elif opend"
            
        #print("dsffd",super(Ui, self).parent().status)
        #print("dsffd",self.parent().status)

#         self.show()

        
    def changeEvent(self, event):
        
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                #                 print('changeEvent: Minimised')
                self.w2.close()
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                self.w2.show()
        #                 print('changeEvent: Normal/Maximised/FullScreen')
        QtWidgets.QWidget.changeEvent(self, event)
""" 
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
"""



def main():
        app = QApplication(sys.argv)
        window = Ui()
        app.exec_()
        
        

if __name__ == '__main__':
    main()
   