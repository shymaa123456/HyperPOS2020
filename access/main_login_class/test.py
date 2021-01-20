import sys
from PyQt4 import QtGui


class Widget(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(parent)

        grid = QtGui.QGridLayout()
        grid.setSpacing(3)

        self.edit_first = QtGui.QLineEdit()
        grid.addWidget(QtGui.QLabel('Question 1'), 1, 0)
        grid.addWidget(self.edit_first, 1, 1)

        #   add layout for second widget
        self.edit_second = QtGui.QLineEdit()
        grid.addWidget(QtGui.QLabel('Question 2'), 2, 0)
        grid.addWidget(self.edit_second, 2, 1)

        apply_button = QtGui.QPushButton('Apply', self)
        apply_button.clicked.connect(self.close)

        grid.addWidget(apply_button, 4, 3)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)

    def return_strings(self):
        #   Return list of values. It need map with str (self.lineedit.text() will return QString)
        return map(str, [self.q1Edit.text(), self.q2Edit.text()])

    @staticmethod
    def get_data(parent=None):
        dialog = Widget(parent)
        dialog.exec_()
        return dialog.return_strings()


def main():
    app = QtGui.QApplication([])
    window = Widget()
    print
    window.get_data()  # window is value from edit field


if __name__ == '__main__':
    main()

