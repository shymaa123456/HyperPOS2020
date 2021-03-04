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


class CL_EditVoucher(QtWidgets.QDialog):
    valueType=""
    valueData=""
    serialCount = ""
    MultiCount = ""
    MultiUse = ""
    movement=0
    serial_num=0
    usage=0
    branch_list = []
    new_branch_list = []
    multiusage=0
    serial_type=0

    def __init__(self):
        super(CL_EditVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()

    def FN_LOADUI(self):
        try:
            filename = self.dirname + '/editVoucher.ui'
            loadUi(filename, self)
            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(10, 100, 271, 25)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_branch = CheckableComboBox(self)
            self.Qcombo_branch.setGeometry(10, 140, 271, 25)
            self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_section = CheckableComboBox(self)
            self.Qcombo_section.setGeometry(10, 180, 271, 25)
            self.Qcombo_section.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.FN_GET_Company()
            self.FN_GET_Branch()
            self.FN_GET_Section()
            self.CMB_CouponStatus.addItems(["Inactive", "Active"])

        except:
            print(sys.exc_info())





    def FN_GET_Company(self):
        #Todo: method for fills the company combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    def FN_GET_Branch(self):
        # Todo: method for fills the Branch combobox
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


    def FN_SELECT_company(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT COMPANY_ID FROM COUPON_BRANCH where COUPON_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_SELECT_branch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO , STATUS FROM COUPON_BRANCH where COUPON_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_check_company(self, indx):
        mycursor = self.conn.cursor()
        sql_select_company = "SELECT COMPANY_ID  FROM COMPANY"
        mycursor.execute(sql_select_company)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_company():
                if row[0] == row1[0]:
                    items = self.Qcombo_company.findText(row[0])
                    for item in range(items + 2):
                        self.Qcombo_company.setChecked(i)
            i = i + 1
        mycursor.close()

    def FN_check_branch(self, index):
        self.FN_unCheckedALL()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM BRANCH"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_branch():
                if row[0] == row1[0]:
                    items = self.Qcombo_branch.findText(row[0])
                    for item in range(items + 2):
                        if int(row1[1]) == 1:
                            self.Qcombo_branch.setChecked(i)
            i = i + 1
        mycursor.close()

    def FN_unCheckedALL(self):
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM SYS_USER where USER_ID='" + CL_userModule.user_name + "'"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            self.Qcombo_branch.unChecked(i)
            i += 1

    def FN_GetMathchBranch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO FROM COUPON_BRANCH where COUPON_ID = %s and STATUS = 1"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_AuthBranchUser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_NO FROM SYS_USER_BRANCH where USER_ID='" + CL_userModule.user_name + "'")
        records = mycursor.fetchall()
        return records

    def FN_GET_Section(self):
        # Todo: method for fills the section combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_DESC , SECTION_ID FROM SECTION")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_section.addItem(row, val)
        mycursor.close()
