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


class CL_EditVoucher(QtWidgets.QDialog):
    valueType=""
    valueData=""
    serialCount = ""
    MultiCount = ""
    MultiUse = ""
    movement=0
    serial_num=0
    usage=0
    branch_list = []
    new_branch_list = []
    multiusage=0
    serial_type=0

    def __init__(self):
        super(CL_EditVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()

    def FN_LOADUI(self):
        filename = self.dirname + '/editVoucher.ui'
        loadUi(filename, self)
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(10, 100, 271, 25)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(10, 140, 271, 25)
        self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.CMB_CouponStatus.addItems(["Inactive","Active"])
        self.FN_getData()
        self.CMB_CouponDes.activated[str].connect(self.FN_getDatabyID)
        self.FN_getDatabyID()
        self.radioButton_Value.clicked.connect(self.FN_EnableDiscVal)
        self.radioButton_Percentage.clicked.connect(self.FN_EnablePercentage)
        self.checkBox_Multi.toggled.connect(self.FN_endableMultiUser)
        self.BTN_editCoupon.clicked.connect(self.FN_editAction)
        # datefrom = str(datetime.today().strftime('%Y-%m-%d'))
        # xfrom = datefrom.split("-")
        # d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        # self.Qdate_from.setMinimumDate(d)
        # self.Qdate_to.setMinimumDate(d)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)


    def FN_GET_Company(self):
        #Todo: method for fills the company combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    def FN_GET_Branch(self):
        # Todo: method for fills the Branch combobox
        i = 0
        try:
            # Todo: method for fills the Branch combobox
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH")
            records = mycursor.fetchall()
            for row, val in records:

                if val in self.FN_AuthBranchUser()[i]:
                    self.Qcombo_branch.addItem(row, val)
                i += 1
            mycursor.close()
        except:
            print(sys.exc_info())




    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_DESC,COP_ID FROM COUPON")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()


    def FN_getDatabyID(self):
         try:
            self.branch_list = []
            self.new_branch_list = []
            self.FN_Clear()
            indx = self.CMB_CouponDes.currentData()
            self.labe_id.setText(str(indx))
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            sql_select_Query = "SELECT * FROM COUPON where COP_ID = %s"
            x = (indx,)
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            self.LE_desc_1.setText(record[1])
            if (record[2]!=None and len(record[2]) > 0):
                self.radioButton_Value.setChecked(True)
                self.LE_desc_2.setValue(float(record[2]))
                self.LE_desc_2.setEnabled(True)
                self.LE_desc_3.setEnabled(False)
                self.LE_desc_3.clear()
                self.valueType = "COP_DISCOUNT_VAL"
                self.valueData = self.LE_desc_2.text()
            else:
                self.radioButton_Percentage.setChecked(True)
                self.LE_desc_3.setValue(float(record[3]))
                self.LE_desc_3.setEnabled(True)
                self.LE_desc_2.setEnabled(False)
                self.LE_desc_2.clear()
                self.valueType = "COP_DISCOUNT_PERCENT"
                self.valueData = self.LE_desc_3.text()
            dateto = record[12]
            xto = dateto.split("-")
            d = QDate(int(xto[2]), int(xto[1]), int(xto[0]))
            self.Qdate_to.setDate(d)

            datefrom = record[11]
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[2]), int(xfrom[1]), int(xfrom[0]))
            self.Qdate_from.setDate(d)



            self.LE_desc_4.setValue(float(record[4]))
            self.serial_num=int(record[4])

            self.multiusage=int(record[5])
            if (int(record[5]) == 1):
                self.checkBox_Multi.setChecked(True)
                self.LE_desc_5.setValue(float(record[6]))
                self.LE_desc_4.setEnabled(False)
                self.LE_desc_5.setEnabled(True)
            else:
                self.checkBox_Multi.setChecked(False)
                self.LE_desc_5.setEnabled(False)
                self.LE_desc_4.setEnabled(True)

            self.CMB_CouponStatus.setCurrentIndex(int(record[13]))
            self.FN_check_company(indx)
            self.FN_check_branch(indx)

            sql_select_Query = " select * FROM COUPON_SERIAL_PRINT_LOG  where COUPON_SERIAL_ID IN(SELECT COPS_SERIAL_ID FROM COUPON_SERIAL , COUPON WHERE COUPON_ID = COP_ID AND COP_ID =  %s) "
            x = (indx,)
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query, x)
            record1 = mycursor.fetchall()
            if mycursor.rowcount>0:
                self.movement=1

            sql_select_Query = " select * FROM COUPON_USAGE where COPS_SERIAL_ID IN(SELECT COPS_SERIAL_ID FROM COUPON_SERIAL , COUPON WHERE COUPON_ID = COP_ID AND COP_ID =  %s) "
            x = (indx,)
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query, x)
            record2 = mycursor.fetchall()
            if mycursor.rowcount > 0:
                self.usage = 1
            mycursor.close()
            if self.usage==1:
                self.LE_desc_1.setEnabled(False)
                self.LE_desc_2.setEnabled(False)
                self.LE_desc_3.setEnabled(False)
                self.LE_desc_4.setEnabled(False)
                self.LE_desc_5.setEnabled(False)
                self.Qcombo_company.setEnabled(False)
                self.Qcombo_branch.setEnabled(False)
                self.Qdate_to.setEnabled(False)
                self.Qdate_from.setEnabled(False)
                self.usage = 0
            else:
                self.LE_desc_1.setEnabled(True)
                self.LE_desc_2.setEnabled(True)
                self.LE_desc_3.setEnabled(True)
                self.LE_desc_4.setEnabled(True)
                self.LE_desc_5.setEnabled(True)
                self.Qcombo_company.setEnabled(True)
                self.Qcombo_branch.setEnabled(True)
                self.Qdate_to.setEnabled(True)
                self.Qdate_from.setEnabled(True)
                if (record[2] != None and len(record[2]) > 0):
                    self.LE_desc_3.setEnabled(False)
                else:
                    self.LE_desc_2.setEnabled(False)
                if (int(record[5]) == 1):
                    self.LE_desc_4.setEnabled(False)
                else:
                    self.checkBox_Multi.setChecked(False)
                    self.LE_desc_5.setEnabled(False)

            self.branch_list.clear()
            if len(self.Qcombo_branch.currentData()) > 0:
                for i in self.Qcombo_branch.currentData():
                    self.branch_list.append(i)

         except:
             print(sys.exc_info())

    def FN_endableMultiUser(self):
        if self.checkBox_Multi.isChecked():
            self.LE_desc_5.setEnabled(True)
            self.LE_desc_4.setEnabled(False)
        else:
            self.LE_desc_5.setEnabled(False)
            self.LE_desc_4.setEnabled(True)

    def FN_editAction(self):
        try:
            if len(self.Qcombo_company.currentData()) == 0 or len(self.Qcombo_branch.currentData()) == 0 or len(
                    self.LE_desc_1.text()) == 0 or len(self.LE_desc_3.text()) == 0 and len(self.LE_desc_2.text()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                if self.Qdate_to.dateTime()<self.Qdate_from.dateTime():
                    QtWidgets.QMessageBox.warning(self, "Done", "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")

                else:
                    mycursor = self.conn.cursor()
                    creationDate = str(datetime.today().strftime('%d-%m-%Y'))
                    if self.checkBox_Multi.isChecked():
                        self.serialCount = "1"
                        self.MultiCount = self.LE_desc_5.text()
                        self.MultiUse = "1"
                        self.serial_type=1
                        print("multi use="+str(self.multiusage))
                        if self.multiusage==0:
                            sql2 = "update COUPON_SERIAL set COPS_STATUS='0' where COUPON_ID='" + str(
                                self.CMB_CouponDes.currentData()) + "'"
                            mycursor.execute(sql2)
                            value = randint(0, 1000000000000)
                            creationDate = str(datetime.today().strftime('%d-%m-%Y'))
                            mycursor = self.conn.cursor()
                            sql7 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val7 = (
                                str(self.CMB_CouponDes.currentData()), bin(value), CL_userModule.user_name,self.serial_type,
                                creationDate, 0,
                                '1')
                            mycursor.execute(sql7, val7)
                            self.multiusage=1




                    else:
                        self.serialCount = self.LE_desc_4.text()
                        self.MultiCount = "0"
                        self.MultiUse = "0"
                        self.serial_type=0
                    print(self.serial_num)
                    print(int(self.LE_desc_4.text()))
                    if int(self.LE_desc_4.text()) < self.serial_num and self.movement == 1:
                        QtWidgets.QMessageBox.warning(self, "Error", "برجاء ادخل عدد اكبر من السابق")
                    else:
                        sql = "update COUPON set COP_DESC='" + self.LE_desc_1.text() + "'," + self.valueType + "=" + self.valueData + ",COP_SERIAL_COUNT=" + self.serialCount + ",COP_MULTI_USE=" + self.MultiUse + ",COP_MULTI_USE_COUNT=" + self.MultiCount + ",COP_CHANGED_BY='" + CL_userModule.user_name + "',COP_CHANGED_ON='" + creationDate + "',COP_VALID_FROM='" + self.Qdate_from.dateTime().toString(
                            'dd-MM-yyyy') + "',COP_VALID_TO='" + self.Qdate_to.dateTime().toString(
                            'dd-MM-yyyy') + "',COP_STATUS='" + str(
                            self.CMB_CouponStatus.currentIndex()) + "' where COP_ID='" + str(
                            self.CMB_CouponDes.currentData()) + "'"
                        mycursor.execute(sql)
                        # sql2 = "update COUPON_SERIAL set COPS_STATUS='" + str(
                        #     self.CMB_CouponStatus.currentIndex()) + "' where COUPON_ID='" + str(
                        #     self.CMB_CouponDes.currentData()) + "'"
                        # mycursor.execute(sql2)
                        # sql3 = "update COUPON_BRANCH set STATUS='" + str(
                        #     self.CMB_CouponStatus.currentIndex()) + "' where COUPON_ID='" + str(
                        #     self.CMB_CouponDes.currentData()) + "'"
                        # mycursor.execute(sql3)
                        
                        if len(self.Qcombo_branch.currentData()) > 0:
                            for i in self.Qcombo_branch.currentData():
                                self.new_branch_list.append(i)

                        if len(self.branch_list) > len(self.new_branch_list):
                            for row in self.branch_list:
                                print(row)
                                if row in self.new_branch_list:
                                    print("found")
                                else:
                                    print("not found")
                                    mycursor = self.conn.cursor()
                                    sql5 = "update COUPON_BRANCH set STATUS= 0 where COUPON_ID='" + str(
                                        self.CMB_CouponDes.currentData()) + "' and BRANCH_NO = '" + row + "'"
                                    mycursor.execute(sql5)
                                    print(sql5)
                        else:
                            for row in self.new_branch_list:
                                print(row)
                                if row in self.branch_list:
                                    print("found")
                                else:

                                    mycursor = self.conn.cursor()
                                    mycursor.execute(
                                        "SELECT * FROM COUPON_BRANCH where BRANCH_NO='" + row + "' and COUPON_ID='" + str(
                                            self.CMB_CouponDes.currentData()) + "'")
                                    record = mycursor.fetchall()
                                    if mycursor.rowcount > 0:
                                        mycursor = self.conn.cursor()
                                        sql8 = "update COUPON_BRANCH set STATUS= 1 where COUPON_ID='" + str(
                                            self.CMB_CouponDes.currentData()) + "' and BRANCH_NO = '" + row + "'"
                                        mycursor.execute(sql8)
                                        print(sql8)
                                    else:
                                        mycursor = self.conn.cursor()
                                        sql6 = "INSERT INTO COUPON_BRANCH (COMPANY_ID,BRANCH_NO,COUPON_ID,STATUS) VALUES (%s,%s,%s,%s)"
                                        val6 = (
                                            str(self.Qcombo_company.currentData()[0]), row,
                                            str(self.CMB_CouponDes.currentData()),
                                            '1')
                                        mycursor.execute(sql6, val6)

                        if int(self.LE_desc_4.text()) < self.serial_num:
                            indx = self.CMB_CouponDes.currentData()
                            sql_select_Query = "SELECT COPS_SERIAL_ID FROM COUPON_SERIAL where COUPON_ID = %s and COPS_STATUS = 1 and COPS_SERIAL_type = 0"
                            x = (indx,)
                            mycursor = self.conn.cursor()
                            mycursor.execute(sql_select_Query, x)
                            record = mycursor.fetchall()
                            num = 0
                            for row in range(self.serial_num - int(self.LE_desc_4.text())):
                                mycursor = self.conn.cursor()
                                sql9 = "update COUPON_SERIAL set COPS_STATUS= 0 where COUPON_ID='" + str(
                                    self.CMB_CouponDes.currentData()) + "' and COPS_SERIAL_ID = '" + str(
                                    record[num][0]) + "'"
                                mycursor.execute(sql9)
                                print(sql9)
                                num += 1
                            self.serial_num=int(self.LE_desc_4.text())
                        else:
                            for row in range(self.serial_num):
                                mycursor = self.conn.cursor()
                                sql9 = "update COUPON_SERIAL set COPS_STATUS= 0 where COUPON_ID='" + str(
                                    self.CMB_CouponDes.currentData()) + "'"
                                mycursor.execute(sql9)
                            for row in range(int(self.LE_desc_4.text())):
                                value = randint(0, 1000000000000)
                                creationDate = str(datetime.today().strftime('%d-%m-%Y'))
                                mycursor = self.conn.cursor()
                                sql7 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                val7 = (
                                    str(self.CMB_CouponDes.currentData()), bin(value), CL_userModule.user_name,
                                    self.serial_type,
                                    creationDate, 0,
                                    '1')
                                mycursor.execute(sql7, val7)



                            self.serial_num = int(self.LE_desc_4.text())

                        db1.connectionCommit(self.conn)
                        mycursor.close()

                        QtWidgets.QMessageBox.warning(self, "Done", "Done")
                        for i in self.FN_GetMathchBranch():
                            self.branch_list.append(i)

            self.FN_getDatabyID()
        except:
            print(sys.exc_info())


    def FN_EnableDiscVal(self):
        self.valueType="COP_DISCOUNT_VAL"
        self.LE_desc_2.setEnabled(True)
        self.LE_desc_3.setEnabled(False)

    def FN_EnablePercentage(self):
        self.valueType = "COP_DISCOUNT_PERCENT"
        self.LE_desc_3.setEnabled(True)
        self.LE_desc_2.setEnabled(False)

    def FN_Clear(self):
        self.LE_desc_1.clear()
        self.LE_desc_2.clear()
        self.LE_desc_3.clear()
        self.LE_desc_4.clear()
        self.LE_desc_5.clear()


    def FN_SELECT_company(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql="SELECT COMPANY_ID FROM COUPON_BRANCH where COUPON_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_SELECT_branch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql="SELECT BRANCH_NO , STATUS FROM COUPON_BRANCH where COUPON_ID = %s"
        c = (indx,)
        mycursor.execute(sql,c)
        records = mycursor.fetchall()
        mycursor.close()
        return records


    def FN_check_company(self, indx):
        mycursor = self.conn.cursor()
        sql_select_company ="SELECT COMPANY_ID  FROM COMPANY"
        mycursor.execute(sql_select_company)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_company():
                if row[0] == row1[0]:
                    items = self.Qcombo_company.findText(row[0])
                    for item in range(items + 2):
                        self.Qcombo_company.setChecked(i)
            i = i + 1
        mycursor.close()



    def FN_check_branch(self,index):
        self.FN_unCheckedALL()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM BRANCH"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_branch():
                if row[0] == row1[0]:
                    items = self.Qcombo_branch.findText(row[0])
                    for item in range(items +2):
                        if int(row1[1])==1:
                            self.Qcombo_branch.setChecked(i)
            i = i + 1
        mycursor.close()


    def FN_unCheckedALL(self):
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM SYS_USER where USER_NAME='"+CL_userModule.user_name+"'"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i=0
        for row in record:
            self.Qcombo_branch.unChecked(i)
            i+=1



    def FN_GetMathchBranch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO FROM COUPON_BRANCH where COUPON_ID = %s and STATUS = 1"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_AuthBranchUser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_NO FROM SYS_USER where USER_NAME='"+CL_userModule.user_name+"'")
        records = mycursor.fetchall()
        return records

