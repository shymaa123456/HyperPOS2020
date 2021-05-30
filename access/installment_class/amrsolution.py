# -*- coding: utf-8 -*-
"""
Created on Mon May 24 12:11:18 2021

@author: mustafa
"""

from PyQt5 import QtWidgets, uic, QtCore
import sys

class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2, self).__init__()
        uic.loadUi('Login2.ui', self)
        self.setWindowTitle('Main Window')
        
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        #self.parent().sta
        #print("sdvmnjndvnjdskjsdj",self.parent().status)
        self.show()
        """
        if self.parent().status == "not opend" :
            self.show()
        elif self.parent().status == "opend" :
            print("reload")
       """

class Ui(QtWidgets.QMainWindow):
    #global status
    status = "not opend"
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Login1.ui', self)
        self.show()
       
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.textEdit = self.findChild(QtWidgets.QTextEdit, 'textEdit')
       
        self.button.clicked.connect(self.on_click)
        
        #self.w.hide()
       
    def on_click(self):
        w = Ui2()
        
        
        if self.status == "not opend" :
            self.status="opend"
            w.setWindowFlag(QtCore.Qt.Tool)
            w.show()
            mytext = self.textEdit.toPlainText()
            print(mytext)
           
            w.label.setText(mytext)
            #self.w.setWindowFlags(self.w.windowFlags() | QtCore.Qt.Window)

            #self.w.setWindowFlag(QtCore.Qt.Tool)
            #w.show()
            
            
        elif self.status == "opend" :
            #self.w.setWindowFlag(QtCore.Qt.Tool)
            #self.w.show()
            #wtwo.close()
            #wtwo.show()
            #wtwo.setUpdatesEnabled(True)
            #self.wtwo.setWindowFlag(QtCore.Qt.Tool)

            #self.w = Ui2()
            mytext = self.textEdit.toPlainText()
            print(mytext)
           
            w.label.setText(mytext)
            #self.w.setWindowFlags(self.w.windowFlags() | QtCore.Qt.Window)

            #self.w.setWindowFlag(QtCore.Qt.Tool)
            #self.w.show()
            
            #wtwo.show()

            #wtwo.refresh(self.line_edit.text())
            print("update")
            print("satus else ", self.status)
            #super(WindowTwo ,self ).update(self.line_edit.text() ,self) 

        #wtwo.update()
        #self.updatesEnabled()
        


app = QtWidgets.QApplication(sys.argv)
window = Ui()
#window.setWindowFlags(window.windowFlags() | QtCore.Qt.Window)
sys.exit(app.exec_())