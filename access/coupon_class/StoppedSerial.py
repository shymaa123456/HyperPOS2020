import sys
from datetime import datetime
from pathlib import Path
from random import randint

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from presentation.Themes.Special_StyleSheet import desc_5


class CL_StoppedSerial(QtWidgets.QDialog):
    serialType=0
    cop_id=""
    serialId=""

    def __init__(self):
        super(CL_StoppedSerial, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/coupon_ui'
        self.conn = db1.connect()

    # Todo: method to load ui of stoppedSerial
    def FN_LOADUI(self):
        filename = self.dirname + '/stoppedSerial.ui'
        loadUi(filename, self)
        self.BTN_search.clicked.connect(self.FN_Search)
        self.CMB_CouponStatus.addItems(["Active"])
        self.BTN_stopCoupon.clicked.connect(self.FN_Stop)
        self.BTN_recreateCoupon.clicked.connect(self.FN_Recreate)

        # Set Style
        # self.label_4.setStyleSheet(label_num)
        self.label_4.setStyleSheet(desc_5)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())

    # Todo: method to search about coupon by barcode
    def FN_Search(self):
        try:
            string=self.lineDesc_2.text()
            x = (string[0:4]+bin(int(string[4:len(string)])))
            print(x)
            sql_select_Query = "select * from COUPON_SERIAL where COPS_BARCODE='"+x+"' and COPS_STATUS=1"
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query)
            record = mycursor.fetchone()
            if mycursor.rowcount > 0:
                self.serialType=record[3]
                self.cop_id=record[1]
                self.serialId=record[0]
                sql_select_Query = "select * from COUPON where COP_ID='"+str(record[1])+"'"
                mycursor.execute(sql_select_Query)
                record = mycursor.fetchone()
                self.lineDesc.setText(record[1])
                if (record[2]!=None and len(record[2]) > 0):
                    self.radioButton_Value.setChecked(True)
                    self.LE_desc_2.setValue(float(record[2]))
                    self.LE_desc_3.clear()
                else:
                    self.radioButton_Percentage.setChecked(True)
                    self.LE_desc_3.setValue(float(record[3]))
                    self.LE_desc_2.clear()
                dateto = record[12]
                xto = dateto.split("-")
                d = QDate(int(xto[2]), int(xto[1]), int(xto[0]))
                self.Qdate_to.setDate(d)
                datefrom = record[11]
                xfrom = datefrom.split("-")
                self.dfrom = QDate(int(xfrom[2]), int(xfrom[1]), int(xfrom[0]))
                self.Qdate_from.setDate(self.dfrom)
                self.LE_desc_4.setValue(float(record[4]))
                if (int(record[5]) == 1):
                    self.checkBox_Multi.setChecked(True)
                    self.LE_desc_5.setValue(float(record[6]))
                else:
                    self.checkBox_Multi.setChecked(False)
                    self.LE_desc_5.clear()
                self.CMB_CouponStatus.setCurrentIndex(int(record[13]))
                self.BTN_stopCoupon.setEnabled(True)
                self.BTN_recreateCoupon.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self, "", "لم يتم العثور علي هذا الباركود")
        except:
            print(sys.exc_info())

    # Todo: method to stop serial of coupon
    def FN_Stop(self):
        mycursor = self.conn.cursor()
        string = self.lineDesc_2.text()
        x = (string[0:4] + bin(int(string[4:len(string)])))
        sql = " update COUPON_SERIAL set COPS_STATUS=0 where COPS_BARCODE=(%s) "
        val = (x,)
        mycursor.execute(sql, val)
        db1.connectionCommit(self.conn)
        mycursor.close()
        QtWidgets.QMessageBox.warning(self, "Done", "Done")

    # Todo: method to refund serial of coupon
    def FN_Recreate(self):
        try:
            value = randint(0, 1000000000000)
            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
            mycursor = self.conn.cursor()
            string = self.lineDesc_2.text()
            x = (string[0:4] + bin(int(string[4:len(string)])))
            sql = " update COUPON_SERIAL set COPS_STATUS=0 where COPS_BARCODE=(%s)"
            val = (x,)
            mycursor.execute(sql, val)
            sql2 = "INSERT INTO COUPON_SERIAL (COUPON_ID,COPS_BARCODE,COPS_CREATED_BY,COPS_SERIAL_type,COPS_CREATED_On,COPS_PRINT_COUNT,COPS_SERIAL_REF,COPS_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val2 = (self.cop_id, "HCOP"+bin(value), CL_userModule.user_name, self.serialType, creationDate, 0,self.serialId ,'1')
            mycursor.execute(sql2, val2)
            QtWidgets.QMessageBox.warning(self, "Done", "new serial is"+str("HCOP"+str(value)))
            db1.connectionCommit(self.conn)
            mycursor.close()
        except:
            print(sys.exc_info())