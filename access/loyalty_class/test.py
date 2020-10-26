import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QGridLayout, QLabel, QRadioButton


class EricsValidator(QValidator):

    def validate(self, text, position):
        print( 'validate (%s %s)' % (repr(text), repr(position)))
        return (QValidator.Intermediate, text, position)

class Form(QDialog):

    def __init__(self, parent=None):

        super(Form, self).__init__(parent)

        self.lineedit = QLineEdit()

        self.validators = []
        layout = QGridLayout()
        layout.addWidget(self.lineedit, 0, 0, 1, 2)
        for i, (name, validator) in enumerate([
            ("Q&IntValidator"   , QIntValidator(self)   ),
            ("Q&DoubleValidator", QDoubleValidator(self)),
            ("&Eric's Validator", EricsValidator(self)  ),
        ]):
            label  = QLabel(name)
            button = QRadioButton()
            label.setBuddy(button)
            self.validators.append((validator, label, button))
            layout.addWidget(label , i + 1, 0)
            layout.addWidget(button, i + 1, 1)
            label.setBuddy(button)

           # self.connect(button, SIGNAL("clicked()"), self.update)
            button.clicked.connect(self.update)
        self.validators[-1][2].setChecked(True)

        self.setLayout(layout)

        self.setWindowTitle("Validation Tester")

        self.update()

    def update(self):

        for validator, label, button in self.validators:
            if button.isChecked():
                print ('setting validator to', label.text())
                self.lineedit.setValidator(validator)
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()