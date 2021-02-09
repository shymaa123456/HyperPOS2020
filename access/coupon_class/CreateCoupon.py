import sys
from pathlib import Path
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from access.coupon_class.PathData import CL_PathData
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
    def __init__(self):
        super(CL_CreateCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()


    def FN_LOADUI(self):
        filename = self.dirname + '/createCoupon.ui'
        loadUi(filename, self)

        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(20, 15, 271, 25)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(20, 55, 271, 25)
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

    def FN_endableMultiUser(self):
        if self.checkBox_Multi.isChecked():
            self.LE_desc_5.setEnabled(True)
            self.LE_desc_4.setEnabled(False)
        else:
            self.LE_desc_5.setEnabled(False)
            self.LE_desc_4.setEnabled(True)

    def FN_EnableDiscVal(self):
        self.valueType="COP_DISCOUNT_VAL"
        self.LE_desc_2.setEnabled(True)
        self.LE_desc_3.setEnabled(False)


    def FN_EnablePercentage(self):
        self.valueType="COP_DISCOUNT_PERCENT"
        self.LE_desc_3.setEnabled(True)
        self.LE_desc_2.setEnabled(False)


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

    def FN_GET_Branch(self):
        # Todo: method for fills the Branch combobox
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_branch.addItem(row, val)
        mycursor.close()

    def FN_Create(self):

        try:
            mycursor = self.conn.cursor()
            if len(self.Qcombo_company.currentData())==0 or len(self.Qcombo_branch.currentData())==0 or len(self.LE_desc.text())==0 or len(self.LE_desc_3.text()) == 0 and len(self.LE_desc_2.text()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                if self.checkBox_Multi.isChecked():
                        self.serialCount = "1"
                        self.MultiCount = self.LE_desc_5.text()
                        self.MultiUse = "1"
                else:
                        self.serialCount = self.LE_desc_4.text()
                        self.MultiCount = "0"
                        self.MultiUse = "0"
            creationDate = str(datetime.today().strftime('%d-%m-%Y'))
            if self.radioButton_Percentage.isChecked():
                if len(self.LE_desc_3.text()) == 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
                else:
                    self.valueData = self.LE_desc_3.text()
            elif self.radioButton_Value.isChecked():
                if len(self.LE_desc_2.text()) == 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
                else:
                    self.valueData = self.LE_desc_2.text()
            self.conn = db1.connect()
            indx = self.LE_desc.text()

            # sql_select_Query = "select * from Hyperpos_users where name = '" + username +"' and password = '"+ password+"'"
            sql_select_Query = "select * from COUPON where COP_DESC = %s "

            x = (indx,)
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()

            if mycursor.rowcount > 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")

            else:
                id = 0
                sql = "INSERT INTO COUPON (COP_DESC, " + self.valueType + ", COP_SERIAL_COUNT,COP_MULTI_USE, COP_MULTI_USE_COUNT, COP_CREATED_BY, COP_CREAED_ON, COP_VALID_FROM, COP_VALID_TO, COP_STATUS)" \
                                                                          " VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s , %s) "
                print(self.Qdate_from.dateTime().toString('dd-MM-yyyy'))
                val = (self.LE_desc.text(), self.valueData, self.serialCount, self.MultiUse,
                       self.MultiCount, CL_userModule.user_name, creationDate,
                       self.Qdate_from.dateTime().toString('dd-MM-yyyy'),
                       self.Qdate_to.dateTime().toString('dd-MM-yyyy'),
                       '0')
                mycursor.execute(sql, val)
                db1.connectionCommit(self.conn)
                mycursor.close()

                self.conn = db1.connect()
                mycursor = self.conn.cursor()

                indx = self.LE_desc.text()
                mycursor.execute("SELECT * FROM COUPON Where COP_DESC = '" + indx + "'")
                c = mycursor.fetchone()
                id = c[0]

                for i in range(int(self.serialCount)):
                    value = randint(0, 1000000000000)

                    sql_select_Query = "select * from COUPON_SERIAL where COPS_BARCODE = %s "

                    x = (bin(value),)
                    mycursor = self.conn.cursor()
                    mycursor.execute(sql_select_Query, x)
                    record = mycursor.fetchone()

                    if mycursor.rowcount > 0:
                        value=value+1
                    sql2 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s)"
                    val2 = (id, bin(value), CL_userModule.user_name, creationDate, 0,
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

                db1.connectionCommit(self.conn)
                mycursor.close()
                QtWidgets.QMessageBox.warning(self, "Done", "رقم الكوبون هو " + str(id))


        except:
            print(sys.exc_info())


