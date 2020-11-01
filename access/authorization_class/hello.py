from PyQt5.QtWidgets import QPushButton

print("hello")
from PyQt5 import QtWidgets, QtCore

class Test(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.listWidget.setGeometry( QtCore.QRect( 10, 10, 211, 291 ) )
        for i in range( 10 ):
            item = QtWidgets.QListWidgetItem( "Item %i" % i )
            self.listWidget.addItem( item )

        self.layout.addWidget( self.listWidget )

        button = QPushButton( 'PyQt5 button', self )
        button.clicked.connect( self.printItemText)
        self.layout.addWidget( button )
        self.setLayout( self.layout )
        self.listWidget.item(0).setSelected(True)
        self.listWidget.item(2).setSelected(True)
    def printItemText(self):
        items = self.listWidget.selectedItems()

        x = []
        for i in range(len(items)):
           x.append(str(self.listWidget.selectedItems()[i].text()))

        print (x)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = Test()
    form.show()
    app.exec_()