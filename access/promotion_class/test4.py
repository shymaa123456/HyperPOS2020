import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        super().setFixedSize(700, 100)
        mainLayout = QHBoxLayout()
        self.model = QStandardItemModel()

        # states
        self.combostates = QComboBox()
        self.combostates.setFixedSize(325, 50)
        self.combostates.setFont(QFont('', 12))
        self.combostates.setModel(self.model)

        # states
        self.combocities = QComboBox()
        self.combocities.setFixedSize(325, 50)
        self.combocities.setFont(QFont('', 12))
        self.combocities.setModel(self.model)

        # add data

        for k, v in data.items():
            state = QStandardItem(k)
            self.model.appendRow(state)
            for value in v:
                city = QStandardItem(value)
                state.appendRow(city)

        self.combostates.currentIndexChanged.connect(self.updatestatecombo)
        self.updatestatecombo(0)


        mainLayout.addWidget(self.combostates)
        mainLayout.addWidget(self.combocities)
        self.setLayout(mainLayout)

    def updatestatecombo(self, index):
        indx = self.model.index(index, 0, self.combostates.rootModelIndex())
        self.combocities.setRootModelIndex(indx)
        self.combocities.setCurrentIndex(0)


data = {'egypt': ['cairo', 'giza', 'asyuit'],
        'suaidia': ['aaaa', 'aass', 'dddd'],
        'qatar': ['www1', '3333', '333']
        }

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
