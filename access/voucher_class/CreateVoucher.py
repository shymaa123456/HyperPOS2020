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
    GV_REFUNDABLE=0
    GV_RECHARGABLE=0
    GV_MULTIUSE=0
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
            self.btn_search.clicked.connect(self.FN_search)
        except:
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




    def FN_Create_Voucher(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            creationDate = str(datetime.today().strftime('%d-%m-%Y'))
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

                else:
                    value = randint(0, 1000000000000)
                    sql = "INSERT INTO VOUCHER (GV_DESC, GVT_ID, GV_BARCODE, GV_VALUE, GV_NET_VALUE, GV_CREATED_BY, GV_CREATED_ON, GV_VALID_FROM, GV_VALID_TO, GV_REFUNDABLE, GV_RECHARGABLE,GV_MULTIUSE, POSC_CUST_ID, GV_PRINTRED,GV_STATUS) VALUES (%s, %s,%s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s) "
                    val = (self.LE_desc.text().strip(),'1',"HVOU"+bin(value),self.LE_desc_2.text().strip(),self.LE_desc_2.text().strip(),CL_userModule.user_name,creationDate,self.Qdate_from.dateTime().toString('dd-MM-yyyy'),self.Qdate_to.dateTime().toString('dd-MM-yyyy'),self.GV_REFUNDABLE,self.GV_RECHARGABLE,self.GV_REFUNDABLE,self.LE_desc_5.text().strip(),'0','0')

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
                    db1.connectionCommit(self.conn)
                    QtWidgets.QMessageBox.warning(self, "Done", "رقم قسيمه الشراء هو " + str(id))
                    self.label_num.setText(str(id))
                    mycursor.close()
        except:
            print(sys.exc_info())

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
            else:
                self.desc_13.setText("العميل غير موجود")
            mycursor.close()
        except:
            print(sys.exc_info())










