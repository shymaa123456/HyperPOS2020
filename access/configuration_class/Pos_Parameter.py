import sys
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from access.Checkable import CheckableComboBox
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import mysql


class CL_Pos_Parameters(QtWidgets.QDialog):
    branch=[]
    def __init__(self):
        super(CL_Pos_Parameters, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Pos_Parameter.ui'
        loadUi(filename, self)
        self.setWindowTitle('Pos_Parameters')
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())

        self.Qcombo_parameter = CheckableComboBox(self)
        self.Qcombo_parameter.setGeometry(50, 160, 271, 25)
        self.Qcombo_parameter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_parameter.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.FN_GET_Parameter()
        self.Qcombo_branch.activated[str].connect(self.FN_GET_POS)
        self.CMB_CouponStatus.addItems(["Inactive", "Active"])
        self.pushButton.clicked.connect(self.FN_create)

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
                self.branch.append(row)
                i += 1
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

    def FN_GET_Parameter(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT PARAMETER_DESC,PARAMETER_ID   FROM SYS_CONFIG_PARAMETERS")
            records = mycursor.fetchall()
            for row, val in records:
                self.Qcombo_parameter.addItem(row, val)
            mycursor.close()
        except:
            print(sys.exc_info())

    def FN_create(self):
        self.conn = db1.connect()
        self.conn.autocommit = False
        mycursor = self.conn.cursor()
        self.conn.start_transaction()
        if len(self.Qcombo_company.currentData()) == 0 or len(self.Qcombo_branch.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
        else:
            try:
                sql0 = "  LOCK TABLES Hyper1_Retail.POS_PARAMETER_POS WRITE  "
                mycursor.execute(sql0)
                for row in range(len(self.Qcombo_parameter.currentData())):
                    sql = "INSERT INTO POS_PARAMETER_POS (COMPANY_ID,BRANCH_NO,POS_NO,PARAMETER_ID,STATUS)" \
                          " VALUES (%s, %s, %s, %s, %s) "
                    val = (self.Qcombo_company.currentData(), self.Qcombo_branch.currentData(),self.Qcombo_pos.currentData(),self.Qcombo_parameter.currentData()[row],self.CMB_CouponStatus.currentIndex())
                    mycursor.execute(sql, val)
                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                db1.connectionCommit(self.conn)
                mycursor.close()
                QtWidgets.QMessageBox.warning(self, "Done", "تم الانشاء")
            except :
                print(sys.exc_info())
                self.conn.rollback()
            finally:
                if self.conn.is_connected():
                    mycursor.close()
                    self.conn.close()
                    print("connection is closed")