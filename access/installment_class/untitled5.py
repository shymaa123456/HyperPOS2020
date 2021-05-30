# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:55:20 2021

@author: mustafa
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 08:16:24 2021
https://gist.github.com/MalloyDelacroix/2c509d6bcad35c7e35b1851dfc32d161
@author: mustafa
"""

import sys
from PyQt5 import QtCore, QtWidgets ,uic
from PyQt5.QtWidgets import QWidget ,QDialog  ,qApp
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#status = "not opend"
#closed="not closed"
class MainWindow(QWidget):

    switch_window = QtCore.pyqtSignal(str)
    status = "not opend"
    
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Main Window')
        
        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        
        self.button.clicked.connect(self.switch)
        #self.button.switch_window.connect(self.switch)

        layout.addWidget(self.button)

        self.setLayout(layout)
        self.updatesEnabled()
        self.show()
                
    def switch(self):
        
        #self.switch_window.emit(self.line_edit.text()).

        print("selfVisi",self.isVisible())
        #print("selfhi",self.isHidden()())
        wtwo = WindowTwo( self.line_edit.text() ,self )
        wtwo.newtext=self.line_edit.text()
        #global status
        if self.status == "not opend" :
            wtwo.setWindowFlags(wtwo.windowFlags() | Qt.Window)
            #print("wtwo",wtwo.isVisible())
            print("open new")
            #wtwo.show()
            
            self.status="opend"
        elif self.status == "opend" :
            #wtwo.close()
            #wtwo.show()
            #wtwo.setUpdatesEnabled(True)
            #self.wtwo.setWindowFlag(QtCore.Qt.Tool)

            wtwo.label.setText(self.line_edit.text())
            wtwo.update()
            wtwo.newtext=self.line_edit.text()
            
            #wtwo.show()
            

            #wtwo.refresh(self.line_edit.text())
            print("update")
            print("satus else ", self.status)
            #super(WindowTwo ,self ).update(self.line_edit.text() ,self) 

        #wtwo.update()
        #self.updatesEnabled()
        
        
class WindowTwo(QWidget):
    newtext = "not text"
    
    def __init__(self , text ,  *args ):
        QWidget.__init__(self, *args )
        uic.load
        #self.data = text
        #self.refresh( text)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle('Window Two')
        self.newtext = text
        print("newtext",text)
        print("WindowTwo",self.isVisible())
        print("selfVisi WindowTwo",self.isVisible())

        layout = QtWidgets.QGridLayout()
        print(text)
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)
        if self.parent().status == "not opend" :
            self.show()
        elif self.parent().status == "opend" :
            print("reload")
        #self.show()
        #self.layout().removeWidget(self,layout)
        
        # Apply layout to widget
        #widget = QWidget()
        #widget.setLayout(layout)
        #widget.show()
        #self.update()
        print("update",self.updatesEnabled())
        
    
    # close application event
    def closeEvent(self, event):
        #global newtext
        print("newtext",self.newtext)
        #print("self.data",self.data)


        self.label.setText(self.newtext)
        print("event",event)
        
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit Application?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.parent().status = "not opend"
            #QApplication.quit()
            #quit()
            
        else:
            event.ignore()    
            
     
     # close application event
    def update(self):
       print("update function")  
       #print("status_windowstwo",self.status)
       #self.label.setText(self.data)
       #print(self.data)
       
       self.refresh(self.newtext)

       #close()
       #self.show()

    def refresh(self,text):
        """
        self.setWindowTitle('Window Two')
        #self.data = text
        print("WindowTwo",self.isVisible())
        print("selfVisi WindowTwo",self.isVisible())

        layout = QtWidgets.QGridLayout()
        print(text)
        self.label = QtWidgets.QLabel()
        
        #self.labelText(self,self.data)
        

        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)
        layout.addWidget(self.button)
        """
            
        
        if self.parent().status == "not opend" :
            #self.label.setText(self.data)
            #self.setLayout(layout)
            self.show()
        elif self.parent().status == "opend" :
            print("refresh FUN",text)
            
            
            #self.show()
            #self.label.setText(text)
            #self.label.repaint()
            #self.updateGeometry()
            #self.setLayout(layout)
            #self.repaint()
            #self.updateMicroFocus()
            #self.show()
            #self.label.setText(self.data)
            #self.button.setText(self.data)
            #layout.repaint()
            #self.labelText(self,self.data)
            #self.updateGeometry()
            #self.repaint()
            #self.updatesEnabled()
            #self.update()
            #self.label.repaint()
            #layout.label.setText(self.data)
            #self.repaint()
            #self.updateGeometry()
            #self.setLayout(None)
            #self.setLayout(sd)
            
            print("refresh FUN text oflbel ",self.label.text())
            self.newtext=str(self.label.text()   )
            

     # +++    
    def labelText(self, WindowTwo, value):
        self.label.setText(str(value))     

class Login(QWidget):

    #switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.button)

        self.setLayout(layout)
        
        self.show()

    def login(self):
        mainw = MainWindow(self)
        mainw.setWindowFlags(mainw.windowFlags() | Qt.Window)
        #mainw.close()
        mainw.show()


def main():
        app = QApplication(sys.argv)
        window = Login()
        app.exec_()
        
        

if __name__ == '__main__':
    main()

