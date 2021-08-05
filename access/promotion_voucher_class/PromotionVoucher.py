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

from access.utils.util import *
from presentation.Themes.Special_StyleSheet import label_num


class CL_PromVoucher(QtWidgets.QDialog):
    status = ''

    def __init__(self):
        super(CL_PromVoucher, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/promotion_voucher_ui'
        self.conn = db1.connect()


    def FN_LOAD_CREATE(self):
        try:
            filename = self.dirname + '/createPromVoucher.ui'
            loadUi(filename, self)
            datefrom = str(datetime.today().strftime('%Y-%m-%d'))
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setMinimumDate(d)
            self.Qdate_to.setMinimumDate(d)

            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_createVoucher.clicked.connect(self.FN_CREATE_VOUCHER)
            # self.setFixedWidth(418)
            # self.setFixedHeight(223)

            # Set Style
            self.voucher_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except:
            print(sys.exc_info())
    def FN_LOAD_MODIFY(self):
        try:
            filename = self.dirname + '/modifyPromVoucher.ui'
            loadUi(filename, self)

            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_modifyVoucher.clicked.connect(self.FN_MODIFY_VOUCHER)
            self.FN_GET_VOUCHERS()
            self.FN_GET_VOUCHER()
            self.CMB_PromVoucher.currentIndexChanged.connect(self.FN_GET_VOUCHER)
            # رself.setFixedWidth(436)
            # self.setFixedHeight(268)

            # Set Style
            # self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

        except:
            print(sys.exc_info())
    def FN_GET_VOUCHERS(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute(
            "SELECT PROMV_VOUCHER_DESC FROM `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` order by PROMV_VOUCHER_ID asc")

        records = mycursor.fetchall()
        for row in records:
            self.CMB_PromVoucher.addItems([row[0]])
        mycursor.close()

    def FN_GET_VOUCHER(self):
        try :
            desc = self.CMB_PromVoucher.currentText()

            if self.status == '':
                print("ee")
                self.LE_desc.setText(desc)
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute(
                "SELECT PROMV_VOUCHER_ID  ,`PROMV_VOUCHER_VAL`,`PROMV_MAX_COUNT`,`PROMV_VALID_FROM`,`PROMV_VALID_TO`,`PROMV_STATUS` from `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` where PROMV_VOUCHER_DESC = '"+desc+"'")

            records = mycursor.fetchone()
            self.voucher_id.setText(str(records[0]))
            self.LE_value.setValue(records[1])
            self.LE_maxCount.setValue(records[2])
            #for logging
            self.oldDesc = desc
            self.oldValue=records[1]
            self.oldMaxVal = records[2]
            self.oldValidFrom = records[3]
            self.oldValidTo = records[4]

            xto = records[3].split("-")
            print(xto)
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_from.setDate(d)

            xto1 = records[4].split("-")
            d1 = QDate(int(xto1[0]), int(xto1[1]), int(xto1[2]))
            self.Qdate_to.setDate(d1)
            print(xto)
            status = util.FN_GET_STATUS_DESC(str(records[5]))
            self.LE_PromVoucherStatus.setText(status)

            mycursor.close()
        except Exception as err:
           print(err)
    def FN_CREATE_VOUCHER(self):
        try:

            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            creationDate = str(datetime.today().strftime('%Y-%m-%d'))
            if len( self.LE_desc.text().strip()) == 0  or len(self.LE_value.text().strip())== 0 or len(self.LE_maxCount.text().strip() )== 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                desc = self.LE_desc.text().strip()
                sql_select_Query = "select * from `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` where PROMV_VOUCHER_DESC = %s"
                x = (desc,)
                mycursor.execute(sql_select_Query, x)
                record = mycursor.fetchone()
                if mycursor.rowcount > 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")
                elif self.Qdate_to.dateTime() < self.Qdate_from.dateTime():
                        QtWidgets.QMessageBox.warning(self, "Error",
                                                      "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")

                else:


                    sql = "INSERT INTO `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` (`PROMV_VOUCHER_DESC`,`PROMV_VOUCHER_VAL`,`PROMV_MAX_COUNT`,`PROMV_CREATED_BY`,`PROMV_CREATED_ON`,`PROMV_VALID_FROM`,`PROMV_VALID_TO`,`PROMV_STATUS`)VALUES " \
                          "('"+self.LE_desc.text().strip()+"',"+self.LE_value.text().strip()+ ","+self.LE_maxCount.text().strip()+ ",'" +CL_userModule.user_name+"','"+ creationDate+"','"+self.Qdate_from.dateTime().toString('yyyy-MM-dd')+"','"+self.Qdate_to.dateTime().toString('yyyy-MM-dd')+"','0')"
                    print (sql)
                    mycursor.execute(sql)
                    db1.connectionCommit(self.conn)

                    mycursor.execute("SELECT * FROM `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` Where PROMV_VOUCHER_DESC = '" + desc + "'")
                    c = mycursor.fetchone()
                    id = c[0]
                    QtWidgets.QMessageBox.information(self, "Done", "رقم قسيمه الشراء هو " + str(id))
                    self.voucher_num.setText(str(id))


                    mycursor.close()
        except Exception as err:
                    print(err)

    def FN_LOAD_CHANGE_STATUS_INACTIVE(self):
        try:
            filename = self.dirname + '/stopPromVoucher.ui'
            loadUi(filename, self)
            self.status = '0'
            self.FN_GET_VOUCHERS()
            self.FN_GET_VOUCHER()
            self.CMB_PromVoucher.currentIndexChanged.connect(self.FN_GET_VOUCHER)
            # self.setFixedWidth(443)
            # self.setFixedHeight(236)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_changeStatus.clicked.connect(self.FN_CHANGE_STATUS)

            # Set Style
            # self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except Exception as err:
            print(err)

    def FN_LOAD_CHANGE_STATUS_ACTIVE(self):
        try:
            filename = self.dirname + '/stopPromVoucher.ui'
            loadUi(filename, self)
            self.status = '1'
            self.FN_GET_VOUCHERS()
            self.FN_GET_VOUCHER()
            self.CMB_PromVoucher.currentIndexChanged.connect(self.FN_GET_VOUCHER)
            # self.setFixedWidth(443)
            # self.setFixedHeight(236)
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
            self.BTN_changeStatus.clicked.connect(self.FN_CHANGE_STATUS)

            # Set Style
            # self.label_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except Exception as err:
            print(err)

    def FN_CHANGE_STATUS(self):
        try:



                id = self.voucher_id.text()
                self.conn = db1.connect()
                mycursor = self.conn.cursor()

                # get old status
                sql = "select PROMV_STATUS from `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` where PROMV_VOUCHER_ID = %s"
                val = ( id,)
                mycursor.execute(sql, val)
                records = mycursor.fetchone()
                print (records[0])
                print(self.status)
                if self.status!=records[0]:

                    changeDate = str(datetime.today().strftime('%Y-%m-%d'))
                    sql = "update `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` set PROMV_STATUS =%s where PROMV_VOUCHER_ID = %s "

                    val = (self.status, id)
                    mycursor.execute(sql, val)
                    db1.connectionCommit(self.conn)

                    mycursor.close()
                    self.LE_PromVoucherStatus.setText(util.FN_GET_STATUS_DESC(str(self.status)))
                    #add in log table

                    util.FN_INSERT_IN_LOG("PROMOTIONAL_VOUCHER", "status", self.status , records[0], id)

                self.status=''

        except Exception as err:
            print(err)
    def FN_MODIFY_VOUCHER(self):
        try:

            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            changeDate = str(datetime.today().strftime('%Y-%m-%d'))
            if len(self.LE_desc.text().strip()) == 0 or len(self.LE_value.text().strip()) == 0 or len(
                    self.LE_maxCount.text().strip()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                desc = self.LE_desc.text().strip()
                id= self.voucher_id.text().strip()
                sql_select_Query = "select * from `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` where PROMV_VOUCHER_DESC = %s and PROMV_VOUCHER_ID != %s "
                x = (desc,id)
                mycursor.execute(sql_select_Query, x)
                record = mycursor.fetchone()
                if mycursor.rowcount > 0:
                    QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")
                elif self.Qdate_to.dateTime() < self.Qdate_from.dateTime():
                    QtWidgets.QMessageBox.warning(self, "خطا",
                                                  "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")

                else:

                    sql = "update `Hyper1_Retail`.`PROMOTIONAL_VOUCHER` set PROMV_VOUCHER_DESC = %s , `PROMV_VOUCHER_VAL` = %s,`PROMV_MAX_COUNT`  = %s,`PROMV_CHANGED_BY`  = %s,`PROMV_CHANGED_ON`  = %s,`PROMV_VALID_FROM`  = %s,`PROMV_VALID_TO`  = %s where PROMV_VOUCHER_ID =%s" \

                    val = (self.LE_desc.text().strip() , self.LE_value.text().strip(),self.LE_maxCount.text().strip(),changeDate,CL_userModule.user_name,self.Qdate_from.dateTime().toString('yyyy-MM-dd'),self.Qdate_to.dateTime().toString('yyyy-MM-dd'),id)
                    #print(sql)
                    mycursor.execute(sql,val)
                    db1.connectionCommit(self.conn)
                    mycursor.close()
                    QtWidgets.QMessageBox.information(self, "sucess", "تم التعديل")

                    valid_from =self.Qdate_from.dateTime().toString('yyyy-MM-dd')
                    valid_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
                    if self.oldDesc != desc:
                        util.FN_INSERT_IN_LOG("PROMOTIONAL_VOUCHER", "desc",  desc,self.oldDesc, id)
                    if int(self.oldValue) != int(self.LE_value.text().strip()):
                        util.FN_INSERT_IN_LOG("PROMOTIONAL_VOUCHER", "value",  self.LE_value.text().strip(),self.oldValue, id)
                    if self.oldMaxVal != int(self.LE_maxCount.text().strip()):
                        util.FN_INSERT_IN_LOG("PROMOTIONAL_VOUCHER", "max count", self.LE_maxCount.text().strip(),self.oldMaxVal,  id)
                    if self.oldValidFrom != valid_from:
                        util.FN_INSERT_IN_LOG("PROMOTIONAL_VOUCHER", "valid from",valid_from, self.oldValidFrom,  id)
                    if self.oldValidTo != valid_to:
                        util.FN_INSERT_IN_LOG("PROMOTIONAL_VOUCHER", "valid to", valid_to,self.oldValidTo,  id)

        except Exception as err:
            print(err)

