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


class CL_redVouch(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''

    def __init__(self):
        super(CL_redVouch, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'

    def textchanged(self):
        try:
            print( "contents of text box: " )
            replacedPoints = int(self.Qline_replace.text().strip())
            actualPoints = int(self.Qline_points.text().strip())
            remainingPoints = actualPoints - replacedPoints
            self.Qline_remainder.setText(str(remainingPoints))
            self.FN_GET_POINTS_VALUE(replacedPoints)
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

    def FN_LOAD_DISPlAY(self):
        try:
            filename = self.dirname + '/redeemVoucher.ui'
            loadUi(filename, self)
            conn = db1.connect()
            mycursor = conn.cursor()
            self.Qbtn_search.clicked.connect(self.FN_SEARCH_RED_VOUCH)
            #self.Qbtn_export.clicked.connect(self.FN_SAVE)
            #self.Qbtn_exit.clicked.connect(self.FN_exit)
            self.Qline_replace.textChanged.connect(self.textchanged)
            for row_number, row_data in enumerate(CL_userModule.myList):
                if row_data[1] == 'Redeem_Voucher':
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
        try:
            print('in replace')
        except Exception as err:
            print(err)
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