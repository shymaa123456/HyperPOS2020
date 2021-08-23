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


class CL_WorkingDay(QtWidgets.QDialog):
    def __init__(self):
        super(CL_WorkingDay, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/PosWorkingDay.ui'
        loadUi(filename, self)
        self.setWindowTitle('Function Group')
        self.CMB_Status.addItems(["Inactive","Active"])
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        self.pushButton.clicked.connect(self.FN_Create)
        self.FN_GET_Company()
        self.FN_GET_Branch()

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



    def FN_Create(self):
        self.conn = db1.connect()
        self.conn.autocommit = False
        mycursor = self.conn.cursor()
        self.conn.start_transaction()


        try:
                    sql0 = "  LOCK TABLES Hyper1_Retail.POS_WORKING_DAY WRITE  "
                    mycursor.execute(sql0)
                    sql = "INSERT INTO POS_WORKING_DAY (COMPANY_ID,BRANCH_NO,WORKING_DATE,START_DATE,START_BY," \
                          "END_DATE,END_BY,DAY_STATUS)" \
                          " VALUES (%s, %s, %s,%s, %s, %s, %s, %s) "
                    val = (
                        self.Qcombo_company.currentData(),self.Qcombo_branch.currentData(),
                        self.Qdate_work.dateTime().toString('yyyy-MM-dd'),
                        self.Qdate_from.dateTime().toString('yyyy-MM-dd'),
                        CL_userModule.user_name,
                        self.Qdate_to.dateTime().toString('yyyy-MM-dd'),
                        CL_userModule.user_name,
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
