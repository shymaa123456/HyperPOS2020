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
            self.LE_custNo.textChanged.connect(self.FN_GET_CUST)
            today_date = str(datetime.today().strftime('%Y-%m-%d'))
            today_date = today_date.split("-")
            d = QDate(int(today_date[0]), int(today_date[1]), int(today_date[2]))
            self.expire_date.setMinimumDate(d)
        except Exception as err:
            print(err)
    def FN_GET_CUST (self):
        conn = db1.connect()
        mycursor = conn.cursor()
        no = self.LE_custNo.text().strip()

        self.LE_custName.setText('')

        sql = "SELECT POSC_NAME FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(no) + "'"

        mycursor.execute(sql)
        myresult = mycursor.fetchone()

        if mycursor.rowcount >0:
            self.LE_custName.setText(myresult[0])
        mycursor.close()
    def FN_VALIDATE_CUST(self,id ):

            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()

            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
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
                else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "العميل غير موجود ")
        except Exception as err:
            print(err)
            # insert in  to db
    def FN_LOAD_MODIFY(self):
        print("here")
    def FN_MODIFY_CUSTGP(self):
        self.conn1 = db1.connect()
        if len(self.Qtable_custGP.selectedIndexes()) >0 :
            rowNo = self.Qtable_custGP.selectedItems()[0].row()
            id = self.LB_custGpId.text().strip()
            desc_old = self.Qtable_custGP.item(rowNo, 1).text()
            desc = self.LE_desc.text().strip()
            custGroup = self.CMB_custGroup.currentText()
            if custGroup == 'Active':
                status = 1
            else:
                status = 0
            #
            error = 0
            if self.desc == '':
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")

            else:
                if desc != desc_old:
                    if self.FN_CHECK_DUP_NAME(desc,id) != False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                        error=1

                if error!=1:
                    mycursor = self.conn1.cursor()
                    changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "update  Hyper1_Retail.CUSTOMER_GROUP  set CG_Status= %s ,CG_DESC = %s ,CG_CHANGED_ON=%s , 	CG_CHANGED_BY =%s  where CG_GROUP_ID = %s"
                    val = (status,desc, changeDate,CL_userModule.user_name,id)
                    mycursor.execute(sql, val)
                    #mycursor.close()
                    #
                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                    db1.connectionCommit(self.conn1)
                    self.FN_GET_CUSTGPS()
                    self.FN_CLEAR_FEILDS ()
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

    def FN_CLEAR_FEILDS (self):
        self.LB_custGpId.clear()
        self.LE_desc.clear()
        self.CMB_custGroup.setCurrentText('Active')
        self.LB_status.setText('1')
