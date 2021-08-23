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


class CL_FNGroupPos(QtWidgets.QDialog):
    def __init__(self):
        super(CL_FNGroupPos, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Pos_Group_Pos.ui'
        loadUi(filename, self)
        self.setWindowTitle('Assign Group Pos')
        self.CMB_Status.addItems(["Inactive","Active"])
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        self.pushButton.clicked.connect(self.FN_Create)
        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.Qcombo_branch.activated[str].connect(self.FN_GET_POS)
        self.FN_GetGroup()

    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    def FN_GET_Branch(self):
        i = 0
        try:
            for row, val in CL_userModule.branch:
                self.Qcombo_branch.addItem(val, row)
                i += 1
        except:
            print(sys.exc_info())

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

    def FN_GET_POS(self):
        try:
            self.Qcombo_pos.clear()
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            print("SELECT POS_NO , POS_NO FROM POS where BRANCH_NO ='"+str(self.Qcombo_branch.currentData())+"'")
            mycursor.execute("SELECT POS_NO , POS_NO FROM POS where BRANCH_NO ='"+str(self.Qcombo_branch.currentData())+"'")
            records = mycursor.fetchall()
            for row, val in records:
                self.Qcombo_pos.addItem(row, val)
            mycursor.close()

        except:
            print(sys.exc_info())

    def FN_Create(self):
        try:
            self.conn = db1.connect()
            self.conn.autocommit = False
            mycursor = self.conn.cursor()
            self.conn.start_transaction()
            sql_select_Query = "select * from POS_FN_GROUP_POS where COMPANY_ID=%s and BRANCH_NO=%s and POS_NO=%s and GROUP_ID = %s  "
            x = (self.Qcombo_company.currentData(),
                 self.Qcombo_branch.currentData(),
                 self.Qcombo_pos.currentData(),
                 self.Qcombo_group.currentData())
            mycursor.execute(sql_select_Query, x)
            record = mycursor.fetchone()
            if mycursor.rowcount > 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "المكنه موجود بالفعل")

            else:
                    try:
                        sql0 = "  LOCK TABLES Hyper1_Retail.POS_FN_GROUP_POS WRITE  "
                        mycursor.execute(sql0)
                        sql = "INSERT INTO POS_FN_GROUP_POS (COMPANY_ID,BRANCH_NO,POS_NO,GROUP_ID,STATUS)" \
                              " VALUES (%s, %s, %s, %s, %s) "
                        val = (
                            self.Qcombo_company.currentData(),self.Qcombo_branch.currentData(),
                            self.Qcombo_pos.currentData(),
                            self.Qcombo_group.currentData(),
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
        except:
            print(sys.exc_info())
