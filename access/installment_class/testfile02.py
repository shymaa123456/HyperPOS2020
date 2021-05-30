import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget ,QDialog
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from testfile01 import MainWindow1
# Subclass QMainWindow to customize your application's main window
class MainWindow(QWidget):

        def __init__(self):
                super().__init__()

                self.initUI()

        def initUI(self):

                self.setWindowTitle("Check Distance Travelled By Vehicles")

                self.vehicleNamelbl = QLabel('VehicleName : ')
                self.vehicleNamecombo = QComboBox()
                self.vehicleNamecombo.addItem('SwitftDzire')

                self.dateEdit    = QDateEdit()
                self.dateEdit.__init__(calendarPopup=True)
                self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
                self.dateEdit.editingFinished.connect(lambda: date_method())

                self.petrolCB = QCheckBox('Petrol')
                self.petrolCB.setChecked(True)
                self.dieselCB = QCheckBox('Diesel')
                self.dieselCB.setChecked(False)

                self.petrolCB.stateChanged.connect(self.checkpetrolCB)
                self.dieselCB.stateChanged.connect(self.checkdieselCB)

                self.submitBtn    = QPushButton('Submit ')
                # adding action to the date when enter key is pressed
                self.submitBtn.clicked[bool].connect(self.collecInput)

                grid = QGridLayout()
                grid.setSpacing(10)

                grid.addWidget(self.vehicleNamelbl,1,0)
                grid.addWidget(self.vehicleNamecombo,1,1)
                grid.addWidget(self.dateEdit,1,2)
                grid.addWidget(self.petrolCB,1,3)
                grid.addWidget(self.dieselCB,1,4)
                grid.addWidget(self.submitBtn,1,5)

                # geometry of the main window
                qtRectangle = self.frameGeometry()
                # center point of screen
                centerPoint = QDesktopWidget().availableGeometry().center()
                # move rectangle's center point to screen's center point
                qtRectangle.moveCenter(centerPoint)
                 # top left of rectangle becomes top left of window centering it
                self.move(qtRectangle.topLeft())

                self.setLayout(grid)
                self.show()

                # method called by date edit 
                def date_method():
                        print('Inside date_method')
                        # getting the date 
                        value = self.dateEdit.date()
                        print(value)
                        print(value.toPyDate())

        def checkpetrolCB(self,checked):
                if checked :
                        print('Petrol Vehicle Is Selected')
                        self.OdFlag = 1
                else:
                        print('Petrol Vehicle Is De-Selected')

        def checkdieselCB(self,checked):
                if checked :
                        print('Diesel Vehicle Is Selected')
                        self.OdFlag = 2
                else:
                        print('Diesel Vehicle Is De-Selected')

        def collecInput(self) :

                print('Submit Button Pressed!! Inputs Selected')

                print(self.vehicleNamecombo.currentText())
                print(self.dateEdit.date().toPyDate())

                if self.petrolCB.isChecked() == True and self.dieselCB.isChecked() == False :
                    print('Petrol Vehicle Is Selected')

                if self.dieselCB.isChecked() == True and self.petrolCB.isChecked() == False :
                    print('Diesel Vehicle Is Selected')

                if self.petrolCB.isChecked() == True and self.dieselCB.isChecked() == True :
                    print('Both Petrol And Diesel Vehicle Are Selected')
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setText('Select Either Petrol Or Diesel')
                    msgBox.setWindowTitle("Alert PopUp")
                    returnValue = msgBox.exec_()
                    return

                # Call A Module To Get The List Of Files Present As per The Input
                vehicleFileList = [ 'dist_SwitftDzire_CityA.13OCT2020','dist_SwitftDzire_CityB.13OCT2020','dist_SwitftDzire_CityC.13OCT2020']

                print('Back to collecInput')
                print(vehicleFileList)
                print('Num Of Files Found : '+str(len(vehicleFileList)))

                numOfFiles = len(vehicleFileList)

                if numOfFiles == 0 : # No Files Have Been Detected
                    print('No Files Found')
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setText('No Files Found')
                    msgBox.setWindowTitle("Alert PopUp")
                    returnValue = msgBox.exec_()

                else: # Atleast 1 File Is Detected
                    print('Populating table entries')
                    table = MyTable(vehicleFileList, numOfFiles, 2, self)
                    # add Qt.Window to table's flags 
                    table.setWindowFlags(table.windowFlags() | Qt.Window)
                    table.show()
                    mainw = MainWindow1(self)
                    
                    mainw.setWindowFlags(mainw.windowFlags() | Qt.Window)
                    mainw.show()
                    
class MyTable(QTableWidget):
        def __init__(self, vehicleFileList, *args):
                QTableWidget.__init__(self, *args)
                self.data = vehicleFileList
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.resizeColumnsToContents()
                self.resizeRowsToContents()
                self.horizontalHeader().setStretchLastSection(False)
                self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.setHorizontalHeaderLabels(['Available Vehicle Data Files','Missing Files'])

                print('Inside MyTable')
                print(vehicleFileList)

                rowCount=0

                for item in vehicleFileList :
                        print(item)
                        self.setItem(rowCount,0,QTableWidgetItem(item))
                        rowCount+=1


"""
class MainWindow1(QWidget):

    #switch_window = QtCore.pyqtSignal(str)

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Main Window')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #self.resizeColumnsToContents()
        #self.resizeRowsToContents()
        #self.horizontalHeader().setStretchLastSection(False)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.setHorizontalHeaderLabels(['Available Vehicle Data Files','Missing Files'])

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        #self.button.clicked.connect(self.switch)
        layout.addWidget(self.button)

        self.setLayout(layout)
        #self.show()
"""      
def main():
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
        #setQuitOnLastWindowClosed
      #QApplication.quitOnLastWindowClosed()

if __name__ == '__main__':
    main()