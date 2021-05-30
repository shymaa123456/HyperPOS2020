from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
import sys


class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2, self).__init__()
        uic.loadUi('Grid2.ui', self)
        self.setWindowTitle('Main Window')

        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.table2 = self.findChild(QtWidgets.QTableWidget, 'tableWidget')


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Grid1.ui', self)
        self.show()

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.save_btn = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.table = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.textEdit = self.findChild(QtWidgets.QTextEdit, 'textEdit')

        self.button.clicked.connect(self.on_click)

        self.save_btn.clicked.connect(self.save)

        self.w = Ui2()

    def on_click(self):
        mytext = self.textEdit.toPlainText()

        if not self.w.isVisible():
            self.w.label.setText(mytext)
            self.w.setWindowFlag(QtCore.Qt.Tool)
            self.w.show()
        else:
            self.w.label.setText(mytext)

    def save(self):
        model = self.table.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data[row].append(str(model.data(index)))

        if not self.w.isVisible():
            self.w.setWindowFlag(QtCore.Qt.Tool)
            self.w.show()

        numcols = len(data[0])
        numrows = len(data)
        self.w.table2.setColumnCount(numcols)
        self.w.table2.setRowCount(numrows)
        for row in range(numrows):
            for column in range(numcols):
                self.w.table2.setItem(row, column, QTableWidgetItem((data[row][column])))

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                self.w.close()
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                self.w.show()
        QtWidgets.QWidget.changeEvent(self, event)


app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()