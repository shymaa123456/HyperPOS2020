from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from data_connection.h1pos import db1

from access.main_login_class.main import *

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QMessageBox

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

        """ checked combobox sample >>> Branch"""
        self.Qcombo_branch2 = CheckableComboBox(self)
        self.Qcombo_branch2.setGeometry(621, 44, 179, 18)
        self.Qcombo_branch2.setLayoutDirection(Qt.RightToLeft)
        self.Qcombo_branch2.setStyleSheet("background-color: rgb(198, 207, 199)")
        # self.Qcombo_branch.hide()

        """ checked combobox sample """
        self.Qcombo_cust_group2 = CheckableComboBox(self)
        self.Qcombo_cust_group2.setGeometry(621, 68, 179, 18)
        self.Qcombo_cust_group2.setLayoutDirection(Qt.RightToLeft)  # RightToLeft)
        # self.Qcombo_cust_group2.lineEdit().setAlignment(Qt.AlignRight)
        self.Qcombo_cust_group2.setStyleSheet("background-color: rgb(198, 207, 199)")
        # self.Qcombo_cust_group.hide()

        """ checked combobox sample >>> sponsor"""
        self.Qcombo_sponsor2 = CheckableComboBox(self)
        self.Qcombo_sponsor2.setGeometry(621, 92, 179, 18)
        self.Qcombo_sponsor2.setLayoutDirection(Qt.RightToLeft)
        self.Qcombo_sponsor2.setStyleSheet("background-color: rgb(198, 207, 199)")
        # self.Qcombo_sponsor.hide()

        try:
             self.Qcombo_sponsor2.activated.connect(self.handleActivated)
             # self.Qcombo_sponsor2.currentIndexChanged().connect(self.handleActivated)

             self.FN_GET_Company()
             self.FN_GET_Branch()
             self.FN_GET_CustomerGroup()

             self.FN_GET_sponser()
             self.FN_GET_promotion_type()

             self.FN_GET_department()
             self.updatestatecombo()

             self.FN_GET_MAGAZINE()

              # department
             self.Qcombo_department.activated[str].connect(self.updatestatecombo)
             self.Qbtn_search.clicked.connect(self.FN_SEARCH_BARCODES)
        except:
            print("An exception occurred")


    # SEARCH BUTTON
    def FN_SEARCH_BARCODES(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_company.addItems(row)
        mycursor.close()

    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_company.addItems(row)
        mycursor.close()

    def FN_GET_Branch(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_DESC_A FROM BRANCH")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_branch2.addItems(row)
        mycursor.close()

    def FN_GET_CustomerGroup(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT CG_DESC FROM CUSTOMER_GROUP")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            # self.Qcombo_cust_group.addItems(row)
            self.Qcombo_cust_group2.addItems(row)
        mycursor.close()

    def FN_GET_MAGAZINE(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT MAGAZINE_DESC FROM MAGAZINE")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_magazine.addItems(row)
        mycursor.close()

    def FN_GET_sponser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SPONSER_NAME , SPONSER_ID FROM SPONSER WHERE SPONSER_STATUS = '1' ")
        records = mycursor.fetchall()
        print(records)
        for row, VAL in records:
            # self.Qcombo_sponsor2.addItems(row)
            self.Qcombo_sponsor2.addItem(row , VAL)
            self.Qline_promotion.text = VAL
        mycursor.close()

        ##################################################
        # ##  test data
        # # self.Qtable_promotion.
        #
        # # data = 'Recordset back from postgis'
        # nb_row = len(records)
        # nb_col = 3
        # self.Qtable_promotion.setRowCount(nb_row)
        # self.Qtable_promotion.setColumnCount(nb_col)
        #
        # combo_box_options = ["Option", "Option 2: val", "Option 3: val"]
        # combo = QComboBox()
        # for t in combo_box_options:
        #     combo.addItem(t)
        #
        # for row in range(nb_row):
        #     for col in range(nb_col-1):
        #         item = QTableWidgetItem(str(records[row][col]))
        #         self.Qtable_promotion.setItem(row, col, item)
        #
        #     # self.Qtable_promotion.setCellWidget(row, 2, combo)
        #     # combo.setCurrentIndex(1)
        # # self.Qtable_promotion.setHorizontalHeaderLabels([u'Column1', u'Column2'])
        #
        # self.Qtable_promotion.setHorizontalHeaderLabels([u'SPONSER_NAME', u'SPONSER_ID', u'combo'])
        # self.Qtable_promotion.cellClicked.connect(self.cell_was_clicked)
        #
        # self.Qtable_promotion.resizeColumnsToContents()
        #
        # ##################################################
        #
        # # self.table = QtGui.QTableWidget()
        # # self.table.setColumnCount(3)
        # # self.setCentralWidget(self.table)
        # # data1 = ['row1', 'row2', 'row3', 'row4']
        # # data2 = ['1', '2.0', '3.00000001', '3.9999999']
        # # combo_box_options = ["Option 1", "Option 2", "Option 3"]
        #
        # # self.table.setRowCount(4)
        #
        # # for index in range(nb_row):
        # #     # item1 = QtGui.QTableWidgetItem(data1[index])
        # #     # self.table.setItem(index, 0, item1)
        # #     # item2 = QtGui.QTableWidgetItem(data2[index])
        # #     # self.table.setItem(index, 1, item2)
        # #     combo = QtGui.QComboBox()
        # #     for t in combo_box_options:
        # #         combo.addItem(t)
        # #     self.Qtable_promotion.setCellWidget(index, 2, combo)
        #
        #     ##################################################

    def handleActivated(self, index):
        print(self.Qcombo_sponsor2.itemText(index))
        print(self.Qcombo_sponsor2.itemData(index))
        QMessageBox.about(self, self.Qcombo_sponsor2.itemText(index), self.Qcombo_sponsor2.itemData(index))

    def cell_was_clicked(self,  row, column):
        # index = self.Qtable_promotion.currentIndex()
        # NewIndex = self.Qtable_promotion.model().index(index.row(), 0)
        # print(NewIndex)
        # print(index)
        print("Row %d and Column %d was clicked" % (row, column))
        item = self.Qtable_promotion.item(row, column)
        print(item.text())

    def FN_GET_promotion_type(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT PROMT_NAME_AR FROM PROMOTION_TYPE order by PROMOTION_TYPE_ID*1 ")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_promotion.addItems(row)
        mycursor.close()

    # department
    def FN_GET_department(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT DEPARTMENT_DESC ,DEPARTMENT_ID FROM DEPARTMENT")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_department.addItem(row, val)
        mycursor.close()

    # section
    def FN_GET_section(self, id):
        self.Qcombo_section.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_DESC ,SECTION_ID FROM SECTION where DEPARTMENT_ID = '" + id + "'")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_section.addItem(row, val)
        mycursor.close()

    # section update
    def updatestatecombo(self):
        indx = self.Qcombo_department.currentData()
        self.FN_GET_section(indx)
        indx = self.Qcombo_section.currentData()
        self.Qcombo_classification.clear()
        self.FN_GET_classification(indx)
        self.Qcombo_section.activated[str].connect(self.updateBMCcombo)


    # BMC
    def FN_GET_classification(self, id):
        self.Qcombo_classification.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BMC_LEVEL4_DESC , BMC_LEVEL4 FROM BMC_LEVEL4 where SECTION_ID =" + id + "")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_classification.addItem(row, val)
        mycursor.close()

    # BMC update
    def updateBMCcombo(self):
        indx = self.Qcombo_section.currentData()
        self.FN_GET_classification(indx)
