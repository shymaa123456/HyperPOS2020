import collections
import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.uic import loadUi

from access.Checkable import CheckableComboBox
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_EditVoucher(QtWidgets.QDialog):
    GV_REFUNDABLE = 0
    GV_RECHARGABLE = 0
    GV_MULTIUSE = 0
    recharge = 0
    branch_list = []
    new_branch_list = []
    section_list = []
    new_section_list = []
    searchpos=False
    oldValue=""
    oldlist = []
    newlist = []
    row=""

    def __init__(self):
        super(CL_EditVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()

    # Todo: method to load ui of editVoucher
    def FN_LOADUI(self):
        try:
            filename = self.dirname + '/editVoucher.ui'
            loadUi(filename, self)
            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(340, 160, 271, 25)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.Qcombo_branch = CheckableComboBox(self)
            self.Qcombo_branch.setGeometry(340, 200, 271, 25)
            self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.Qcombo_section = CheckableComboBox(self)
            self.Qcombo_section.setGeometry(340, 240, 271, 25)
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
            self.BTN_editCoupon.clicked.connect(self.FN_editAction)
            self.LE_desc_5.textChanged.connect(self.FN_search)
            # Set Style
            # self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except:
            print(sys.exc_info())

    # Todo: method for fills the company combobox
    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    # Todo: method for fills the Branch combobox
    def FN_GET_Branch(self):
            i = 0
            try:
                for row, val in CL_userModule.branch:
                    self.Qcombo_branch.addItem(val, row)
                    i += 1
            except:
                print(sys.exc_info())

    # Todo: method to get company of voucher
    def FN_SELECT_company(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT COMPANY_ID FROM VOUCHER_BRANCH where GV_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method to get branches of voucher
    def FN_SELECT_branch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO , STATUS FROM VOUCHER_BRANCH where GV_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method to get sections of voucher
    def FN_SELECT_section(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT SECTION_ID , STATUS FROM VOUCHER_SECTION where GV_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method to check company assgined to voucher
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

    # Todo: method to check branch assgined to voucher
    def FN_check_branch(self, index):
        self.FN_unCheckedALL()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM SYS_USER_BRANCH where USER_ID='" + CL_userModule.user_name + "'"
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

    # Todo: method to check section assgined to voucher
    def FN_check_section(self, index):
        self.FN_unCheckedALLsection()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT SECTION_ID FROM SYS_USER_SECTION where USER_ID='" + CL_userModule.user_name + "'"
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

    # Todo: method to refresh Qcombo_branch
    def FN_unCheckedALL(self):
        i = 0
        for row in CL_userModule.branch:
            self.Qcombo_branch.unChecked(i)
            i += 1

    # Todo: method to refresh Qcombo_section
    def FN_unCheckedALLsection(self):
        i = 0
        for row in CL_userModule.section:
            self.Qcombo_section.unChecked(i)
            i += 1

    # Todo: method to get branch of voucher
    def FN_GetMathchBranch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO FROM VOUCHER_BRANCH where GV_ID = %s and STATUS = 1"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method for fills the section combobox
    def FN_GET_Section(self):
        try:
            for row, val,row1,val1 in CL_userModule.section:
                self.Qcombo_section.addItem(val, row)
        except:
            print(sys.exc_info())

    # Todo: method for fills the sponsor combobox
    def FN_GET_sponsor(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SPONSER_NAME,SPONSER_ID FROM SPONSER")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_sponser.addItem(row, val)
        mycursor.close()

    # Todo: method for get all voucher
    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT GV_DESC,GV_ID FROM VOUCHER where GVT_ID in (2,3)")
        records = mycursor.fetchall()
        for row, val in records:
            self.CMB_CouponDes.addItem(row, val)
        mycursor.close()

    # Todo: method for get data about voucher
    def FN_getDatabyID(self):
        try:
            self.branch_list = []
            self.new_branch_list = []
            self.section_list = []
            self.new_section_list = []
            indx = self.CMB_CouponDes.currentData()
            self.labe_id.setText(str(indx))
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            sql_select_Query = "SELECT * FROM VOUCHER where GV_ID = %s"
            x = (indx,)
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            self.row=str(record[0])
            self.LE_desc_1.setText(str(record[1]))
            self.LE_desc_2.setValue(float(record[4]))
            self.CMB_CouponStatus.setCurrentIndex(int(record[20]))
            self.LE_desc_5.setText(str(record[19]))
            self.FN_search()

            timefrom = record[13]
            tfrom = timefrom.split(":")
            some_time = QtCore.QTime(int(tfrom[0]), int(tfrom[1]), 00)
            self.Qtime_from.setTime(some_time)

            timeto = record[15]
            tto = timeto.split(":")
            some_time = QtCore.QTime(int(tto[0]), int(tto[1]), 00)
            self.Qtime_to.setTime(some_time)

            self.oldValue=record[1]
            datefrom = record[12]
            xfrom = datefrom.split("-")
            self.dfrom = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setDate(self.dfrom)
            self.dfrom = QDateTime(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]), 00, 00, 00, 00)
            dateto = record[14]
            xto = dateto.split("-")
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_to.setDate(d)
            if int(record[16]) == 1:
                self.checkBox_refundable.setChecked(True)
            else:
                self.checkBox_refundable.setChecked(False)
            if int(record[17]) == 1:
                self.checkBox_rechange.setChecked(True)
                self.LE_desc_3.setEnabled(True)
            else:
                self.checkBox_rechange.setChecked(False)
                self.LE_desc_3.setEnabled(False)
            if int(record[18]) == 1:
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
            self.section_list.clear()
            if len(self.Qcombo_branch.currentData()) > 0:
                for i in self.Qcombo_branch.currentData():
                    self.branch_list.append(i)
            if len(self.Qcombo_section.currentData()) > 0:
                for x in self.Qcombo_section.currentData():
                    self.section_list.append(x)
            self.oldlist=self.Qcombo_branch.currentData()
        except:
            print(sys.exc_info())

    # Todo: method to make voucher multiuse
    def FN_multiuse(self):
        if self.checkBox_Multi.isChecked():
            self.GV_MULTIUSE = 1
        else:
            self.GV_MULTIUSE = 0

    # Todo: method to make voucher Rechangable
    def FN_Rechangable(self):
        if self.checkBox_rechange.isChecked():
            self.GV_RECHARGABLE = 1
            self.LE_desc_3.setEnabled(True)
        else:
            self.GV_RECHARGABLE = 0
            self.LE_desc_3.setEnabled(False)

    # Todo: method to make voucher Refundable
    def FN_Refundable(self):
        if self.checkBox_refundable.isChecked():
            self.GV_REFUNDABLE = 1
        else:
            self.GV_REFUNDABLE = 0

    # Todo: method to edit voucher
    def FN_editAction(self):
        try:
            self.FN_search()
            self.newlist = self.Qcombo_branch.currentData()
            if len(self.Qcombo_company.currentData()) == 0 or len(self.Qcombo_branch.currentData()) == 0 or len(
                    self.LE_desc_1.text().strip()) == 0 or len(self.Qcombo_section.currentData()) == 0 or len(
                    self.LE_desc_5.text().strip()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            elif (self.Qdate_from.date() == self.Qdate_to.date()) and int(
                    self.Qtime_from.dateTime().toString('hh')) + int(self.Qtime_from.dateTime().toString('mm')) > int(
                    self.Qtime_to.dateTime().toString('hh')) + int(self.Qtime_to.dateTime().toString('mm')):
                QtWidgets.QMessageBox.warning(self, "خطا", "وقت الانتهاء يجب ان يكون اكبر من او يساوي وقت الانشاء")
            else:
                if self.Qdate_to.dateTime() < self.Qdate_from.dateTime():
                    QtWidgets.QMessageBox.warning(self, "Done",
                                                  "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                elif self.Qdate_from.dateTime() < self.dfrom:
                    QtWidgets.QMessageBox.warning(self, "Done",
                                                  "تاريخ الانشاء الجديد يجب ان يكون اكبر او يساوي تاريخ الانشاء قبل التعديل")
                elif self.searchpos== False :
                    QtWidgets.QMessageBox.warning(self, "Done",
                                                  "العميل غير موجود")
                else:
                    mycursor = self.conn.cursor()
                    creationDate = str(datetime.today().strftime('%Y-%m-%d'))
                    sql = "update VOUCHER set GV_DESC='" + self.LE_desc_1.text().strip() + "',GV_RECHARGE_VALUE='" + self.LE_desc_3.text().strip() + "',GV_REFUNDABLE=" + str(
                        self.GV_REFUNDABLE) + ",GV_RECHARGABLE=" + str(self.GV_RECHARGABLE) + ",GV_MULTIUSE=" + str(
                        self.GV_MULTIUSE) + " ,GV_CHANGED_BY='" + CL_userModule.user_name + "',GV_CHANGE_ON='" + creationDate + "',GV_VALID_FROM='" + self.Qdate_from.dateTime().toString(
                        'yyyy-MM-dd') + "',GV_VALID_TO='" + self.Qdate_to.dateTime().toString(
                        'yyyy-MM-dd') + "',GV_STATUS='" + str(
                        self.CMB_CouponStatus.currentIndex()) + "',POSC_CUST_ID='"+self.LE_desc_5.text().strip()+"' ,GV_TIME_FROM='"+str(self.Qtime_from.dateTime().toString('hh:mm'))+"',GV_TIME_TO='"+str(self.Qtime_to.dateTime().toString('hh:mm'))+"' where GV_ID='" + str(
                        self.CMB_CouponDes.currentData()) + "'"
                    print(sql)
                    mycursor.execute(sql)
                    if len(self.Qcombo_branch.currentData()) > 0:
                        for i in self.Qcombo_branch.currentData():
                            self.new_branch_list.append(i)
                    if len(self.Qcombo_section.currentData()) > 0:
                        for i in self.Qcombo_section.currentData():
                            self.new_section_list.append(i)
                    if len(self.branch_list) > len(self.new_branch_list):
                        for row in self.branch_list:
                            print(row)
                            if row in self.new_branch_list:
                                print("found")
                            else:
                                print("not found")
                                mycursor = self.conn.cursor()
                                sql5 = "update VOUCHER_BRANCH set STATUS= 0 where GV_ID='" + str(
                                    self.CMB_CouponDes.currentData()) + "' and BRANCH_NO = '" + row + "'"
                                mycursor.execute(sql5)
                                print(sql5)
                    else:
                        for row in self.new_branch_list:
                            print(row)
                            if row in self.branch_list:
                                print("found")
                            else:
                                mycursor = self.conn.cursor()
                                mycursor.execute(
                                    "SELECT * FROM VOUCHER_BRANCH where BRANCH_NO='" + row + "' and GV_ID='" + str(
                                        self.CMB_CouponDes.currentData()) + "'")
                                record = mycursor.fetchall()
                                if mycursor.rowcount > 0:
                                    mycursor = self.conn.cursor()
                                    sql8 = "update VOUCHER_BRANCH set STATUS= 1 where GV_ID='" + str(
                                        self.CMB_CouponDes.currentData()) + "' and BRANCH_NO = '" + row + "'"
                                    mycursor.execute(sql8)
                                    print(sql8)
                                else:
                                    mycursor = self.conn.cursor()
                                    sql6 = "INSERT INTO VOUCHER_BRANCH (COMPANY_ID,BRANCH_NO,GV_ID,STATUS) VALUES (%s,%s,%s,%s)"
                                    val6 = (
                                        str(self.Qcombo_company.currentData()[0]), row,
                                        str(self.CMB_CouponDes.currentData()),
                                        '1')
                                    mycursor.execute(sql6, val6)
                    if len(self.section_list) > len(self.new_section_list):
                        for row in self.section_list:
                            print(row)
                            if row in self.new_section_list:
                                print("found")
                            else:
                                print("not found")
                                mycursor = self.conn.cursor()
                                sql5 = "update VOUCHER_SECTION set STATUS= 0 where GV_ID='" + str(
                                    self.CMB_CouponDes.currentData()) + "' and SECTION_ID = '" + row + "'"
                                mycursor.execute(sql5)
                                print(sql5)
                    else:
                        for row in self.new_branch_list:
                            print(row)
                            if row in self.branch_list:
                                print("found")
                            else:
                                mycursor = self.conn.cursor()
                                mycursor.execute(
                                    "SELECT * FROM VOUCHER_SECTION where SECTION_ID='" + row + "' and GV_ID='" + str(
                                        self.CMB_CouponDes.currentData()) + "'")
                                record = mycursor.fetchall()
                                if mycursor.rowcount > 0:
                                    mycursor = self.conn.cursor()
                                    sql8 = "update VOUCHER_SECTION set STATUS= 1 where GV_ID='" + str(
                                        self.CMB_CouponDes.currentData()) + "' and SECTION_ID = '" + row + "'"
                                    mycursor.execute(sql8)
                                    print(sql8)
                                else:
                                    mycursor = self.conn.cursor()
                                    sql6 = "INSERT INTO VOUCHER_SECTION (SECTION_ID,GV_ID,STATUS) VALUES (%s,%s,%s)"
                                    val6 = (
                                        row,
                                        str(self.CMB_CouponDes.currentData()),
                                        '1')
                                    mycursor.execute(sql6, val6)
                    if (self.LE_desc_1.text() != self.oldValue):
                        sql7 = "INSERT INTO SYS_CHANGE_LOG (TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY) VALUES (%s,%s,%s,%s,%s,%s)"
                        val7 = ('VOUCHER', 'GV_DESC', self.oldValue, self.LE_desc_1.text().strip(), creationDate,
                                CL_userModule.user_name)
                        mycursor.execute(sql7, val7)

                    elif collections.Counter(self.Qcombo_branch.currentData()) == collections.Counter(self.oldlist):

                        print("the same list")

                    elif len(collections.Counter(self.Qcombo_branch.currentData())) > len(
                            collections.Counter(self.oldlist)):

                        print(self.Diff(self.newlist, self.oldlist))

                        if len(collections.Counter(self.Qcombo_branch.currentData())) > len(
                                collections.Counter(record)):

                            for row in self.Diff(record, self.newlist):
                                sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

                                val8 = (self.row, 'COUPON_BRANCH', 'STATUS', "null",

                                        "1",

                                        creationDate,

                                        CL_userModule.user_name, row)

                                mycursor.execute(sql8, val8)

                        else:

                            for row in self.Diff(self.oldlist, self.newlist):
                                sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

                                val8 = (self.row, 'COUPON_BRANCH', 'STATUS', "0",

                                        "1",

                                        creationDate,

                                        CL_userModule.user_name, row)

                                mycursor.execute(sql8, val8)


                    elif len(collections.Counter(self.Qcombo_branch.currentData())) < len(
                            collections.Counter(self.oldlist)):

                        print(self.Diff(self.oldlist, self.newlist))

                        for row in self.Diff(self.oldlist, self.newlist):
                            sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

                            val8 = (self.row, 'COUPON_BRANCH', 'STATUS', "1",

                                    "0",

                                    creationDate,

                                    CL_userModule.user_name, row)

                            mycursor.execute(sql8, val8)

                    db1.connectionCommit(self.conn)
                    mycursor.close()
                    self.FN_getDatabyID()
                    QtWidgets.QMessageBox.warning(self, "Done", "Done")

        except:
            print(sys.exc_info())

    # Todo: method to search about customer
    def FN_search(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            name = self.LE_desc_5.text().strip()
            sql_select_Query = "select * from POS_CUSTOMER where POSC_CUST_ID = '" + name + "'"
            mycursor.execute(sql_select_Query)
            records = mycursor.fetchone()
            if mycursor.rowcount > 0:
                self.desc_13.setText(str(records[3]))
                self.searchpos=True
            else:
                self.desc_13.setText("العميل غير موجود")
                self.searchpos=False
            mycursor.close()
        except:
            print(sys.exc_info())

    # Todo: method get diff between two list
    def Diff(self,li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))