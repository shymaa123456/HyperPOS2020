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
            self.Qcombo_cust_group.addItems( row )
        mycursor.close()

        #  self.Qcombo_cust_group = CheckableComboBox(self)




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

