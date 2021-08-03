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

            if self.Qline_replace.text().strip() !='' and self.Qline_points.text().strip() !='' :
                ret = CL_validation.FN_validation_int(self.Qline_replace.text().strip())
                if ret == True:
                    replacedPoints = float(self.Qline_replace.text().strip())

                    actualPoints = float(self.Qline_points.text().strip())
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
        return result
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

            self.Qline_replace.textChanged.connect(self.textchanged)
            self.Qline_cust.textChanged.connect(self.FN_CLEAR_FEILDS)
            # self.setFixedWidth(513)
            # self.setFixedHeight(330)

            # Set Style
            # self.voucher_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
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
                    #self.FN_CREATE_VOUCHER()
                    self.FN_UPDATE_CUST_POINTS()
                    self.FN_CLEAR_FEILDS()
                    self.Qline_cust.setText("")

                else :
                    QtWidgets.QMessageBox.warning(self, "خطأ", "النقاط المستبدله يجب أن تكون أقل من أو تساوي نقاط العميل ")
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "النقاط المستبدله يجب أن تكون أكثر من صفر")
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يجب إدخال رقم عميل")


    def FN_UPDATE_CUST_POINTS(self):
        try:
            # insert voucher
            value = self.Qline_point_value.text().strip()
            customer = self.Qline_cust.text().strip()
            replacedPoints = float(self.Qline_replace.text().strip())
            conn = db1.connect()
            mycursor = conn.cursor()
            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            actualPoints = float(self.Qline_points.text().strip())
            remainingPoints = float(self.Qline_remainder.text().strip())
            pts = remainingPoints - actualPoints

            sql0 = "  LOCK  TABLES    Hyper1_Retail.POS_CUSTOMER_POINT   WRITE , " \
                   "    Hyper1_Retail.LOYALITY_POINTS_TRANSACTION_LOG   WRITE  "


            mycursor.execute(sql0)
            # get point value
            result = self.FN_GET_POINTS_VALUE(replacedPoints)
            sql = "INSERT INTO `Hyper1_Retail`.`LOYALITY_POINTS_TRANSACTION_LOG` " \
                  "(`POSC_CUST_ID`,`REDEEM_TYPE_ID`,`COMPANY_ID`,`BRANCH_NO`,`TRANS_CREATED_BY`," \
                  "`TRANS_CREATED_ON`,`POSC_POINTS_BEFORE`,`VALUE_OF_POINTS`,`TRANS_POINTS_QTY`,`TRANS_POINTS_VALUE`,`TRANS_REASON`,`POSC_POINTS_AFTER`,`TRANS_STATUS` ,REFERENCE_TRANS)" \
                  "                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            val = (
                customer,4, '1', 'H010', CL_userModule.user_name, creationDate, actualPoints, result[1], pts,
                float(result[1]) * pts, 'Gift redeem', remainingPoints,
                '2',self.CMB_redeemItem.currentData())
            mycursor.execute(sql, val)

            mycursor.execute(
                "SELECT max(cast(`MEMBERSHIP_POINTS_TRANS`  AS UNSIGNED)) FROM LOYALITY_POINTS_TRANSACTION_LOG")
            myresult = mycursor.fetchone()
            MEMBERSHIP_POINTS_TRANS = myresult[0]

            sql = "update Hyper1_Retail.POS_CUSTOMER_POINT set MEMBERSHIP_POINTS_TRANS=%s , POSC_POINTS_BEFORE =%s ,TRANS_POINTS = %s ,POSC_POINTS_AFTER=%s, POINTS_CHANGED_ON =%s , TRANS_SIGN = '0' where POSC_CUSTOMER_ID = %s"
            val = (MEMBERSHIP_POINTS_TRANS, actualPoints, pts, remainingPoints, creationDate, customer)
            mycursor.execute(sql, val)

            # QtWidgets.QMessageBox.warning(self, "Done", "Voucher is created")
            sql00 = "  UNLOCK   tables    "
            mycursor.execute(sql00)
            db1.connectionCommit(conn)
            print("customer points are updated")
        except Exception as err:
            print(err)
    def FN_VALIDATE(self):
        replacedPoints = float(self.Qline_replace.text().strip())
        actualPoints = float(self.Qline_points.text().strip())
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
    def FN_LOAD_REDEEM_ITEMS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_redeemItem.clear()
        branch = []
        for id,name in CL_userModule.branch:
            branch.append(id)
        branch_list_tuple = tuple(branch)
        sql = "select POS_GTIN_DESC_A ,REDEEM_ITEM.POS_GTIN from Hyper1_Retail.REDEEM_ITEM Inner join " \
              "POS_ITEM on REDEEM_ITEM.POS_GTIN= POS_ITEM.POS_GTIN  where" \
              " REDEEM_VALID_FROM <= %s and REDEEM_VALID_TO >= %s and REDEEM_STATUS = '1' and BRANCH_NO in {}".format(branch_list_tuple)
        print(sql)
        currentDate = str(datetime.today().strftime('%Y-%m-%d'))
        x = (currentDate, currentDate)
        mycursor.execute(sql, x)
        myresult = mycursor.fetchall()
        myresult = list(dict.fromkeys(myresult))
        for row, val in myresult:
            self.CMB_redeemItem.addItem(row, val)
        mycursor.close()
        #return myresult
    def FN_SEARCH_RED_VOUCH(self):
       try:
           print('in search')

           customer = self.Qline_cust.text().strip()
           if customer != '':
               ret= self.FN_CHECK_CUSTOMER(customer)
               if ret == True :
                   self.FN_LOAD_REDEEM_ITEMS()
                   print(self.CMB_redeemItem.currentData())
                   ##get customer points
                   conn = db1.connect()
                   mycursor = conn.cursor()
                   sql = "SELECT cp.POSC_POINTS_AFTER , c.POSC_NAME  FROM Hyper1_Retail.POS_CUSTOMER_POINT  cp " \
                         " inner join Hyper1_Retail.POS_CUSTOMER  c " \
                         " on cp.POSC_CUSTOMER_ID = c.POSC_CUST_ID " \
                         " where c.POSC_CUST_ID = '" + str(customer) + "'"
                   mycursor.execute(sql)
                   myresult = mycursor.fetchone()
                   self.Qline_points.setText(str(myresult[0]))
                   self.Qline_name.setText(str(myresult[1]))
               else:
                   QtWidgets.QMessageBox.warning(self, "خطأ", "رقم العميل غير صحيح")
           else:
               QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال رقم العميل")
       except Exception as err:
            print(err)

    def FN_exit(self):
        QApplication.quit()