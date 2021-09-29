from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from access.utils.util import *
from datetime import datetime
import mysql.connector


class CL_ModifyFunctionKey(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(CL_ModifyFunctionKey, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/master_data_ui'
        self.conn = db1.connect()

    ###
    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/ModifyFunctionK.ui'
        loadUi(filename, self)

        self.BTN_search.clicked.connect(self.FN_SEARCH)

        self.BTN_modify.clicked.connect(self.FN_Modify)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())


    def FN_Modify(self):

        mycursor = self.conn.cursor()

        if self.LE_Front_Buttons_Name.text().strip() == '' or self.LE_Front_Buttons_Form.text().strip() == '' \
                or self.LE_Front_Functions_Name.text().strip() == '' or self.LE_Front_Functions_Text.text().strip() == '' :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال ")

        else:
            try:
                self.conn.autocommit = False

                sql0 = "  LOCK  TABLES   Hyper1_Retail.Front_Buttons   WRITE , Hyper1_Retail.Front_Functions  WRITE" \
                       " , Hyper1_Retail.Front_Functions_Buttons  WRITE"
                mycursor.execute(sql0)

                name = self.LE_Front_Buttons_Name.text().strip()

                if name == '':
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الأسم")

                elif name != '':

                    sql_select_query = "SELECT  Front_Buttons_ID   FROM Hyper1_Retail.Front_Buttons where Front_Buttons_Name = '" \
                                       + str(name) + "' "
                    print("Front_Buttons", sql_select_query)

                    mycursor.execute(sql_select_query)
                    records = mycursor.fetchall()
                    if len(records) > 0:
                        for row in records:
                            print("Front_Buttons_ID", row[0])
                            self.Front_Buttons_ID = str(row[0])
                            sql_select_query = "SELECT Front_Functions_ID  FROM Hyper1_Retail.Front_Functions_Buttons where Front_Buttons_ID ='" + str(row[0]) + "'"
                            print("sql_select_query --- Front_Functions_Buttons")
                            mycursor.execute(sql_select_query)
                            recordsFB = mycursor.fetchall()

                            for rowFB in recordsFB:
                                self.Front_Functions_ID = str(rowFB[0])
                                #Front_Buttons
                                sql_update_queryFB = "UPDATE Hyper1_Retail.Front_Buttons SET `Front_Buttons_Form` = %s ,Front_Buttons_Form=%s" \
                                                   " WHERE Front_Buttons_ID = %s"
                                print("sql_select_queryFB --- Front_Functions")
                                val = (self.LE_Front_Buttons_Name.text().strip(), self.LE_Front_Buttons_Form.text().strip() ,self.Front_Buttons_ID)
                                mycursor.execute(sql_update_queryFB, val)

                                # Front_Functions
                                sql_update_queryFF = "UPDATE Hyper1_Retail.Front_Functions SET `Front_Functions_Name` = %s ,Front_Functions_Text=%s" \
                                                   " WHERE Front_Functions_ID = %s"
                                print("sql_select_queryFF --- Front_Functions")
                                valFF = (
                                self.LE_Front_Functions_Name.text().strip(), self.LE_Front_Functions_Text.text().strip(),
                                self.Front_Functions_ID)
                                mycursor.execute(sql_update_queryFF, valFF)

                    else:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "الأسم غير موجود")

                        QtWidgets.QMessageBox.information(self, "بنجاح", "تم الإنشاء")
                        db1.connectionCommit(self.conn)

                    # # unlock table :
                    sql00 = "  UNLOCK   tables    "
                    mycursor.execute(sql00)
                    self.conn.commit()


            except mysql.connector.Error as error:
                print("Failed to update record to database rollback: {}".format(error))
                self.conn.rollback()

                import traceback
                print(traceback.format_exc())
            finally:
                # closing database connection.
                if self.conn.is_connected():
                    # # unlock table :
                    sql00 = "  UNLOCK   tables    "
                    mycursor.execute(sql00)
                    mycursor.close()


    def FN_SEARCH(self):
        try:

            mycursor = self.conn.cursor()
            name = self.LE_Front_Buttons_Name.text().strip()

            if name == '' :
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الأسم")

            elif name != '' :

                sql_select_query = "SELECT  Front_Buttons_ID , Front_Buttons_Name , Front_Buttons_Form  FROM Hyper1_Retail.Front_Buttons where Front_Buttons_Name like '%" \
                                   + str(name) + "%' "
                print("Front_Buttons",sql_select_query)

                mycursor.execute(sql_select_query)
                records = mycursor.fetchall()
                if len(records) >0 :
                    for row in records:
                        print("Front_Buttons_ID",row[0])
                        self.LE_Front_Buttons_Name.setText(row[1])
                        self.LE_Front_Buttons_Form.setText(row[2])

                        sql_select_query = "SELECT Front_Functions_ID  FROM Hyper1_Retail.Front_Functions_Buttons where Front_Buttons_ID ='" + str(row[0]) + "'"
                        print("sql_select_query --- Front_Functions_Buttons")
                        mycursor.execute(sql_select_query)
                        recordsFB = mycursor.fetchall()

                        for rowFB in recordsFB:

                            sql_select_queryFB = "SELECT  Front_Functions_Name , Front_Functions_Text  FROM Hyper1_Retail.Front_Functions" \
                                               " where Front_Functions_ID = " + str(rowFB[0]) + " "
                            print("sql_select_queryFB --- Front_Functions")

                            mycursor.execute(sql_select_queryFB)
                            recordsFF = mycursor.fetchall()
                            for rowFF in recordsFF:
                                self.LE_Front_Functions_Name.setText(rowFF[0])
                                self.LE_Front_Functions_Text.setText(rowFF[1])
                else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "الأسم غير موجود")

        except Exception as err:
            print(err)
            import traceback
            print(traceback.format_exc())

