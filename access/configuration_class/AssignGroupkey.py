import sys
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox


class CL_FNGroupKey(QtWidgets.QDialog):
    def __init__(self):
        super(CL_FNGroupKey, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Pos_Group_Key.ui'
        loadUi(filename, self)
        self.setWindowTitle('Assign Group Key')
        self.CMB_Status.addItems(["Inactive","Active"])
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        self.pushButton.clicked.connect(self.FN_Create)
        self.FN_GetGroup()
        self.FN_GetKey()


    def FN_GetGroup(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT GROUP_NAME , GROUP_ID FROM POS_FN_GROUP")
            records = mycursor.fetchall()
            print(records)
            for row, val in records:
                self.Qcombo_group.addItem(row, val)
            mycursor.close()
        except:
            print(sys.exc_info())

    def FN_GetKey(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT KEY_CODE , KEY_ID FROM POS_FN_KEY")
            records = mycursor.fetchall()
            print(records)
            for row, val in records:
                self.Qcombo_key.addItem(str(row), val)
            mycursor.close()

        except:
            print(sys.exc_info())

    def FN_Create(self):
        self.conn = db1.connect()
        self.conn.autocommit = False
        mycursor = self.conn.cursor()
        self.conn.start_transaction()
        indx = self.Qcombo_group.currentData()
        sql_select_Query = "select * from POS_FN_GROUP_KEY where GROUP_ID = %s "
        x = (indx,)
        mycursor.execute(sql_select_Query, x)
        record = mycursor.fetchone()
        if mycursor.rowcount > 0:
            QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")

        else:
                try:
                    sql0 = "  LOCK TABLES Hyper1_Retail.POS_FN_GROUP_KEY WRITE  "
                    mycursor.execute(sql0)
                    sql = "INSERT INTO POS_FN_GROUP_KEY (GROUP_ID,KEY_ID,STATUS)" \
                          " VALUES (%s, %s, %s) "
                    val = (
                        self.Qcombo_group.currentData(), self.Qcombo_key.currentData(),
                        self.CMB_Status.currentIndex())
                    mycursor.execute(sql, val)
                    sql00 = "  UNLOCK   tables    "
                    mycursor.execute(sql00)
                    db1.connectionCommit(self.conn)
                    mycursor.close()
                    QtWidgets.QMessageBox.warning(self, "Done", "تم الانشاء")
                except:
                    print(sys.exc_info())
                    self.conn.rollback()
                finally:
                    if self.conn.is_connected():
                        mycursor.close()
                        self.conn.close()
                        print("connection is closed")
