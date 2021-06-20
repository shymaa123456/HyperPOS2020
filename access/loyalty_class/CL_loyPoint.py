from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp, QDate

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from access.utils.util import *
from datetime import datetime


class CL_loyPoint(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_loyPoint, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()

    ###

    def FN_LOAD_DISPlAY(self):
        try:
            filename = self.dirname + '/loyalityPoint.ui'
            loadUi(filename, self)
            conn = db1.connect()
            mycursor = conn.cursor()
            self.FN_GET_POINTS()
            self.BTN_searchLoyPoint.clicked.connect(self.FN_SEARCH_LOYPOINT)
            self.BTN_searchLoyPoint_all.clicked.connect(self.FN_GET_POINTS)

            self.BTN_createLoyPoint.clicked.connect(self.FN_CREATE_LOYPOINT)
            self.BTN_modifyLoyPoint.clicked.connect(self.FN_MODIFY_LOYPOINT)

            self.setFixedWidth(380)
            self.setFixedHeight(448)
            self.Qtable_point.setColumnHidden(0, True)
            self.Qtable_point.doubleClicked.connect(self.FN_GET_LOYPOINT)
            self.Qtable_point.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            for row_number, row_data in enumerate(CL_userModule.myList):
                if row_data[1] == 'loyality_points':
                    if row_data[4] == 'None':
                        print('hh')
                    else:
                        sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                        x = (row_data[4],)
                        mycursor.execute(sql_select_query, x)

                        result = mycursor.fetchone()
                        # print(result)
                        if result[0] == 'create':
                            self.BTN_createLoyPoint.setEnabled(True)
                            self.BTN_createLoyPoint.clicked.connect(self.FN_CREATE_LOYPOINT)
                        elif result[0] == 'modify':
                            self.BTN_modifyLoyPoint.setEnabled(True)
                            self.BTN_modifyLoyPoint.clicked.connect(self.FN_MODIFY_LOYPOINT)

            valid_from = str(datetime.today().strftime('%Y-%m-%d'))
            xto = valid_from.split("-")
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_from.setDate(d)
            self.Qdate_to.setDate(d)

        except Exception as err:
            print(err)
    def FN_SEARCH_LOYPOINT(self):
        try:
            for i in reversed(range(self.Qtable_redeem.rowCount())):
                self.Qtable_point.removeRow(i)

            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            conn = db1.connect()
            mycursor = conn.cursor()
            whereClause = ""

            whereClause = whereClause + " and `POINTS_VALID_FROM` >= '" + date_from + "' and `POINTS_VALID_TO` <= '" + date_to + "' "


            sql_select_query = "select POINTS_ID, POINTS_QTY,POINTS_VALUE,POINTS_VALID_FROM,POINTS_VALID_TO from Hyper1_Retail.LOYALITY_POINT   where " + whereClause
            # print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_point.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.Qtable_point.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            mycursor.close()
        except Exception as err:
            print(err)
    def FN_GET_POINTS(self):
        self.conn = db1.connect()
        try:
            for i in reversed(range(self.Qtable_point.rowCount())):
                self.Qtable_point.removeRow(i)

            mycursor = self.conn.cursor()
            mycursor.execute(
                "SELECT POINTS_ID,POINTS_QTY,POINTS_VALUE,POINTS_VALID_FROM,POINTS_VALID_TO FROM Hyper1_Retail.LOYALITY_POINT order by POINTS_ID*1   asc")
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_point.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.Qtable_point.setItem(row_number, column_number, item)
            # self.Qtable_redeemTp.doubleClicked.connect(self.FN_GET_CUSTGP)

            # mycursor.close()
        except Exception as err:
            print(err)

    def FN_GET_LOYPOINT(self):
        try:

            if len(self.Qtable_point.selectedIndexes()) > 0:
                rowNo = self.Qtable_point.selectedItems()[0].row()
                id = self.Qtable_point.item(rowNo, 0).text()
                qty = self.Qtable_point.item(rowNo, 1).text()
                val = self.Qtable_point.item(rowNo,2).text()

                valid_from = self.Qtable_redeem.item(rowNo, 3).text()
                valid_to = self.Qtable_redeem.item(rowNo, 5).text()

                self.LB_pointId.setText(id)
                self.LE_pointQty.setValue(qty)
                self.LE_pointValue.setValue(val)

                self.old_qty = qty
                self.old_valid_from = valid_from
                self.old_valid_to = valid_to
                self.old_value = val

                xto = valid_from.split("-")

                d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
                self.Qdate_from.setDate(d)

                xto = valid_to.split("-")

                d1 = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
                self.Qdate_to.setDate(d1)


        except Exception as err:
            print(err)

    def FN_CREATE_LOYPOINT(self):
        date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
        date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
        qty=self.LE_pointQty.text().strip()
        val=self.LE_pointValue.text().strip()
        conn = db1.connect()
        mycursor = conn.cursor()
        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
        creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))
        if qty == 0 or val==0:
            QtWidgets.QMessageBox.warning(self, "Error", "برجاء إدخال جميع البيانات")
        elif date_to < date_from:
            QtWidgets.QMessageBox.warning(self, "خطأ",
                                          "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
        elif date_from < creationDate1:
            QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ الإنشاء  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")
