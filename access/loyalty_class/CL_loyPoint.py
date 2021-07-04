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

            self.setFixedWidth(511)
            self.setFixedHeight(450)
            self.Qtable_point.setColumnHidden(0, True)
            self.Qtable_point.doubleClicked.connect(self.FN_GET_LOYPOINT)
            self.Qtable_point.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            for row_number, row_data in enumerate(CL_userModule.myList):

                if row_data[1] == 'Loyality_Point':

                    if row_data[4] == 'None':
                        print('hh')
                    else:

                        sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                        x = (row_data[4],)
                        mycursor.execute(sql_select_query, x)
                        result = mycursor.fetchone()
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
            self.creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
        except Exception as err:
            print(err)
    def FN_SEARCH_LOYPOINT(self):
        try:
            for i in reversed(range(self.Qtable_point.rowCount())):
                self.Qtable_point.removeRow(i)

            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            conn = db1.connect()
            mycursor = conn.cursor()
            whereClause = ""

            whereClause =" `POINTS_VALID_FROM` >= '" + date_from + "' and `POINTS_VALID_TO` <= '" + date_to + "' "


            sql_select_query = "select POINTS_ID, POINTS_QTY,POINTS_VALUE,POINTS_VALID_FROM,POINTS_VALID_TO from Hyper1_Retail.LOYALITY_POINT   where " + whereClause
            print(sql_select_query)
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

                valid_from = self.Qtable_point.item(rowNo, 3).text()
                valid_to = self.Qtable_point.item(rowNo, 4).text()

                self.LB_pointId.setText(id)
                self.LE_pointQty.setValue(int(qty))
                self.LE_pointValue.setValue(float(val))
                # set old values
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
    def FN_CHK_PT_VALIDITY (self,f_new ,t_new):
        ret=False
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT POINTS_VALID_FROM , POINTS_VALID_TO FROM Hyper1_Retail.LOYALITY_POINT  ")
        records = mycursor.fetchall()
        if records != None :
            for date_from,date_to in  records :
                #t_new = f_new.date().toString('yyyy-MM-dd')
                #date_to = t_new.date().toString('yyyy-MM-dd')
                if (f_new < date_from and t_new < date_from ) or ( f_new> date_to and t_new > date_to):
                    ret = True
        return ret

    def FN_CREATE_LOYPOINT(self):
        try:
            date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
            ret=self.FN_CHK_PT_VALIDITY(date_from,date_to)
            if ret == False:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء العلم أنه يوجد فتره فعاله ")
            else:

                qty = self.LE_pointQty.text().strip()
                val = self.LE_pointValue.text().strip()
                conn = db1.connect()
                mycursor = conn.cursor()

                creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))
                if qty == 0 or val==0:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
                elif date_to < date_from:
                    QtWidgets.QMessageBox.warning(self, "خطأ",
                                                  "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                elif date_from < creationDate1:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ الإنشاء  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")
                else:
                    mycursor.execute("SELECT max(cast(POINTS_ID  AS UNSIGNED)) FROM Hyper1_Retail.LOYALITY_POINT")
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        id = "1"
                    else:
                        id = int(myresult[0]) + 1

                    sql = "INSERT INTO Hyper1_Retail.LOYALITY_POINT ( POINTS_ID, POINTS_QTY,POINTS_VALUE,POINTS_VALID_FROM,POINTS_VALID_TO,POINTS_CREATED_ON,POINTS_CREATED_BY)   VALUES ( '" +str(id)+"', '"+str(qty)+"','"+str(val)+"' ,'"+date_from+"','"+date_to+"','"+self.creationDate+"','"+CL_userModule.user_name+"')"

                    # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                    print(sql)
                    #val = (id, qty, val,date_from,date_to,creationDate,CL_userModule.user_name)
                    #print(val)
                    mycursor.execute(sql)
                    db1.connectionCommit(conn)
                    print(mycursor.rowcount, "loy point inserted.")
                    QtWidgets.QMessageBox.information(self, "تم", "تم الإنشاء")
                    mycursor.close()
                    self.FN_GET_POINTS()
                    self.FN_CLEAR_FEILDS()
        except Exception as err:
            print(err)
    def FN_MODIFY_LOYPOINT(self):
        try:
                if len(self.Qtable_point.selectedIndexes()) > 0:


                    id = self.LB_pointId.text()
                    date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
                    date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
                    qty=self.LE_pointQty.text().strip()
                    val=self.LE_pointValue.text().strip()
                    conn = db1.connect()
                    mycursor = conn.cursor()

                    creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))

                    if qty == 0 or val == 0:
                        QtWidgets.QMessageBox.warning(self, "Error", "برجاء إدخال جميع البيانات")
                    elif date_to < date_from:
                        QtWidgets.QMessageBox.warning(self, "خطأ",
                                                      "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                    elif date_from < creationDate1:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ التعديل  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")

                    else:


                            sql = "update   Hyper1_Retail.LOYALITY_POINT " \
                                  "set POINTS_QTY =%s,POINTS_VALUE =%s , POINTS_VALID_FROM = %s , " \
                                  "POINTS_VALID_TO =%s where POINTS_ID = %s "
                            val = (qty,val,date_from,date_to,id)

                            mycursor.execute(sql, val)
                            mycursor.close()

                            print(mycursor.rowcount, "record updated.")
                            QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل ")

                            db1.connectionCommit(conn)
                            self.FN_GET_POINTS()

                            if str(qty) != str(self.old_qty):
                                util.FN_INSERT_IN_LOG("LOYALITY_POINT", "quantity", qty, self.old_qty, id)
                            if str(val) != str(self.old_value):
                                util.FN_INSERT_IN_LOG("LOYALITY_POINT","value", val, self.old_value,id)

                            if str(date_from) != str(self.old_valid_from):
                                util.FN_INSERT_IN_LOG("LOYALITY_POINT", "valid_from", date_from, self.old_valid_from, id)

                            if str(date_to) != str(self.old_valid_to):
                                util.FN_INSERT_IN_LOG("LOYALITY_POINT", "valid_to", date_to, self.old_valid_to, id)
                            print("in modify loy pt")
                else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")
        except Exception as err:
            print(err)

    def FN_CLEAR_FEILDS(self):
        self.LB_pointId.setText('')
        self.LE_pointQty.setValue(0)
        self.LE_pointValue.setValue(0)