import time
from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from mysql.connector import Error
import xlrd
from datetime import datetime
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from PyQt5.QtCore import *
from random import randint

class CL_redGift(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''

    def __init__(self):
        super(CL_redGift, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'

    from Validation.Validation import CL_validation
    def textchanged(self):
        try:
            print( "contents of text box: " )
            if self.Qline_replace.text().strip() !='' and self.Qline_points.text().strip() !='' :
                ret = CL_validation.FN_validation_int(self.Qline_replace.text().strip())
                if ret == True:
                    replacedPoints = int(self.Qline_replace.text().strip())

                    actualPoints = int(self.Qline_points.text().strip())
                    remainingPoints = actualPoints - replacedPoints
                    self.Qline_remainder.setText(str(remainingPoints))
                    self.FN_GET_POINTS_VALUE(replacedPoints)
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "replaced points is not integer ")
        except (Error, Warning) as e:
            print(e)

    def FN_GET_POINTS_VALUE(self,replacedPoints):
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT POINTS_QTY,POINTS_VALUE FROM Hyper1_Retail.LOYALITY_POINT where POINTS_VALID_FROM <= %s and POINTS_VALID_TO >= %s"
        currentDate =str(datetime.today().strftime('%Y-%m-%d'))
        x = (currentDate,currentDate,)
        mycursor.execute(sql_select_query,x)
        result = mycursor.fetchone()
        value = replacedPoints * int(result[1] )/int(result[0])
        print(result)
        self.Qline_point_value.setText(str(value))
    def FN_CLEAR_FEILDS (self):
        self.Qline_points.setText("")
        self.Qline_name.setText('')
        self.Qline_replace.setText("")
        self.Qline_remainder.setText("")
        self.Qline_point_value.setText("")
    def FN_LOAD_DISPlAY(self):
        try:
            filename = self.dirname + '/redeemGift.ui'
            loadUi(filename, self)
            conn = db1.connect()
            mycursor = conn.cursor()
            self.Qbtn_search.clicked.connect(self.FN_SEARCH_RED_VOUCH)
            #self.Qbtn_export.clicked.connect(self.FN_SAVE)
            #self.Qbtn_exit.clicked.connect(self.FN_exit)
            self.Qline_replace.textChanged.connect(self.textchanged)
            self.Qline_cust.textChanged.connect(self.FN_CLEAR_FEILDS)
            self.setFixedWidth(513)
            self.setFixedHeight(330)
            for row_number, row_data in enumerate(CL_userModule.myList):
                if row_data[1] == 'Redeem_Gift':
                    if row_data[4] == 'None':
                        print('hh')
                    else:
                        sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                        x = (row_data[4],)
                        mycursor.execute(sql_select_query, x)

                        result = mycursor.fetchone()
                        # print(result)
                        if result[0] == 'replace':
                            self.Qbtn_replace.setEnabled(True)
                            self.Qbtn_replace.clicked.connect(self.FN_REPLACE_VOUCHER)
        except (Error, Warning) as e:
                print(e)

    def FN_REPLACE_VOUCHER(self):
        replacedPoints = int(self.Qline_replace.text().strip())
        customer = self.Qline_cust.text().strip()
        if customer !='':
            if replacedPoints > 0 :
                ret = self.FN_VALIDATE()
                if ret == True:
                    self.FN_CREATE_VOUCHER()
                    self.FN_UPDATE_CUST_POINTS()
                    self.FN_CLEAR_FEILDS()
                    self.Qline_cust.setText("")

                else :
                    QtWidgets.QMessageBox.warning(self, "Error", "النقاط المستبدله يجب أن تكون أقل من أو تساوي نقاط العميل ")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "النقاط المستبدله يجب أن تكون أكثر من صفر")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "يجب إدخال رقم عميل")

    def FN_CREATE_VOUCHER(self):
        try:
            # insert voucher
            value = self.Qline_point_value.text().strip()
            customer = self.Qline_cust.text().strip()

            conn = db1.connect()
            mycursor = conn.cursor()
            creationDate = str(datetime.today().strftime('%d-%m-%Y'))
            # insert voucher
            value11 = randint(0, 1000000000000)
            voucherBarcode ="RVOU" + bin(value11)
            sql = "INSERT INTO Hyper1_Retail.VOUCHER (GV_DESC, GVT_ID, GV_BARCODE, GV_VALUE, GV_NET_VALUE, GV_CREATED_BY, GV_CREATED_ON, GV_VALID_FROM, GV_VALID_TO, POSC_CUST_ID, GV_PRINTRED,GV_STATUS) VALUES (%s, %s,%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s) "
            val = ('Redeem Points', '1', "RVOU" + bin(value11), value, value,
                   CL_userModule.user_name, creationDate,
                   creationDate, '31-12-9999', customer,
                   '0', '0')
            mycursor.execute(sql, val)
            db1.connectionCommit(conn)
            mycursor.execute( "select GV_ID from Hyper1_Retail.VOUCHER where GV_BARCODE ='"+voucherBarcode+"'")
            result= mycursor.fetchone()
            QtWidgets.QMessageBox.information(self, "Done", "Voucher is created with number "+str(result[0]))
            # update customer points
            actualPoints = self.Qline_points.text().strip()
            remainingPoints = self.Qline_remainder.text().strip()


        except Exception as err:
            print(err)

    def FN_UPDATE_CUST_POINTS(self):
        try:
            # insert voucher
            value = self.Qline_point_value.text().strip()
            customer = self.Qline_cust.text().strip()

            conn = db1.connect()
            mycursor = conn.cursor()
            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            actualPoints = self.Qline_points.text().strip()
            remainingPoints = self.Qline_remainder.text().strip()
            sql = "update Hyper1_Retail.POS_CUSTOMER_POINT set POSC_POINTS_BEFORE =%s ,POSC_POINTS_AFTER=%s , POINTS_CHANGED_ON =%s , TRANS_SIGN = '0' where POSC_CUSTOMER_ID = %s"
            val = (actualPoints, remainingPoints, creationDate, customer)
            mycursor.execute(sql, val)
            db1.connectionCommit(conn)
            # QtWidgets.QMessageBox.warning(self, "Done", "Voucher is created")
            print("customer points are updated")
        except Exception as err:
            print(err)

    def FN_VALIDATE(self):
        replacedPoints = int(self.Qline_replace.text().strip())
        actualPoints = int(self.Qline_points.text().strip())
        if replacedPoints > actualPoints:
            return False
        else:
            return True
    def FN_CHECK_CUSTOMER(self,id):
        try:
            conn = db1.connect()
            mycursor = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False
        except (Error, Warning) as e:
            print(e)
    def FN_SEARCH_RED_VOUCH(self):
       try:
           print('in search')

           customer = self.Qline_cust.text().strip()
           if customer != '':
               ret= self.FN_CHECK_CUSTOMER(customer)
               if ret == True :
                   ##get customer points
                   conn = db1.connect()
                   mycursor = conn.cursor()
                   sql = "SELECT cp.POSC_POINTS_AFTER , c.POSC_NAME  FROM Hyper1_Retail.POS_CUSTOMER_POINT  cp " \
                         " inner join Hyper1_Retail.POS_CUSTOMER  c " \
                         " on cp.POSC_CUSTOMER_ID = c.POSC_CUST_ID " \
                         " where c.POSC_CUST_ID = '" + str(customer) + "'"
                   mycursor.execute(sql)
                   myresult = mycursor.fetchone()
                   self.Qline_points.setText(myresult[0])
                   self.Qline_name.setText(myresult[1])
               else:
                   QtWidgets.QMessageBox.warning(self, "Error", "Customer no is invalid")
           else:
               QtWidgets.QMessageBox.warning(self, "Error", "Please enter customer no")
       except Exception as err:
            print(err)

    def FN_exit(self):
        QApplication.quit()