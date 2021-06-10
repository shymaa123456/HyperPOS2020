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
            if len( self.LE_desc.text().strip()) == 0  or len(
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
                    value = randint(0, 1000000000000)
                    sql = "INSERT INTO VOUCHER (GV_DESC, GVT_ID, GV_BARCODE, GV_VALUE, GV_NET_VALUE, GV_CREATED_BY, GV_CREATED_ON, GV_VALID_FROM, GV_VALID_TO, GV_REFUNDABLE, GV_RECHARGABLE,GV_MULTIUSE, POSC_CUST_ID, GV_PRINTRED,GV_STATUS) VALUES (%s, %s,%s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s) "
                    val = (self.LE_desc.text().strip(),self.VGType,"HVOU"+bin(value),self.LE_desc_2.text().strip(),self.LE_desc_2.text().strip(),CL_userModule.user_name,creationDate,self.Qdate_from.dateTime().toString('dd-MM-yyyy'),self.Qdate_to.dateTime().toString('dd-MM-yyyy'),self.GV_REFUNDABLE,self.GV_RECHARGABLE,self.GV_REFUNDABLE,self.LE_desc_5.text().strip(),'0','0')

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



    def FN_LOAD_CHANGE_STATUS(self,status):
        try:
            filename = self.dirname + '/stopPromVoucher.ui'
            loadUi(filename, self)
            print(status)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_changeStatus.clicked.connect(self.FN_CHANGE_STATUS)
        except Exception as err:
            print(err)

    def FN_MODIFY_VOUCHER(self):
        print("hhh")

    def FN_CHANGE_STATUS(self):
        print("hhh")