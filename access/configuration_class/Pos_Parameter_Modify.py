import sys
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from access.Checkable import CheckableComboBox
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import mysql


class CL_Pos_Parameters_Modify(QtWidgets.QDialog):
    branch=[]
    parameter=[]
    parameterlist=[]
    new_parameter_list=[]
    def __init__(self):
        super(CL_Pos_Parameters_Modify, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Pos_Parameter_Modify.ui'
        loadUi(filename, self)
        self.setWindowTitle('Pos_Parameters_Modify')
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
        self.Qcombo_pos.activated[str].connect(self.FN_check_branch)
        self.CMB_CouponStatus.addItems(["Inactive", "Active"])
        self.pushButton.clicked.connect(self.FN_Edit)

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
                self.parameter.append(val)

            mycursor.close()
        except:
            print(sys.exc_info())

    def FN_unCheckedALL(self):
        i=0
        for row in self.parameter:
            self.Qcombo_parameter.unChecked(i)
            i+=1

    def FN_check_branch(self):
        try:
            self.FN_unCheckedALL()
            mycursor = self.conn.cursor()
            sql_select_branch = "SELECT PARAMETER_ID FROM POS_PARAMETER_POS where POS_NO='"+self.Qcombo_pos.currentData()+"'"
            mycursor.execute(sql_select_branch)
            record = mycursor.fetchall()
            print(self.parameter)
            i = 0
            for row in record:
                for row1 in self.parameter:
                    if row[0] == int(row1[0]):
                        self.Qcombo_parameter.setChecked(i)
                i = i + 1
            mycursor.close()
            if len(self.Qcombo_parameter.currentData()) > 0:
                for i in self.Qcombo_parameter.currentData():
                    self.parameterlist.append(i)
        except:
            print(sys.exc_info())

    def FN_Edit(self):
        self.new_parameter_list.clear()
        try:
            mycursor = self.conn.cursor()
            if len(self.Qcombo_parameter.currentData()) > 0:
                for i in self.Qcombo_parameter.currentData():
                    self.new_parameter_list.append(i)
            if len(self.parameterlist) > len(self.new_parameter_list):
                for row in self.parameterlist:
                    print(row)
                    if row in self.new_parameter_list:
                        print("found")
                    else:
                        print("not found")
                        mycursor = self.conn.cursor()
                        sql5 = "delete from POS_PARAMETER_POS where PARAMETER_ID ='" + row + "' and BRANCH_NO ='" + self.Qcombo_branch.currentData() + "' and POS_NO='"+self.Qcombo_pos.currentData()+"'"
                        print(sql5)
                        mycursor.execute(sql5)
            else:
                for row in self.new_parameter_list:
                    print(row)
                    if row in self.parameterlist:
                        print("found")
                    else:
                            mycursor = self.conn.cursor()
                            sql6 = "INSERT INTO POS_PARAMETER_POS (COMPANY_ID,PARAMETER_ID,POS_NO,BRANCH_NO,STATUS) VALUES (%s,%s,%s,%s,%s)"
                            val6 = (
                                str(self.Qcombo_company.currentData()), row,
                                self.Qcombo_pos.currentData(), self.Qcombo_branch.currentData(),
                                self.CMB_CouponStatus.currentIndex())
                            mycursor.execute(sql6, val6)


            db1.connectionCommit(self.conn)
            mycursor.close()
            QtWidgets.QMessageBox.warning(self, "Done", "Done")
            self.parameterlist.clear()
            self.FN_check_branch()
            print(self.new_parameter_list)
            print(self.parameterlist)

        except:
            print(sys.exc_info())
