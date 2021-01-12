from pathlib import Path
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_EditCoupon(QtWidgets.QDialog):
    valueType=""
    valueData=""
    serialCount = ""
    MultiCount = ""
    MultiUse = ""
    def __init__(self):
        super(CL_EditCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()

    def FN_LOADUI(self):
        filename = self.dirname + '/editCoupon.ui'
        loadUi(filename, self)
        self.CMB_CouponStatus.addItems(["Active", "Inactive"])
        self.FN_getData()
        self.CMB_CouponDes.activated[str].connect(self.FN_getDatabyID)
        self.FN_getDatabyID()
        self.radioButton_Value.clicked.connect(self.FN_EnableDiscVal)
        self.radioButton_Percentage.clicked.connect(self.FN_EnablePercentage)
        self.checkBox_Multi.toggled.connect(self.FN_endableMultiUser)
        self.BTN_editCoupon.clicked.connect(self.FN_editAction)



    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_DESC,COP_ID FROM COUPON")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()

    def FN_getDatabyID(self):
        self.FN_Clear()
        indx = self.CMB_CouponDes.currentData()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT * FROM COUPON where COP_ID = '" + indx + "'")
        record = mycursor.fetchone()
        self.LE_desc_1.setText(record[1])
        if(len(record[2])>0):
            self.radioButton_Value.setChecked(True)
            self.LE_desc_2.setText(str(record[2]))
            self.LE_desc_2.setEnabled(True)
            self.LE_desc_3.setEnabled(False)
            self.LE_desc_3.clear()
            self.valueType = "COP_DISCOUNT_VAL"
            self.valueData = self.LE_desc_2.text()
        else:
            self.radioButton_Percentage.setChecked(True)
            self.LE_desc_3.setText(str(record[3]))
            self.LE_desc_3.setEnabled(True)
            self.LE_desc_2.setEnabled(False)
            self.LE_desc_2.clear()
            self.valueType = "COP_DISCOUNT_PERCENT"
            self.valueData =self.LE_desc_3.text()

        dateto=record[12]
        xto = dateto.split("-")
        d = QDate(int(xto[0]),int(xto[1]),int(xto[2]))
        self.Qdate_to.setDate(d)

        datefrom = record[11]
        xfrom = datefrom.split("-")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        self.Qdate_from.setDate(d)

        self.LE_desc_4.setText(str(record[4]))
        print(record[5])
        if (int(record[5])==0):
            self.checkBox_Multi.setChecked(True)
            self.LE_desc_5.setText(str(record[6]))
            self.LE_desc_5.setEnabled(True)
            self.LE_desc_4.setEnabled(False)
        else:
            self.checkBox_Multi.setChecked(False)
            self.LE_desc_5.setEnabled(False)
            self.LE_desc_4.setEnabled(True)

        self.CMB_CouponStatus.setCurrentIndex(int(record[13]))
        mycursor.close()

    def FN_endableMultiUser(self):
        if self.checkBox_Multi.isChecked():
            self.LE_desc_5.setEnabled(True)
            self.LE_desc_4.setEnabled(False)
        else:
            self.LE_desc_5.setEnabled(False)
            self.LE_desc_4.setEnabled(True)

    def FN_editAction(self):
        mycursor = self.conn.cursor()
        creationDate = str(datetime.today().strftime('%Y-%m-%d'))
        if self.checkBox_Multi.isChecked():
            self.serialCount="1"
            self.MultiCount=self.LE_desc_5.text()
            self.MultiUse="0"
        else:
            self.serialCount=self.LE_desc_4.text()
            self.MultiCount = "0"
            self.MultiUse = "1"
        sql = "update COUPON set COP_DESC='" + self.LE_desc_1.text() + "'," + self.valueType + "=" + self.valueData + ",COP_SERIAL_COUNT="+self.serialCount+",COP_MULTI_USE="+self.MultiUse+",COP_MULTI_USE_COUNT="+self.MultiCount+",COP_CHANGED_BY='"+CL_userModule.user_name+"',COP_CHANGED_ON='"+creationDate+"',COP_VALID_FROM='"+self.Qdate_from.dateTime().toString('yyyy-MM-dd')+"',COP_VALID_TO='"+self.Qdate_to.dateTime().toString('yyyy-MM-dd')+"',COP_STATUS='" + str(self.CMB_CouponStatus.currentIndex()) + "' where COP_ID='" + str(self.CMB_CouponDes.currentData()) + "'"
        mycursor.execute(sql)
        db1.connectionCommit(self.conn)
        mycursor.close()
        QtWidgets.QMessageBox.warning(self, "Done", "Done")


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