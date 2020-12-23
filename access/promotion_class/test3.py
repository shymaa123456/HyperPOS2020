import sys
from PyQt5.QtWidgets import *

class ComboBox(QComboBox):
    def setCurrentIndex(self, ix):
        self.blockSignals(True)
        QComboBox.setCurrentIndex(self, ix)
        self.blockSignals(False)

class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())

        l = [str(i) for i in range(15)]
        cb1 = ComboBox(self)
        cb1.addItems(l)

        cb2 = ComboBox(self)
        cb2.addItems(l)

        cb3 = ComboBox(self)
        cb3.addItems(l)

        cb4 = ComboBox(self)
        cb4.addItems(l)

        cb1.currentIndexChanged.connect(cb2.setCurrentIndex)
        cb2.currentIndexChanged.connect(cb3.setCurrentIndex)
        cb3.currentIndexChanged.connect(cb4.setCurrentIndex)

        self.layout().addWidget(cb1)
        self.layout().addWidget(cb2)
        self.layout().addWidget(cb3)
        self.layout().addWidget(cb4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())