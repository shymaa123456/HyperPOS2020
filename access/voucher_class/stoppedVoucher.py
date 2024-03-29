import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from data_connection.h1pos import db1
from PyQt5.QtCore import QDate, QDateTime


class CL_modifyVoucher(QtWidgets.QDialog):

    def __init__(self):
        super(CL_modifyVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/voucher_ui'
        self.conn = db1.connect()

    # Todo: method to load ui of stoppedVoucher
    def FN_LOADUI(self):
        try:
            filename = self.dirname + '/stoppedVoucher.ui'
            loadUi(filename, self)
            css_path = Path(__file__).parent.parent.parent
            # Apply Style For Design
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
            self.CMB_CouponStatus.addItems(["Inactive", "Active"])
            self.CMB_CouponDes.activated[str].connect(self.FN_getStatus)
            self.FN_getData()
            self.FN_getDatabyID()
            self.FN_getStatus()
            self.BTN_modifyCoupon.clicked.connect(self.FN_UpdateStatus)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        except:
            print(sys.exc_info())

    # Todo: method to get all voucher
    def FN_getData(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT GV_DESC,GV_ID FROM VOUCHER")
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_CouponDes.addItem(row,val)
        mycursor.close()

    # Todo: method to get data of voucher
    def FN_getDatabyID(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            indx = self.CMB_CouponDes.currentData()
            self.labe_id.setText(str(indx))
            sql_select_Query = "SELECT * FROM VOUCHER where GV_ID = %s "
            x = (indx,)
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            self.LE_desc_2.setValue(float(record[4]))
            datefrom = record[12]
            xfrom = datefrom.split("-")
            self.dfrom = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setDate(self.dfrom)
            self.dfrom = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            dateto = record[14]
            xto = dateto.split("-")
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_to.setDate(d)

            if(record[18]=="1"):
                self.checkBox_Multi.setChecked(True)
            elif(record[17]=="1"):
                self.checkBox_rechange.setChecked(True)
            elif (record[16] == "1"):
                self.checkBox_refundable.setChecked(True)
            sql_select_Query3 = "select * from POS_CUSTOMER where POSC_CUST_ID ='" + str(record[19]) + "'"
            print(sql_select_Query3)
            mycursor.execute(sql_select_Query3)
            record3 = mycursor.fetchone()
            self.LE_desc_5.setText(str(record3[0]))
            self.desc_13.setText(str(record3[3]))

            sql_select_Query2 = "SELECT * from SPONSOR where SPONSOR_ID=( SELECT SPONSER_ID FROM VOUCHER_SPONSOR where GV_ID = '"+str(record[0])+"')"
            print(sql_select_Query2)
            mycursor.execute(sql_select_Query2)
            record2 = mycursor.fetchone()
            self.LE_desc_6.setText(record2[2])
            mycursor.close()
        except:
            print(sys.exc_info())

    # Todo: method to get status of voucher
    def FN_getStatus(self):
        indx = self.CMB_CouponDes.currentData()
        self.conn = db1.connect()
        sql_select_Query = "SELECT GV_STATUS FROM VOUCHER where GV_ID = %s "
        x = (indx,)
        mycursor = self.conn.cursor()
        mycursor.execute(sql_select_Query, x)
        records = mycursor.fetchone()
        for row in records:
            int(row)
            self.CMB_CouponStatus.setCurrentIndex(int(row))
        mycursor.close()
        self.FN_getDatabyID()

    # Todo: method to change status of voucher
    def FN_UpdateStatus(self):
        mycursor = self.conn.cursor()
        print(self.CMB_CouponStatus.currentIndex())
        print(self.CMB_CouponDes.currentData())
        sql = "update VOUCHER set GV_STATUS='"+str(self.CMB_CouponStatus.currentIndex())+"' where GV_ID='"+str(self.CMB_CouponDes.currentData())+"'"
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
