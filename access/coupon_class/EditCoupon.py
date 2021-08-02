import collections
import sys
from pathlib import Path
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.uic import loadUi

from access.Checkable import CheckableComboBox
from presentation.Themes.Special_StyleSheet import label_num, desc_5
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_EditCoupon(QtWidgets.QDialog):
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
    dfrom=QDate(1,1,2000)
    Special=0
    DescOldValue= ""
    COPDISCOUNToldVAL= ""
    COPDISCOUNToldprecnt= ""
    Othertype=""
    row=""
    oldlist=[]
    newlist=[]
    oldstatus=""

    def __init__(self):
        super(CL_EditCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()

    #Todo: method to load ui of edit coupon
    def FN_LOADUI(self):
        filename = self.dirname + '/editCoupon.ui'
        loadUi(filename, self)
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(350, 135, 271, 25)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(350, 165, 271, 25)
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
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        # Set Style
        self.labe_id.setStyleSheet(label_num)
        self.label.setStyleSheet(desc_5)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())

    #Todo: method for fills the company combobox
    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    # Todo: method for fills the Branch combobox
    def FN_GET_Branch(self):
        i = 0
        try:
            for row, val in CL_userModule.branch:
                self.Qcombo_branch.addItem(val, row)
                i += 1
        except:
            print(sys.exc_info())

    # Todo: method to get name and id of coupon
    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_DESC,COP_ID FROM COUPON")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()

    # Todo: method to get all data about coupon
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
            self.row=record[0]
            self.LE_desc_1.setText(record[1])
            self.DescOldValue=record[1]
            self.COPDISCOUNToldVAL=str(record[2])
            self.COPDISCOUNToldprecnt=str(record[3])
            if (record[2]!=None and len(self.COPDISCOUNToldVAL) > 0):
                self.radioButton_Value.setChecked(True)
                self.LE_desc_2.setValue(float(record[2]))
                self.LE_desc_2.setEnabled(True)
                self.LE_desc_3.setEnabled(False)
                self.LE_desc_3.clear()
                self.valueType = "COP_DISCOUNT_VAL"
                self.valueData = self.LE_desc_2.text()
                self.Othertype="COP_DISCOUNT_PERCENT"
            else:
                self.radioButton_Percentage.setChecked(True)
                self.LE_desc_3.setValue(float(record[3]))
                self.LE_desc_3.setEnabled(True)
                self.LE_desc_2.setEnabled(False)
                self.LE_desc_2.clear()
                self.valueType = "COP_DISCOUNT_PERCENT"
                self.valueData = self.LE_desc_3.text()
                self.Othertype="COP_DISCOUNT_VAL"
            dateto = record[13]
            xto = dateto.split("-")
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_to.setDate(d)
            datefrom = record[11]
            xfrom = datefrom.split("-")
            self.dfrom = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setDate(self.dfrom)
            self.dfrom=QDateTime(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]),00,00,00,00)
            self.LE_desc_4.setValue(float(record[4]))
            self.serial_num=int(record[4])
            self.multiusage=int(record[5])
            self.Special=int(record[5])
            if (int(record[5]) == 1):
                self.checkBox_Multi.setChecked(True)
                self.LE_desc_5.setValue(float(record[6]))
                self.LE_desc_4.setEnabled(False)
                self.LE_desc_5.setEnabled(True)
            else:
                self.checkBox_Multi.setChecked(False)
                self.LE_desc_5.setEnabled(False)
                self.LE_desc_4.setEnabled(True)
            self.CMB_CouponStatus.setCurrentIndex(int(record[15]))
            self.oldstatus =str(record[15])


            timefrom = record[12]
            tfrom = timefrom.split(":")
            some_time = QtCore.QTime(int(tfrom[0]), int(tfrom[1]), 00)
            self.Qtime_from.setTime(some_time)

            timeto = record[14]
            tto = timeto.split(":")
            some_time = QtCore.QTime(int(tto[0]), int(tto[1]), 00)
            self.Qtime_to.setTime(some_time)

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
                if (record[2] != None and len(self.COPDISCOUNToldVAL) > 0):
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
            self.oldlist=self.Qcombo_branch.currentData()
         except:
             print(sys.exc_info())

    # Todo: method to make coupon multi use
    def FN_endableMultiUser(self):
        if self.checkBox_Multi.isChecked():
            self.LE_desc_5.setEnabled(True)
            self.LE_desc_4.setEnabled(False)
            self.LE_desc_4.setValue(1.0)
            self.multiusage=1
        else:
            self.LE_desc_5.setEnabled(False)
            self.LE_desc_4.setEnabled(True)
            self.multiusage=0

    # Todo: method to edit coupon
    def FN_editAction(self):
        try:
            self.newlist = self.Qcombo_branch.currentData()
            if len(self.Qcombo_company.currentData()) == 0 or len(self.Qcombo_branch.currentData()) == 0 or len(
                    self.LE_desc_1.text().strip()) == 0 or len(self.LE_desc_3.text().strip()) == 0 and len(self.LE_desc_2.text().strip()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                if self.Qdate_to.dateTime()<self.Qdate_from.dateTime():
                    QtWidgets.QMessageBox.warning(self, "Done", "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                elif self.Qdate_from.dateTime()<self.dfrom:
                    QtWidgets.QMessageBox.warning(self, "Done", "تاريخ الانشاء الجديد يجب ان يكون اكبر او يساوي تاريخ الانشاء قبل التعديل")
                elif (self.Qdate_from.date() == self.Qdate_to.date()) and int(self.Qtime_from.dateTime().toString('hh')) + int(
                            self.Qtime_from.dateTime().toString('mm')) > int(
                            self.Qtime_to.dateTime().toString('hh')) + int(self.Qtime_to.dateTime().toString('mm')):
                            QtWidgets.QMessageBox.warning(self, "خطا",
                            "وقت الانتهاء يجب ان يكون اكبر من او يساوي وقت الانشاء")

                else:
                    mycursor = self.conn.cursor()
                    creationDate = str(datetime.today().strftime('%Y-%m-%d'))
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
                            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
                            mycursor = self.conn.cursor()
                            sql7 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val7 = (
                                str(self.CMB_CouponDes.currentData()), "HCOP"+bin(value), CL_userModule.user_name,self.serial_type,
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
                        if self.valueType == "COP_DISCOUNT_VAL":
                            self.valueData = self.LE_desc_2.text()
                        elif self.valueType == "COP_DISCOUNT_PERCENT":
                            self.valueData = self.LE_desc_3.text()
                        sql = "update COUPON set COP_DESC='" + self.LE_desc_1.text().strip() + "'," + self.valueType + "=" + self.valueData +","+self.Othertype+"="+"null"+",COP_SERIAL_COUNT=" + self.serialCount + ",COP_MULTI_USE=" + self.MultiUse + ",COP_MULTI_USE_COUNT=" + self.MultiCount + ",COP_CHANGED_BY='" + CL_userModule.user_name + "',COP_CHANGED_ON='" + creationDate + "',COP_VALID_FROM='" + self.Qdate_from.dateTime().toString(
                            'dd-MM-yyyy') + "',COP_VALID_TO='" + self.Qdate_to.dateTime().toString(
                            'dd-MM-yyyy') + "',COP_STATUS='" + str(
                            self.CMB_CouponStatus.currentIndex()) + "',COP_TIME_FROM='"+str(self.Qtime_from.dateTime().toString('hh:mm'))+"',COP_TIME_TO='"+str(self.Qtime_to.dateTime().toString('hh:mm'))+"' where COP_ID='" + str(
                            self.CMB_CouponDes.currentData()) + "'"
                        print(sql)
                        mycursor.execute(sql)
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
                        if(self.multiusage==1):
                            mycursor = self.conn.cursor()
                            sql9 = "update COUPON_SERIAL set COPS_STATUS= 0 where COUPON_ID='" + str(
                                     self.CMB_CouponDes.currentData()) + "' and COPS_SERIAL_type = 0"
                            mycursor.execute(sql9)
                            value = randint(0, 1000000000000)
                            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
                            mycursor = self.conn.cursor()
                            sql7 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val7 = (
                                str(self.CMB_CouponDes.currentData()), "HCOP" + bin(value),
                                CL_userModule.user_name,
                                self.serial_type,
                                creationDate, 0,
                                '1')
                            mycursor.execute(sql7, val7)
                        else:
                            mycursor = self.conn.cursor()
                            if(int(self.Special)==1):
                                self.serial_num=0
                                print("num"+str(self.serial_num))
                            sql9 = "update COUPON_SERIAL set COPS_STATUS= 0 where COUPON_ID='" + str(
                                self.CMB_CouponDes.currentData()) + "' and COPS_SERIAL_type = 1"
                            mycursor.execute(sql9)
                            if int(self.LE_desc_4.text()) < self.serial_num:
                                indx = self.CMB_CouponDes.currentData()
                                sql_select_Query = "SELECT COPS_SERIAL_ID FROM COUPON_SERIAL where COUPON_ID = %s and COPS_STATUS = 1 and COPS_SERIAL_type = 0"
                                x = (indx,)
                                mycursor = self.conn.cursor()
                                mycursor.execute(sql_select_Query, x)
                                record = mycursor.fetchall()
                                print(record)
                                num = 0
                                for row in range(self.serial_num - int(self.LE_desc_4.text())):
                                    mycursor = self.conn.cursor()
                                    sql9 = "update COUPON_SERIAL set COPS_STATUS= 0 where COUPON_ID='" + str(
                                        self.CMB_CouponDes.currentData()) + "' and COPS_SERIAL_ID = '" + str(
                                        record[num][0]) + "'"
                                    mycursor.execute(sql9)
                                    print(sql9)
                                    num += 1
                                self.serial_num = int(self.LE_desc_4.text())
                            else:
                                for row in range(int(self.LE_desc_4.text()) - self.serial_num):
                                    value = randint(0, 1000000000000)
                                    creationDate = str(datetime.today().strftime('%Y-%m-%d'))
                                    mycursor = self.conn.cursor()
                                    sql7 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                    val7 = (
                                        str(self.CMB_CouponDes.currentData()), "HCOP" + bin(value),
                                        CL_userModule.user_name,
                                        self.serial_type,
                                        creationDate, 0,
                                        '1')
                                    mycursor.execute(sql7, val7)
                                self.serial_num = int(self.LE_desc_4.text())
                        if (self.LE_desc_1.text() != self.DescOldValue):
                            CL_userModule.FN_AddLog(self,'COUPON', 'COP_DESC', self.DescOldValue, self.LE_desc_1.text().strip(), creationDate,
                                    CL_userModule.user_name,self.row,None,None,None,None,mycursor)
                        elif (self.CMB_CouponStatus.currentIndex() != self.oldstatus):
                            sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val8 = (self.row, 'COUPON', 'STATUS', self.oldstatus,
                                    str(self.CMB_CouponStatus.currentIndex()),
                                    creationDate,
                                    CL_userModule.user_name)
                            mycursor.execute(sql8, val8)
                        elif collections.Counter(self.Qcombo_branch.currentData())== collections.Counter(self.oldlist):
                             print("the same list")
                        elif len(collections.Counter(self.Qcombo_branch.currentData())) > len(collections.Counter(self.oldlist)):
                            print(self.Diff(self.newlist, self.oldlist))
                            if len(collections.Counter(self.Qcombo_branch.currentData())) > len(collections.Counter(record)):
                                for row in self.Diff(record, self.newlist):
                                    sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                    val8 = (self.row, 'COUPON_BRANCH', 'STATUS', "null",
                                            "1",
                                            creationDate,
                                            CL_userModule.user_name, row)
                                    mycursor.execute(sql8, val8)
                            else:
                                for row in self.Diff(self.oldlist, self.newlist):
                                    sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                    val8 = (self.row, 'COUPON_BRANCH', 'STATUS', "0",
                                            "1",
                                            creationDate,
                                            CL_userModule.user_name, row)
                                    mycursor.execute(sql8, val8)
                        elif len(collections.Counter(self.Qcombo_branch.currentData())) < len(collections.Counter(self.oldlist)):
                            print(self.Diff(self.oldlist, self.newlist))
                            for row in self.Diff(self.oldlist, self.newlist):
                                sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                val8 = (self.row, 'COUPON_BRANCH', 'STATUS', "1",
                                        "0",
                                        creationDate,
                                        CL_userModule.user_name, row)
                                mycursor.execute(sql8, val8)
                        elif(self.LE_desc_2.text() != self.COPDISCOUNToldVAL):
                            sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val8 = (self.row, 'COUPON', 'COP_DISCOUNT_VAL', self.COPDISCOUNToldVAL, self.LE_desc_2.text().strip(),
                                    creationDate,
                                    CL_userModule.user_name)
                            mycursor.execute(sql8, val8)
                        elif (self.LE_desc_3.text() != self.COPDISCOUNToldprecnt):
                            sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val8 = (self.row, 'COUPON', 'COP_DISCOUNT_PERCENT', self.COPDISCOUNToldprecnt,
                                    self.LE_desc_3.text().strip(),
                                    creationDate,
                                    CL_userModule.user_name)
                            mycursor.execute(sql8, val8)
                        db1.connectionCommit(self.conn)
                        mycursor.close()
                        QtWidgets.QMessageBox.warning(self, "Done", "Done")
                        for i in self.FN_GetMathchBranch():
                            self.branch_list.append(i)
            self.FN_getDatabyID()
        except:
            print(sys.exc_info())

    # Todo: method when make coupon use DISCOUNT_VAL
    def FN_EnableDiscVal(self):
        self.valueType="COP_DISCOUNT_VAL"
        self.LE_desc_2.setEnabled(True)
        self.LE_desc_3.setEnabled(False)
        self.Othertype="COP_DISCOUNT_PERCENT"

    # Todo: method when make coupon use DISCOUNT_PERCENT
    def FN_EnablePercentage(self):
        self.valueType = "COP_DISCOUNT_PERCENT"
        self.LE_desc_3.setEnabled(True)
        self.LE_desc_2.setEnabled(False)
        self.Othertype="COP_DISCOUNT_VAL"

    # Todo: method to clear edit text
    def FN_Clear(self):
        self.LE_desc_1.clear()
        self.LE_desc_2.clear()
        self.LE_desc_3.clear()
        self.LE_desc_4.clear()
        self.LE_desc_5.clear()

    # Todo: method to get company assigned to coupon
    def FN_SELECT_company(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql="SELECT COMPANY_ID FROM COUPON_BRANCH where COUPON_ID = %s"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method to get branch assigned to coupon
    def FN_SELECT_branch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql="SELECT BRANCH_NO , STATUS FROM COUPON_BRANCH where COUPON_ID = %s"
        c = (indx,)
        mycursor.execute(sql,c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method to get check company assigned to coupon
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

    # Todo: method to get check branch assigned to coupon
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

    # Todo: method refresh Qcombo_branch
    def FN_unCheckedALL(self):
        i=0
        for row in CL_userModule.branch:
            self.Qcombo_branch.unChecked(i)
            i+=1

    # Todo: method get branch has this coupon
    def FN_GetMathchBranch(self):
        indx = self.CMB_CouponDes.currentData()
        mycursor = self.conn.cursor()
        sql = "SELECT BRANCH_NO FROM COUPON_BRANCH where COUPON_ID = %s and STATUS = 1"
        c = (indx,)
        mycursor.execute(sql, c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    # Todo: method get diff between two list
    def Diff(self,li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
