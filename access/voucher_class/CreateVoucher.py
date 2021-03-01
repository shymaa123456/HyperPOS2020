import sys
from pathlib import Path
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_CreateVoucher(QtWidgets.QDialog):

    def __init__(self):
        super(CL_CreateVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()


    def FN_LOADUI(self):
        try:
            filename = self.dirname + '/createVoucher.ui'
            loadUi(filename, self)

            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(20, 15, 271, 25)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_branch = CheckableComboBox(self)
            self.Qcombo_branch.setGeometry(20, 55, 271, 25)
            self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_section = CheckableComboBox(self)
            self.Qcombo_section.setGeometry(20, 90, 271, 25)
            self.Qcombo_section.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.FN_GET_Company()
            self.FN_GET_Branch()
            self.FN_GET_Section()
            datefrom = str(datetime.today().strftime('%Y-%m-%d'))
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setMinimumDate(d)
            self.Qdate_to.setMinimumDate(d)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        except :
            print(sys.exc_info())





    def FN_GET_Company(self):
        #Todo: method for fills the company combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    def FN_GET_Section(self):
        #Todo: method for fills the section combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_DESC , SECTION_ID FROM SECTION")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_section.addItem(row, val)
        mycursor.close()



    def FN_GET_Branch(self):
        i = 0
        try:
            # Todo: method for fills the Branch combobox
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH")
            records = mycursor.fetchall()
            for row, val in records:
                for bra in self.FN_AuthBranchUser():
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1
            mycursor.close()
        except:
            print(sys.exc_info())



    def FN_AuthBranchUser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_NO FROM SYS_USER_BRANCH where USER_ID='" + CL_userModule.user_name + "'")
        records = mycursor.fetchall()
        return records




