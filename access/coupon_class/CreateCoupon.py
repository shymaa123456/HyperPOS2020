import sys
from pathlib import Path
from random import randint

import mysql
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from presentation.Themes.Special_StyleSheet import label_num, desc_5
from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_CreateCoupon(QtWidgets.QDialog):
    dirname = ''
    valueType=""
    valueData=""
    serialCount=""
    MultiCount=""
    MultiUse=""
    serialType=0
    def __init__(self):
        super(CL_CreateCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()

    # Todo: method to load ui of create coupon
    def FN_LOADUI(self):
        filename = self.dirname + '/createCoupon.ui'
        loadUi(filename, self)
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(360, 35, 271, 25)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(360, 65, 271, 25)
        self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.FN_EnableDiscVal()
        self.checkBox_Multi.toggled.connect(self.FN_endableMultiUser)
        self.radioButton_Value.clicked.connect(self.FN_EnableDiscVal)
        self.radioButton_Percentage.clicked.connect(self.FN_EnablePercentage)
        self.BTN_createCoupon.clicked.connect(self.FN_Create)
        datefrom = str(datetime.today().strftime('%Y-%m-%d'))
        xfrom = datefrom.split("-")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        self.Qdate_from.setMinimumDate(d)
        self.Qdate_to.setMinimumDate(d)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.LE_desc_5.setEnabled(False)
        css_path = Path(__file__).parent.parent.parent
        # Apply Style For Design
        self.label_num.setStyleSheet(label_num)
        self.desc_5.setStyleSheet(desc_5)
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        this_moment = QtCore.QTime.currentTime()
        self.Qtime_from.setMinimumTime(this_moment)

    # Todo: method to make coupon multi use
    def FN_endableMultiUser(self):
        if self.checkBox_Multi.isChecked():
            self.LE_desc_5.setEnabled(True)
            self.LE_desc_4.setEnabled(False)
        else:
            self.LE_desc_5.setEnabled(False)
            self.LE_desc_4.setEnabled(True)

    # Todo: method to make coupon use discount value
    def FN_EnableDiscVal(self):
        self.valueType="COP_DISCOUNT_VAL"
        self.LE_desc_2.setEnabled(True)
        self.LE_desc_3.setEnabled(False)

    # Todo: method to make coupon use percentage value
    def FN_EnablePercentage(self):
        self.valueType="COP_DISCOUNT_PERCENT"
        self.LE_desc_3.setEnabled(True)
        self.LE_desc_2.setEnabled(False)

    # Todo: method for fills the company combobox
    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    # Todo: method for fills the Branch combobox
    def FN_GET_Branch(self):
        i=0
        try:
            for row, val in CL_userModule.branch:
                self.Qcombo_branch.addItem(val, row)
                i += 1
        except:
            print(sys.exc_info())

    # Todo: method for create coupon
    def FN_Create(self):
        try:
            self.conn = db1.connect()
            self.conn.autocommit = False
            mycursor = self.conn.cursor()
            self.conn.start_transaction()

            print(int(self.Qtime_from.dateTime().toString('hh')))

            if len(self.Qcombo_company.currentData())==0 or len(self.Qcombo_branch.currentData())==0 or len(self.LE_desc.text().strip())==0 or len(self.LE_desc_3.text().strip()) == 0 and len(self.LE_desc_2.text().strip()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            elif self.Qdate_to.dateTime() < self.Qdate_from.dateTime():
                QtWidgets.QMessageBox.warning(self, "Done", "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
            elif (self.Qdate_from.date ()==self.Qdate_to.date ()) and int(self.Qtime_from.dateTime().toString('hh'))+int(self.Qtime_from.dateTime().toString('mm'))> int(self.Qtime_to.dateTime().toString('hh'))+int(self.Qtime_to.dateTime().toString('mm')):
                    QtWidgets.QMessageBox.warning(self, "خطا", "وقت الانتهاء يجب ان يكون اكبر من او يساوي وقت الانشاء")

            else:
                if self.checkBox_Multi.isChecked():
                    self.serialCount = "1"
                    self.MultiCount = self.LE_desc_5.text()
                    self.MultiUse = "1"
                    self.serialType=1
                else:
                    self.serialCount = self.LE_desc_4.text()
                    self.MultiCount = "0"
                    self.MultiUse = "0"
                    self.serialType=0
            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
            if self.radioButton_Percentage.isChecked():
                if len(self.LE_desc_3.text().strip()) == 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
                else:
                    self.valueData = self.LE_desc_3.text()
            elif self.radioButton_Value.isChecked():
                if len(self.LE_desc_2.text().strip()) == 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
                else:
                    self.valueData = self.LE_desc_2.text()
            indx = self.LE_desc.text().strip()
            sql_select_Query = "select * from COUPON where COP_DESC = %s "
            x = (indx,)
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            if mycursor.rowcount > 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")
            else:
                sql0 = "  LOCK  TABLES    Hyper1_Retail.COUPON   WRITE , " \
                       "    Hyper1_Retail.COUPON_SERIAL   WRITE , " \
                       "    Hyper1_Retail.COUPON_BRANCH   WRITE  "
                mycursor.execute(sql0)
                id = 0
                print("srial"+self.serialCount)
                sql = "INSERT INTO COUPON (COP_DESC, " + self.valueType + ", COP_SERIAL_COUNT,COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_VALID_FROM, COP_TIME_FROM, COP_VALID_TO, COP_TIME_TO, COP_STATUS)" \
                                                                          " VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s , %s , %s, %s) "
                print(self.Qdate_from.dateTime().toString('yyyy-MM-dd'))
                val = (self.LE_desc.text(),
                       self.valueData,
                       self.serialCount,
                       self.MultiUse,
                       self.MultiCount,
                       CL_userModule.user_name,
                       creationDate,
                       self.Qdate_from.dateTime().toString('yyyy-MM-dd'),
                       str(self.Qtime_from.dateTime().toString('hh:mm')),
                       self.Qdate_to.dateTime().toString('yyyy-MM-dd'),
                       str(self.Qtime_to.dateTime().toString('hh:mm')),
                       '0')
                mycursor.execute(sql, val)
                indx = self.LE_desc.text()
                mycursor.execute("SELECT * FROM COUPON Where COP_DESC = '" + indx + "'")
                c = mycursor.fetchone()
                id = c[0]
                for i in range(int(self.serialCount)):
                    value = randint(0, 1000000000000)
                    sql_select_Query = "select * from COUPON_SERIAL where COPS_BARCODE = %s "
                    x = ("HCOP"+bin(value),)
                    mycursor.execute(sql_select_Query, x)
                    record = mycursor.fetchone()
                    if mycursor.rowcount > 0:
                        value=value+1
                    sql2 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    val2 = (id, "HCOP"+bin(value), CL_userModule.user_name,self.serialType ,creationDate, 0,
                            '1')
                    print(sql2, val2)
                    mycursor.execute(sql2, val2)
                for j in range(len(self.Qcombo_company.currentData())):
                    for i in range(len(self.Qcombo_branch.currentData())):
                        sql3 = "INSERT INTO COUPON_BRANCH (COMPANY_ID,BRANCH_NO,COUPON_ID,STATUS) VALUES (%s,%s,%s,%s)"
                        val3 = (
                            self.Qcombo_company.currentData()[j], self.Qcombo_branch.currentData()[i],
                            id,
                            '1')
                        mycursor.execute(sql3, val3)
                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                db1.connectionCommit(self.conn)
                mycursor.close()
                QtWidgets.QMessageBox.warning(self, "Done", "رقم الكوبون هو " + str(id))
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




