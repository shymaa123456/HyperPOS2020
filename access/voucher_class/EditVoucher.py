import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_EditVoucher(QtWidgets.QDialog):
    GV_REFUNDABLE = 0
    GV_RECHARGABLE = 0
    GV_MULTIUSE = 0

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
            self.FN_GET_sponsor()

            self.CMB_CouponStatus.addItems(["Inactive", "Active"])
            self.FN_getData()
            self.FN_getDatabyID()
            self.CMB_CouponDes.activated[str].connect(self.FN_getDatabyID)
            self.checkBox_Multi.toggled.connect(self.FN_multiuse)
            self.checkBox_rechange.toggled.connect(self.FN_Rechangable)
            self.checkBox_refundable.toggled.connect(self.FN_Refundable)


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
        sql = "SELECT COMPANY_ID FROM VOUCHER_BRANCH where GV_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_SELECT_branch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO , STATUS FROM VOUCHER_BRANCH where GV_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records


    def FN_SELECT_section(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT SECTION_ID , STATUS FROM VOUCHER_SECTION where GV_ID = %s"
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
        sql_select_branch = "SELECT BRANCH_NO FROM SYS_USER_BRANCH where USER_ID='"+CL_userModule.user_name+"'"
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

    def FN_check_section(self, index):
        self.FN_unCheckedALLsection()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT SECTION_ID FROM SYS_USER_SECTION where USER_ID='"+CL_userModule.user_name+"'"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_section():
                if row[0] == row1[0]:
                    items = self.Qcombo_section.findText(row[0])
                    for item in range(items + 2):
                        if int(row1[1]) == 1:
                            self.Qcombo_section.setChecked(i)
            i = i + 1
        mycursor.close()

    def FN_unCheckedALL(self):
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM SYS_USER_BRANCH where USER_ID='" + CL_userModule.user_name + "'"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            self.Qcombo_branch.unChecked(i)
            i += 1

    def FN_unCheckedALLsection(self):
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT SECTION_ID FROM SYS_USER_SECTION where USER_ID='" + CL_userModule.user_name + "'"
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
            try:
                self.conn = db1.connect()
                mycursor = self.conn.cursor()
                mycursor.execute("SELECT SECTION_DESC , SECTION_ID FROM SECTION")
                records = mycursor.fetchall()
                print(records)
                for row, val in records:
                    for bra in self.FN_AuthSectionUser():
                        if val in bra:
                            self.Qcombo_section.addItem(row, val)
                mycursor.close()
            except:
                print(sys.exc_info())

    def FN_AuthSectionUser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_ID FROM SYS_USER_SECTION where USER_ID='" + CL_userModule.user_name + "'")
        records = mycursor.fetchall()
        return records

    def FN_GET_sponsor(self):
        # Todo: method for fills the sponsor combobox
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SPONSER_NAME,SPONSER_ID FROM SPONSER")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_sponser.addItem(row, val)
        mycursor.close()

    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT GV_DESC,GV_ID FROM VOUCHER")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()

    def FN_getDatabyID(self):
         try:
            self.branch_list = []
            self.new_branch_list = []
            indx = self.CMB_CouponDes.currentData()
            self.labe_id.setText(str(indx))
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            sql_select_Query = "SELECT * FROM VOUCHER where GV_ID = %s"
            x = (indx,)
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            self.LE_desc_1.setText(record[1])
            self.LE_desc_2.setValue(float(record[4]))

            self.CMB_CouponStatus.setCurrentIndex(int(record[20]))

            datefrom = record[12]
            xfrom = datefrom.split("-")
            self.dfrom = QDate(int(xfrom[2]), int(xfrom[1]), int(xfrom[0]))
            self.Qdate_from.setDate(self.dfrom)

            dateto = record[13]
            xto = dateto.split("-")
            d = QDate(int(xto[2]), int(xto[1]), int(xto[0]))
            self.Qdate_to.setDate(d)


            if int(record[14])==1:
                self.checkBox_refundable.setChecked(True)
            else:
                self.checkBox_refundable.setChecked(False)
            if int(record[15])==1:
                self.checkBox_rechange.setChecked(True)
            else:
                self.checkBox_rechange.setChecked(False)
            if int(record[16])==1:
                self.checkBox_Multi.setChecked(True)
            else:
                self.checkBox_Multi.setChecked(False)
            self.FN_check_section(indx)
            self.FN_check_company(indx)
            self.FN_check_branch(indx)
            sql_select = "select * from SPONSER where SPONSER_ID=( SELECT SPONSER_ID FROM VOUCHER_SPONSOR where GV_ID = %s)"
            x = (indx,)
            mycursor.execute(sql_select, x)
            record = mycursor.fetchone()
            self.Qcombo_sponser.setCurrentText(record[2])

            self.branch_list.clear()
            if len(self.Qcombo_branch.currentData()) > 0:
                for i in self.Qcombo_branch.currentData():
                    self.branch_list.append(i)

         except:
             print(sys.exc_info())

    def FN_multiuse(self):
        if self.checkBox_Multi.isChecked():
            self.GV_MULTIUSE=1
        else:
            self.GV_MULTIUSE=0

    def FN_Rechangable(self):
        if self.checkBox_rechange.isChecked():
            self.GV_RECHARGABLE=1
        else:
            self.GV_RECHARGABLE=0

    def FN_Refundable(self):
        if self.checkBox_refundable.isChecked():
            self.GV_REFUNDABLE=1
        else:
            self.GV_REFUNDABLE=0

    def FN_editAction(self):
        try:
            if len(self.Qcombo_company.currentData()) == 0 or len(self.Qcombo_branch.currentData()) == 0 or len(
                    self.LE_desc_1.text().strip()) == 0 or len(self.Qcombo_section.currentData()) == 0 :
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                if self.Qdate_to.dateTime()<self.Qdate_from.dateTime():
                    QtWidgets.QMessageBox.warning(self, "Done", "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                elif self.Qdate_from.dateTime()<self.dfrom:
                    QtWidgets.QMessageBox.warning(self, "Done", "تاريخ الانشاء الجديد يجب ان يكون اكبر او يساوي تاريخ الانشاء قبل التعديل")

                else:
                    mycursor = self.conn.cursor()
                    creationDate = str(datetime.today().strftime('%d-%m-%Y'))
                    sql = "update VOUCHER set GV_DESC='" + self.LE_desc_1.text().strip() +",GV_RECHARGE_VALUE="++",GV_REFUNDABLE="+self.GV_REFUNDABLE+",GV_RECHARGABLE="+self.GV_RECHARGABLE+",GV_MULTIUSE=" +self.GV_MULTIUSE+ ",POSC_CUST_ID="+self.LE_desc_5.text().strip()+" ,GV_CHANGED_BY='" + CL_userModule.user_name + "',GV_CHANGE_ON='" + creationDate + "',GV_VALID_FROM='" + self.Qdate_from.dateTime().toString(
                        'dd-MM-yyyy') + "',GV_VALID_TO='" + self.Qdate_to.dateTime().toString(
                        'dd-MM-yyyy') + "',GV_STATUS='" + str(
                        self.CMB_CouponStatus.currentIndex()) + "' where GV_ID='" + str(
                        self.CMB_CouponDes.currentData()) + "'"
                    mycursor.execute(sql)

        except:
            print(sys.exc_info())




