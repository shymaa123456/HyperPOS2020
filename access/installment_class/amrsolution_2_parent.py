# -*- coding: utf-8 -*-
"""
Created on Tue May 25 13:32:45 2021

@author: mustafa
"""

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Ui2(QtWidgets.QMainWindow):
    def __init__(self, parent ,text):
        super(Ui2, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        uic.loadUi('Login2.ui', self)
        self.setWindowTitle('Main Window')
       
        self.label = self.findChild(QtWidgets.QLabel, 'label')
       
        self.updateparentButton = self.findChild(QtWidgets.QPushButton, 'updateparentButton')

        self.updateparentButton.clicked.connect(self.UpdateParent_FUN)

        self.parent = parent
        self.text=text
        print("child",self.parent.status)
        
        #self.parent.status = "opend"
        self.label.setText(text)
        print("label text ",self.label.text())
        #self.show()

    def UpdateParent_FUN(self):
        self.parent.Refresh_ParenContentFromChilds("Ui2")
        print("UI2",self.parent.label_Main.text())

        self.parent.label_Main.setText(self.label.text())

    # close application event
    def closeEvent(self, event):
        #global newtext
        #print("newtext",self.newtext)
        #print("self.data",self.data)


        #self.label.setText(self.newtext)
        #print("event",event)
        
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit Application?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.parent.status = "not opend"
            #QApplication.quit()
            #self.w.close()
            #quit()
            
        else:
            event.ignore()
            
    """    
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
#                 print('changeEvent: Minimised')
                self.parent.status = 'not opened'
                print(self.parent.status)
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                self.parent.status = 'opened again'
                print(self.parent.status)
#                 print('changeEvent: Normal/Maximised/FullScreen')
        QtWidgets.QWidget.changeEvent(self, event)

#         self.show()
       """


class Ui3(QtWidgets.QMainWindow):
    def __init__(self, parent ,text):
        super(Ui3, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        uic.loadUi('Login2.ui', self)
        self.setWindowTitle('scond Window')
       
        self.label = self.findChild(QtWidgets.QLabel, 'label')
       
        self.updateparentButton = self.findChild(QtWidgets.QPushButton, 'updateparentButton')

        self.updateparentButton.clicked.connect(self.UpdateParent_FUN)

        self.parent = parent
        self.text=text
        print("child",self.parent.status_scond)
        #self.parent.status = "opend"
        self.label.setText(text)
        
        #self.parent.isVisibleTo(False)
        
        print("U3 label text ",self.label.text())
        #self.show()

    def UpdateParent_FUN(self):
        self.parent.Refresh_ParenContentFromChilds("Ui3")
        print("UI3",self.parent.label_Main.text())
        self.parent.label_Main.setText(self.label.text())
    # close application event
    def closeEvent(self, event):
        #global newtext
        #print("newtext",self.newtext)
        #print("self.data",self.data)


        #self.label.setText(self.newtext)
        #print("event",event)
        
        #reply = QMessageBox.question(self, 'Message',"Are you sure to quit Application?", QMessageBox.Yes, QMessageBox.No)

        #if reply == QMessageBox.Yes:
        self.parent.status_scond = "not opend"
            #QApplication.quit()
            #self.w.close()
            #quit()
            
        #else:
        #    event.ignore()
            
    """    
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
#                 print('changeEvent: Minimised')
                self.parent.status = 'not opened'
                print(self.parent.status)
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                self.parent.status = 'opened again'
                print(self.parent.status)
#                 print('changeEvent: Normal/Maximised/FullScreen')
        QtWidgets.QWidget.changeEvent(self, event)

#         self.show()
       """


class Ui(QtWidgets.QMainWindow):
    status = 'not opend'
    status_scond = 'not opend'


    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Login1.ui', self)
        self.show()
       
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.scondbtn = self.findChild(QtWidgets.QPushButton, 'openScond')

        self.textEdit = self.findChild(QtWidgets.QTextEdit, 'textEdit')

        self.label_Main = self.findChild(QtWidgets.QLabel, 'label_Main')

        self.button.clicked.connect(self.on_click)
        self.scondbtn.clicked.connect(self.on_click_scond)

        #print("init_UI",self.label_Main.text())


#         self.w.hide()
    
    def on_click_scond(self):
        
        mytext = self.textEdit.toPlainText()
#         print(mytext)
        print("parent",self.status_scond)
        
        """
        if not self.w.isVisible():
            self.w.label.setText(mytext)
            self.w.setWindowFlag(QtCore.Qt.Tool)
            self.w.show()
            
        else:
            self.w.label.setText(mytext)
        """
        if self.status_scond == "not opend" :
            print("if  not opend")
            self.status_scond = "opend"
            self.w3 = Ui3(parent=self ,text=mytext)

            self.w3.label.setText(mytext)
            self.w3.setWindowFlag(QtCore.Qt.Tool)
            self.w3.show()
            
        
            #self.status = "opend"
            #self.w.show()
        elif self.status_scond == "opend" :
            print("reload")
            #self.w = Ui2(parent=self ,text=mytext)
            
            self.w3.label.setText(mytext)
            #self.w.close()
    
    def Refresh_ParenContentFromChilds(self,fromscreen):
        print("Refresh_ParenContentFromChilds",fromscreen) 
        #print("UI",self.label_Main.text())
        

        
    def on_click(self):
        
        mytext = self.textEdit.toPlainText()
#         print(mytext)
        print("parent",self.status)
        
        """
        if not self.w.isVisible():
            self.w.label.setText(mytext)
            self.w.setWindowFlag(QtCore.Qt.Tool)
            self.w.show()
            
        else:
            self.w.label.setText(mytext)
        """
        if self.status == "not opend" :
            print("if  not opend")
            self.status = "opend"
            self.w = Ui2(parent=self ,text=mytext)

            self.w.label.setText(mytext)
            self.w.setWindowFlag(QtCore.Qt.Tool)
            self.w.show()
            
        
            #self.status = "opend"
            #self.w.show()
        elif self.status == "opend" :
            print("reload")
            #self.w = Ui2(parent=self ,text=mytext)
            
            self.w.label.setText(mytext)
            #self.w.close()
    """       
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
#                 print('changeEvent: Minimised')
                self.w.close()
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                self.w.show()
#                 print('changeEvent: Normal/Maximised/FullScreen')
        QtWidgets.QWidget.changeEvent(self, event)
        """
    
    # close application event
    def closeEvent(self, event):
        #global newtext
        #print("newtext",self.newtext)
        #print("self.data",self.data)


        #self.label.setText(self.newtext)
        #print("event",event)
        
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit Application?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            #self.parent().status = "not opend"
            QApplication.quit()
            #self.w.close()
            #self.w3.close()
            #quit()
            
        else:
            event.ignore()    

    
def main():
        app = QApplication(sys.argv)
        window = Ui()
        app.exec_()
        
        

if __name__ == '__main__':
    main()
