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


class CL_PromVoucher(QtWidgets.QDialog):


    def __init__(self):
        super(CL_PromVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()


    def FN_LOAD_CREATE(self):
        try:
            filename = self.dirname + '/createPromVoucher.ui'
            loadUi(filename, self)
            datefrom = str(datetime.today().strftime('%Y-%m-%d'))
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setMinimumDate(d)
            self.Qdate_to.setMinimumDate(d)

            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_createVoucher.clicked.connect(self.FN_CREATE_VOUCHER)
        except:
            print(sys.exc_info())
    def FN_LOAD_MODIFY(self):
        try:
            filename = self.dirname + '/modifyPromVoucher.ui'
            loadUi(filename, self)
            datefrom = str(datetime.today().strftime('%Y-%m-%d'))
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setMinimumDate(d)
            self.Qdate_to.setMinimumDate(d)

            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_modifyVoucher.clicked.connect(self.FN_MODIFY_VOUCHER)
        except:
            print(sys.exc_info())


    def FN_CREATE_VOUCHER(self):
        try:

            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
            if len( self.LE_desc.text().strip()) == 0  or len(self.LE_value.text().strip())== 0 or len(self.LE_maxCount.text().strip() )== 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:

                if self.Qdate_to.dateTime() < self.Qdate_from.dateTime():
                        QtWidgets.QMessageBox.warning(self, "Done",
                                                      "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")

                else:

                    sql = "INSERT INTO VOUCHER (''PROMV_VOUCHER_DESC','PROMV_VOUCHER_VAL','PROMV_MAX_COUNT','PROMV_CREATED_BY','PROMV_CREATED_ON', 'PROMV_VALID_FROM','PROMV_VALID_TO','PROMV_STATUS) VALUES (%s, %s,%s, %s, %s, %s, %s) "
                    val = (self.LE_desc.text().strip(),self.LE_value.text().strip(),self.LE_maxCount.text().strip(),CL_userModule.user_name,creationDate,self.Qdate_from.dateTime().toString('dd-MM-yyyy'),self.Qdate_to.dateTime().toString('dd-MM-yyyy'),'0','0')

                    mycursor.execute(sql, val)

                    db1.connectionCommit(self.conn)
                    QtWidgets.QMessageBox.warning(self, "Done", "رقم قسيمه الشراء هو " + str(id))
                    #self.label_num.setText(str(id))
                    mycursor.close()
        except:
            print(sys.exc_info())



    def FN_LOAD_CHANGE_ACTIVE(self):
        try:
            filename = self.dirname + '/stopPromVoucher.ui'
            loadUi(filename, self)

            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_changeStatus.clicked.connect(self.FN_CHANGE_STATUS)
        except Exception as err:
            print(err)

    def FN_LOAD_CHANGE_STATUS(self,ss):
        try:

            filename = self.dirname + '/stopPromVoucher.ui'
            loadUi(filename, self)

            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_changeStatus.clicked.connect(self.FN_CHANGE_STATUS)
        except Exception as err:
            print(err)
    def FN_MODIFY_VOUCHER(self):
        print("hhh")

    def FN_CHANGE_STATUS(self):
        print("hhh")