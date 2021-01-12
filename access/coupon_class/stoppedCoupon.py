from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime


class CL_modifyCoupon(QtWidgets.QDialog):

    def __init__(self):
        super(CL_modifyCoupon, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()


    def FN_LOADUI(self):
        filename = self.dirname + '/stoppedCoupon.ui'
        loadUi(filename, self)
        self.CMB_CouponStatus.addItems(["Active", "Inactive"])
        self.FN_getData()
        self.CMB_CouponDes.activated[str].connect(self.FN_getStatus)
        self.FN_getStatus()
        self.BTN_modifyCoupon.clicked.connect(self.FN_UpdateStatus)

    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_DESC,COP_ID FROM COUPON")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()

    def FN_getStatus(self):
        indx = self.CMB_CouponDes.currentData()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COP_STATUS FROM COUPON where COP_ID = '" + indx + "'")
        records = mycursor.fetchone()
        for row in records:
            int(row)
            self.CMB_CouponStatus.setCurrentIndex(int(row))
        mycursor.close()


    def FN_UpdateStatus(self):
        mycursor = self.conn.cursor()
        print(self.CMB_CouponStatus.currentIndex())
        print(self.CMB_CouponDes.currentData())
        sql = "update COUPON set COP_STATUS='"+str(self.CMB_CouponStatus.currentIndex())+"' where COP_ID='"+str(self.CMB_CouponDes.currentData())+"'"
        mycursor.execute(sql)
        sql2 = "update COUPON_SERIAL set COPS_STATUS='" + str(self.CMB_CouponStatus.currentIndex()) + "' where COUPON_ID='" + str(self.CMB_CouponDes.currentData()) + "'"
        mycursor.execute(sql2)
        sql3 = "update COUPON_BRANCH set STATUS='" + str(
            self.CMB_CouponStatus.currentIndex()) + "' where COUPON_ID='" + str(self.CMB_CouponDes.currentData()) + "'"
        mycursor.execute(sql3)
        db1.connectionCommit(self.conn)
        mycursor.close()
        QtWidgets.QMessageBox.warning(self, "Done", "Done")
        self.close()



