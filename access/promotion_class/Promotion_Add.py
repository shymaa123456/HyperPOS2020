from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from data_connection.h1pos import db1

from access.main_login_class.main import *

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


import sys

""" 
# new check-able combo box- in test
class CheckableComboBox(QComboBox):

    # constructor
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

    count = 0

    # action called when item get checked
    def do_action(self):

        CL_create_promotion.label.setText("Checked number : " + str(self.count))

        # when any item get pressed

    def handleItemPressed(self, index):

        # getting the item
        item = self.model().itemFromIndex(index)

        # checking if item is checked
        if item.checkState() == Qt.Checked:

            # making it unchecked
            item.setCheckState(Qt.Unchecked)

            # if not checked
        else:
            # making the item checked
            item.setCheckState(Qt.Checked)

            self.count += 1

            # call the action
            self.do_action()
"""


class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res


class CL_create_promotion(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    def __init__(self):
        super(CL_create_promotion, self).__init__()

        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/promotion_ui'
        self.conn = db1.connect()





    def FN_LOAD_CREATE_PROM(self):
        filename = self.dirname + '/Promotion_create.ui'

        loadUi(filename, self)

        """ checked combobox sample """
        self.Qcombo_cust_group2 = CheckableComboBox(self)
        self.Qcombo_cust_group2.setGeometry(400, 79, 179, 18)
        self.Qcombo_cust_group2.setLayoutDirection(Qt.RightToLeft)
        # self.Qcombo_cust_group2.lineEdit().setAlignment(Qt.AlignRight)


        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.FN_GET_CustomerGroup()
        self.FN_GET_MAGAZINE()
        self.FN_GET_department()
        self.FN_GET_promotion_sponser()
        self.FN_GET_promotion_type()



    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_company.addItems( row )
        mycursor.close()
    def FN_GET_Branch(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT BRANCH_DESC_A FROM BRANCH" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_branch.addItems( row )
        mycursor.close()
    def FN_GET_CustomerGroup(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT CG_DESC FROM CUSTOMER_GROUP" )
        records = mycursor.fetchall()
        print(records)




        for row in records:
            self.Qcombo_cust_group.addItems(row)
            self.Qcombo_cust_group2.addItems(row)
        mycursor.close()







    def FN_GET_MAGAZINE(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT MAGAZINE_DESC FROM MAGAZINE" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_magazine.addItems( row )
        mycursor.close()
    def FN_GET_department(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT DEPARTMENT_DESC FROM DEPARTMENT" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_sponsor_2.addItems( row )
        mycursor.close()
    def FN_GET_promotion_sponser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT SPONSER_NAME FROM SPONSER" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_sponsor.addItems( row )
        mycursor.close()
    def FN_GET_promotion_type(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT PROMT_NAME_AR FROM PROMOTION_TYPE order by PROMOTION_TYPE_ID*1 " )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_promotion.addItems( row )
        mycursor.close()

