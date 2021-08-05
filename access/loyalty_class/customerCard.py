from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp, QDate

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from access.utils.util import *
from datetime import datetime
#from cryptography.fernet import Fernet


class CL_customerCard(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(CL_customerCard, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    ###

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createCustomerCard.ui'
        loadUi(filename, self)

        try:
            self.CMB_status.addItem( "Active", '1')
            self.CMB_status.addItem("Inactive", '0')
            self.Qbtn_create.clicked.connect(self.FN_CREATE_CUSTCD)
            self.LE_custNo.textChanged.connect(self.FN_GET_CUST_NAME)
            today_date = str(datetime.today().strftime('%Y-%m-%d'))
            today_date = today_date.split("-")
            d = QDate(int(today_date[0]), int(today_date[1]), int(today_date[2]))
            self.expire_date.setMinimumDate(d)

            # Set Style
            # self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except Exception as err:
            print(err)

    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyCustomerCard.ui'
        loadUi(filename, self)

        try:

            self.CMB_status.addItem("Inactive", '0')
            self.Qbtn_modify.clicked.connect(self.FN_MODIFY_CUSTCD)
            self.LE_custNo.textChanged.connect(self.FN_GET_CARD_DETAILS)
            # today_date = str(datetime.today().strftime('%Y-%m-%d'))
            # today_date = today_date.split("-")
            # d = QDate(int(today_date[0]), int(today_date[1]), int(today_date[2]))
            # self.expire_date.setMinimumDate(d)

            # Set Style
            # self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except Exception as err:
            print(err)
    def FN_GET_CARD_DETAILS(self):
        self.FN_GET_CUST_NAME ()

        conn = db1.connect()
        mycursor = conn.cursor()
        no = self.LE_custNo.text().strip()
        sql = "SELECT `EXPIRY_DATE`,CARD_SERIAL FROM Hyper1_Retail.POS_CUSTOMER_CARD where POS_CUST_ID = '" + str(
                no) + "' and CARD_STATUS = '1'"
        mycursor.execute(sql)
        myresult = mycursor.fetchone()

        if mycursor.rowcount > 0:
            xto = myresult[0].split("-")

            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.expire_date.setDate(d)
            self.card_serial = myresult[1]
            #set the date
            print("found")
        else:
            print("no data")

    def FN_GET_CUST_NAME (self):
        conn = db1.connect()
        mycursor = conn.cursor()
        no = self.LE_custNo.text().strip()

        self.LE_custName.setText('')

        sql = "SELECT POSC_NAME FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(no) + "'"

        mycursor.execute(sql)
        myresult = mycursor.fetchone()

        if mycursor.rowcount >0:
            self.LE_custName.setText(myresult[0])
            print(myresult[0])
        mycursor.close()
        return  self.LE_custName.text()
    def FN_VALIDATE_CUST(self,id ):

            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()

            if mycursor11.rowcount > 0:
                sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER_CARD where POS_CUST_ID = '" + str(id) + "' and CARD_STATUS = '1'"
                mycursor11.execute(sql)
                myresult = mycursor11.fetchone()
                if mycursor11.rowcount > 0:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "العميل لديه كارت فعال ")
                    mycursor11.close()
                    return False
                else:
                    mycursor11.close()
                    return True
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "العميل غير موجود ")
                mycursor11.close()
                return False
    def FN_GET_MASKED_CARD_SERIAL(self,id):
        print("here")
        # key = Fernet.generate_key()
        # print(key)
        # id = 'b'+ id
        # cipher_suite = Fernet(key)
        # ciphered_text = cipher_suite.encrypt(b'id')
        # print(ciphered_text)
        # return ciphered_text
    def FN_CREATE_CUSTCD(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            no = self.LE_custNo.text().strip()
            name = self.LE_custName.text().strip()
            expire_date = self.expire_date.date().toString('yyyy-MM-dd')

            if name == '' or no =='' :
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاءادخال العميل")

            else:
                ret = self.FN_VALIDATE_CUST(no)
                if ret == True:
                        mask_serial = self.FN_GET_MASKED_CARD_SERIAL(no)
                        sql = "INSERT INTO `Hyper1_Retail`.`POS_CUSTOMER_CARD`(`CARD_SERIAL_BARCODE`,`POS_CUST_ID`,`EXPIRY_DATE`,`CARD_STATUS`) " \
                              "         VALUES ( %s, %s, %s,  %s)"

                        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                        val = (mask_serial, no, expire_date, self.CMB_status.currentData()
                               )
                        mycursor.execute(sql, val)
                        # mycursor.execute(sql)

                        mycursor.close()
                        QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                        db1.connectionCommit(self.conn)


        except Exception as err:
            print(err)
            # insert in  to db

    def FN_MODIFY_CUSTCD(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        no = self.LE_custNo.text().strip()
        name = self.LE_custName.text().strip()
        if len(name) >0:
            print(len (no))
            sql = "update `Hyper1_Retail`.`POS_CUSTOMER_CARD` set CARD_STATUS = '0'  where CARD_SERIAL = %s "
            val = (self.card_serial,)
            mycursor.execute(sql, val)
            mycursor.close()
            QtWidgets.QMessageBox.information(self, "تم", "تم  التعديل")
            db1.connectionCommit(self.conn)
        else:
            if len(no) > 0:
                QtWidgets.QMessageBox.warning(self, "خطأ", " رقم العميل غير موجود")
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال رقم العميل")

