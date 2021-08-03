import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from data_connection.h1pos import db1
from PyQt5.QtCore import QDate

from presentation.Themes.Special_StyleSheet import desc_5


class CL_modifyCoupon(QtWidgets.QDialog):

    def __init__(self):
        super(CL_modifyCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()

    # Todo: method to load ui of stoppedCoupon
    def FN_LOADUI(self):
        try:
            filename = self.dirname + '/stoppedCoupon.ui'
            loadUi(filename, self)
            self.CMB_CouponStatus.addItems(["Inactive", "Active"])
            self.CMB_CouponDes.activated[str].connect(self.FN_getStatus)
            self.FN_getData()
            self.FN_getDatabyID()
            self.FN_getStatus()
            self.BTN_modifyCoupon.clicked.connect(self.FN_UpdateStatus)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

            # Set Style
            # self.label.setStyleSheet(label_num)
            self.label.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except:
            print(sys.exc_info())

    # Todo: method to get all coupons
    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_DESC,COP_ID FROM COUPON")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()

    # Todo: method to get data of coupon
    def FN_getDatabyID(self):
        try:
            indx = self.CMB_CouponDes.currentData()
            self.labe_id.setText(str(indx))
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            sql_select_Query = "SELECT * FROM COUPON where COP_ID = %s "
            x = (indx,)
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            self.COPDISCOUNToldVAL=str(record[2])

            if (record[2]!=None and len(self.COPDISCOUNToldVAL) > 0):
                self.radioButton_Value.setChecked(True)
                self.LE_desc_2.setValue(float(record[2]))
                self.LE_desc_3.clear()
                self.valueType = "COP_DISCOUNT_VAL"
                self.valueData = self.LE_desc_2.text()
            else:
                self.radioButton_Percentage.setChecked(True)
                self.LE_desc_3.setValue(float(record[3]))
                self.LE_desc_2.clear()
                self.valueType = "COP_DISCOUNT_PERCENT"
                self.valueData = self.LE_desc_3.text()
            dateto = record[13]
            xto = dateto.split("-")
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_to.setDate(d)
            datefrom = record[11]
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setDate(d)
            self.LE_desc_4.setValue(float(record[4]))
            print(record[5])
            if (int(record[5]) == 0):
                self.checkBox_Multi.setChecked(True)
                self.LE_desc_5.setValue(float(record[6]))
            else:
                self.checkBox_Multi.setChecked(False)
            self.CMB_CouponStatus.setCurrentIndex(int(record[13]))
            mycursor.close()
        except:
            print(sys.exc_info())

    # Todo: method to get status of coupon
    def FN_getStatus(self):
        indx = self.CMB_CouponDes.currentData()
        self.conn = db1.connect()
        sql_select_Query = "SELECT COP_STATUS FROM COUPON where COP_ID = %s "
        x = (indx,)
        mycursor = self.conn.cursor()
        mycursor.execute(sql_select_Query, x)
        records = mycursor.fetchone()
        for row in records:
            int(row)
            self.CMB_CouponStatus.setCurrentIndex(int(row))
        mycursor.close()
        self.FN_getDatabyID()

    # Todo: method to edit status of coupon
    def FN_UpdateStatus(self):
        mycursor = self.conn.cursor()
        print(self.CMB_CouponStatus.currentIndex())
        print(self.CMB_CouponDes.currentData())
        sql = "update COUPON set COP_STATUS='"+str(self.CMB_CouponStatus.currentIndex())+"' where COP_ID='"+str(self.CMB_CouponDes.currentData())+"'"
        mycursor.execute(sql)
        db1.connectionCommit(self.conn)
        mycursor.close()
        QtWidgets.QMessageBox.warning(self, "Done", "Done")
        self.close()

    # Todo: method to clear edit text
    def FN_Clear(self):
        self.LE_desc_2.clear()
        self.LE_desc_3.clear()
        self.LE_desc_4.clear()
        self.LE_desc_5.clear()