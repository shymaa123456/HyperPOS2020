import sys
from pathlib import Path
from random import randint
import mysql
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime

from presentation.Themes.Special_StyleSheet import label_num, desc_5


class CL_CreateVoucher(QtWidgets.QDialog):
    GV_REFUNDABLE=0
    GV_RECHARGABLE=0
    GV_MULTIUSE=0
    searchpos=False
    VGType="2"

    def __init__(self):
        super(CL_CreateVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()

    #Todo: method for load ui of createVoucher
    def FN_LOADUI(self):
        try:
            filename = self.dirname + '/createVoucher.ui'
            loadUi(filename, self)
            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(320, 35, 271, 15)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.Qcombo_branch = CheckableComboBox(self)
            self.Qcombo_branch.setGeometry(320, 60, 271, 15)
            self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.Qcombo_section = CheckableComboBox(self)
            self.Qcombo_section.setGeometry(320, 85, 271, 15)
            self.Qcombo_section.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.FN_GET_Company()
            self.FN_GET_Branch()
            self.FN_GET_Section()
            self.FN_GET_sponsor()
            self.checkBox_Multi.toggled.connect(self.FN_multiuse)
            self.checkBox_rechange.toggled.connect(self.FN_Rechangable)
            self.checkBox_refundable.toggled.connect(self.FN_Refundable)
            datefrom = str(datetime.today().strftime('%Y-%m-%d'))
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setMinimumDate(d)
            self.Qdate_to.setMinimumDate(d)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_createVoucher.clicked.connect(self.FN_Create_Voucher)
            self.LE_desc_5.textChanged.connect(self.FN_search)
            self.radioButton.clicked.connect(self.FN_SelectSponser)
            self.radioButton_2.clicked.connect(self.FN_Selectprepaid)
            # Set Style
            self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except:
            print(sys.exc_info())

    #Todo: method to make voucher type sponser
    def FN_SelectSponser(self):
        self.Qcombo_sponser.setEnabled(True)
        self.LE_desc_3.setEnabled(True)
        self.LE_desc_6.setEnabled(True)
        self.LE_desc_7.setEnabled(True)
        self.VGType = "2"

    #Todo: method to make voucher prepaid
    def FN_Selectprepaid(self):
        self.Qcombo_sponser.setEnabled(False)
        self.LE_desc_3.setEnabled(False)
        self.LE_desc_6.setEnabled(False)
        self.LE_desc_7.setEnabled(False)
        self.VGType = "3"

    #Todo: method for fills the company combobox
    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    #Todo: method for fills the section combobox
    def FN_GET_Section(self):
        print(CL_userModule.section)
        try:
            for row, val,row1,val1 in CL_userModule.section:
                self.Qcombo_section.addItem(val, row)
        except:
            print(sys.exc_info())

    # Todo: method for fills the Branch combobox
    def FN_GET_Branch(self):
        i = 0
        try:
            for row, val in CL_userModule.branch:
                self.Qcombo_branch.addItem(val, row)
                i += 1
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

    # Todo: method to make voucher multi use
    def FN_multiuse(self):
        if self.checkBox_Multi.isChecked():
            self.GV_MULTIUSE=1
        else:
            self.GV_MULTIUSE=0

    # Todo: method to make voucher Rechangable
    def FN_Rechangable(self):
        if self.checkBox_rechange.isChecked():
            self.GV_RECHARGABLE=1
        else:
            self.GV_RECHARGABLE=0

    # Todo: method to make voucher Refundable
    def FN_Refundable(self):
        if self.checkBox_refundable.isChecked():
            self.GV_REFUNDABLE=1
        else:
            self.GV_REFUNDABLE=0

    # Todo: method to create voucher
    def FN_Create_Voucher(self):
        try:
            self.conn = db1.connect()
            self.conn.autocommit = False
            mycursor = self.conn.cursor()
            self.conn.start_transaction()
            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
            if len(self.Qcombo_company.currentData()) == 0 or len(self.Qcombo_branch.currentData()) == 0 or len(self.Qcombo_section.currentData()) == 0 or len(self.Qcombo_sponser.currentData()) == 0 or len(
                    self.LE_desc.text().strip()) == 0 or len(self.LE_desc_3.text().strip()) == 0 or len(
                    self.LE_desc_2.text().strip()) == 0 :
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                indx = self.LE_desc.text().strip()
                sql_select_Query = "select * from VOUCHER where GV_DESC = %s"
                x = (indx,)
                mycursor.execute(sql_select_Query, x)
                record = mycursor.fetchone()
                if mycursor.rowcount > 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")
                elif self.Qdate_to.dateTime() < self.Qdate_from.dateTime():
                        QtWidgets.QMessageBox.warning(self, "Done",
                                                      "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                elif self.searchpos == False:
                        QtWidgets.QMessageBox.warning(self, "Done",
                                                      "العميل غير موجود")
                elif self.VGType=="2":
                    if float(self.LE_desc_3.text())+float(self.LE_desc_6.text())!=100:
                       QtWidgets.QMessageBox.warning(self, "Done",
                                                  "يرجى مراجعة نسبة الدعم")
                else:
                    sql0 = "  LOCK  TABLES    Hyper1_Retail.VOUCHER   WRITE , " \
                           "    Hyper1_Retail.VOUCHER_SPONSOR   WRITE , " \
                           "    Hyper1_Retail.VOUCHER_BRANCH   WRITE , "\
                           "    Hyper1_Retail.VOUCHER_SECTION   WRITE  "
                    mycursor.execute(sql0)
                    value = randint(0, 1000000000000)
                    sql = "INSERT INTO VOUCHER (GV_DESC, GVT_ID, GV_BARCODE, GV_VALUE, GV_NET_VALUE, GV_CREATED_BY, GV_CREATED_ON, GV_VALID_FROM, GV_VALID_TO, GV_REFUNDABLE, GV_RECHARGABLE,GV_MULTIUSE, POSC_CUST_ID, GV_PRINTRED,GV_STATUS) VALUES (%s, %s,%s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s) "
                    val = (self.LE_desc.text().strip(),self.VGType,"HVOU"+bin(value),self.LE_desc_2.text().strip(),self.LE_desc_2.text().strip(),CL_userModule.user_name,creationDate,self.Qdate_from.dateTime().toString('yyyy-MM-dd'),self.Qdate_to.dateTime().toString('yyyy-MM-dd'),self.GV_REFUNDABLE,self.GV_RECHARGABLE,self.GV_REFUNDABLE,self.LE_desc_5.text().strip(),'0','0')
                    mycursor.execute(sql, val)
                    indx = self.LE_desc.text()
                    mycursor.execute("SELECT * FROM VOUCHER Where GV_DESC = '" + indx + "'")
                    c = mycursor.fetchone()
                    id = c[0]
                    sql3 = "INSERT INTO VOUCHER_SPONSOR (SPONSER_ID,GV_ID,SPONSOR_SHARE,HYPER_SHARE,NOTES) VALUES (%s,%s,%s,%s,%s)"
                    val3 = (
                            self.Qcombo_sponser.currentData(), id,
                            self.LE_desc_6.text(),
                            self.LE_desc_3.text(),
                            self.LE_desc_7.text().strip())
                    mycursor.execute(sql3, val3)
                    for j in range(len(self.Qcombo_company.currentData())):
                        for i in range(len(self.Qcombo_branch.currentData())):
                            sql3 = "INSERT INTO VOUCHER_BRANCH (COMPANY_ID,BRANCH_NO,GV_ID,STATUS) VALUES (%s,%s,%s,%s)"
                            val3 = (
                                self.Qcombo_company.currentData()[j], self.Qcombo_branch.currentData()[i],
                                id,
                                '1')
                            mycursor.execute(sql3, val3)
                        for a in range(len(self.Qcombo_section.currentData())):

                            sql3 = "INSERT INTO VOUCHER_SECTION (GV_ID,SECTION_ID,STATUS) VALUES (%s,%s,%s)"
                            val3 = (
                                id, self.Qcombo_section.currentData()[a],
                                '1')
                            mycursor.execute(sql3, val3)
                    sql00 = "  UNLOCK   tables    "
                    mycursor.execute(sql00)
                    db1.connectionCommit(self.conn)
                    mycursor.close()
                    QtWidgets.QMessageBox.warning(self, "Done", "رقم قسيمه الشراء هو " + str(id))
                    self.label_num.setText(str(id))
        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            # reverting changes because of exception
            self.conn.rollback()
        finally:
            # closing database connection.
            if self.conn.is_connected():
                mycursor.close()
                self.conn.close()
                print("connection is closed")

    # Todo: method to search about clint
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
                self.searchpos = True
            else:
                self.desc_13.setText("العميل غير موجود")
                self.searchpos = False
            mycursor.close()
        except:
            print(sys.exc_info())
