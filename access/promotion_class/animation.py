# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

from PyQt5 import QtCore, QtGui, QtWidgets

class LoginButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(60, 60)

        # if self.ff == '1':
        #     self.color1 = QtGui.QColor(9, 88, 91)  # (240, 53, 218)
        #     self.color2 = QtGui.QColor(74, 88, 245)  # (61, 217, 245)
        # else:
        #     self.color1 = QtGui.QColor(9, 44, 91)  # (240, 53, 218)
        #     self.color2 = QtGui.QColor(74, 50, 245)  # (61, 217, 245)

        self.color1 = QtGui.QColor(9,44,91)#(240, 53, 218)
        self.color2 = QtGui.QColor(74, 50, 245)#(61, 217, 245)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:21px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)
        # self.setStyleSheet("color: red ")#background-color: red")

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)
        # self.setStyleSheet("color: blue ")#background-color: blue")



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)

    for i in range(5):
        button = LoginButton()
        button.setText("Login")
        lay.addWidget(button)
    lay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
