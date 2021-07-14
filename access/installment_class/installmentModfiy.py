from pathlib import Path

import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import sys

from pathlib import Path
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate ,QTime
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem

from access.Checkable import CheckableComboBox

#from access.promotion_class.Promotion_Add import CheckableComboBox

from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime
from Validation.Validation import CL_validation

import xlrd
from datetime import datetime
import xlwt.Workbook

import webbrowser

class CL_installmentModify(QtWidgets.QDialog):
    dirname = ''
    parent = ''
    def __init__(self,parentInit):
        super(CL_installmentModify, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/installment_ui'
        self.conn = db1.connect()
        self.parent = parentInit


    def FN_LOAD_Modify(self):
        filename = self.dirname + '/Installment_modify.ui'
        loadUi(filename, self)


        #drob down list with multiselection for company
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(570,120,179,20)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")


        #drob down list with multiselection for bracnch
        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(570,160,179,20)
        self.Qcombo_branch.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")

        #validation for not pick date before today
        datefrom = str(datetime.today().strftime('%Y-%m-%d'))
        xfrom = datefrom.split("-")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        self.Qdate_from.setMinimumDate(d)
        self.Qdate_to.setMinimumDate(d)

        # Get customer Groupe
        self.Qcombo_customerGroupe = CheckableComboBox(self)
        self.Qcombo_customerGroupe.setGeometry(570, 200, 179, 20)
        self.Qcombo_customerGroupe.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_customerGroupe.setEnabled(False)
        self.Qcombo_customerGroupe.setStyleSheet("background-color: rgb(198, 207, 199)")

        #Multi selection for department
        self.Qcombo_department = CheckableComboBox(self)
        self.Qcombo_department.setGeometry(570, 250, 171, 22)
        self.Qcombo_department.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_department.setEnabled(False)
        self.Qcombo_department.setStyleSheet("background-color: rgb(198, 207, 199)")

        # Multi selection for sections
        self.Qcombo_section = CheckableComboBox(self)
        self.Qcombo_section.setGeometry(570, 275, 171, 22)
        self.Qcombo_section.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_section.setEnabled(False)
        self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")


        # Multi selection for BMCLevel
        self.Qcombo_BMCLevel = CheckableComboBox(self)
        self.Qcombo_BMCLevel.setGeometry(570, 300, 171, 22)
        self.Qcombo_BMCLevel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_BMCLevel.setEnabled(False)
        self.Qcombo_BMCLevel.setStyleSheet("background-color: rgb(198, 207, 199)")

        #set minimum time
        # this_moment PyQt5.QtCore.QTime(10, 43, 1, 872)
        this_moment = QtCore.QTime.currentTime()
        #this_moment = this_moment.toString('hh:mm ap')
        print("this_moment",this_moment)
        self.Qtime_to.setTime(this_moment)
        self.Qtime_from.setTime(this_moment)
        self.Qtime_to.setMinimumTime(this_moment)

        # Search for installment program
        self.Qbtn_searchInstallment.clicked.connect(self.FN_SearchForInstallmentProgram)

        #save installment program
        self.Qbtn_modifyInstallment.clicked.connect(self.FN_UpdateInstallemtProgram)


    #Who active if installment is active


    #Get data for installment program
    def FN_SearchForInstallmentProgram(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()

        # insert to INSTALLMENT_PROGRAM
        sql2 = "SELECT INST_DESC,INST_STATUS FROM INSTALLMENT_PROGRAM WHERE INST_PROGRAM_ID='"+self.QL_installmentNo.text()+"'"

        mycursor.execute(sql2)
        records = mycursor.fetchall()
        if len(records) >0 :

            for INST_DESC, INST_STATUS in records:
                print("INST_DESC", INST_DESC)
                print("INST_STATUS", INST_STATUS)
                self.LE_installmentTypeDesc.setText (INST_DESC)

                if INST_STATUS == str(0):
                    self.QRBTN_inactive.setChecked(True)
                elif INST_STATUS ==str(1):
                    self.QRBTN_active.setChecked(True)

        else:
            print("Program doesn't exist")
            QtWidgets.QMessageBox.information(self, "INFO", " Program doesn't exist")


        mycursor.close()


    #Validate installment program
    def FN_ValidateInstallemt(self):
        error=0
        if len(self.LE_installmentTypeDesc.text()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى البحث اولا")
            error = 0

        elif not self.QRBTN_active.isChecked() and not self.QRBTN_inactive.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى البحث اولا")
            error = 0
        else:
            error = 1

        return error


    # save Installment program
    def FN_UpdateInstallemtProgram(self):
        error = 0
        Validation_For_installmentProgramm = 0

        error = self.FN_ValidateInstallemt()
        print(error)
        if error != 0:

            try:
                self.conn = db1.connect()
                self.conn.autocommit = False
                mycursor = self.conn.cursor()
                self.conn.start_transaction()

                # # lock table for new record:
                sql0 = "  LOCK  TABLES   Hyper1_Retail.INSTALLMENT_PROGRAM   WRITE "
                mycursor.execute(sql0)

                ModifingDateTime = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

                # insert to INSTALLMENT_PROGRAM
                if self.QRBTN_active.isChecked():
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=1 , INST_CHANGED_ON = '" + ModifingDateTime + "' , INST_CHANGED_BY = " + CL_userModule.user_name + " , INST_ACTIVATED_BY = " + CL_userModule.user_name + " where INST_PROGRAM_ID='" + self.QL_installmentNo.text() + "'"
                elif self.QRBTN_inactive.isChecked():
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=0 , INST_CHANGED_ON = '" + ModifingDateTime + "' , INST_CHANGED_BY = " + CL_userModule.user_name + " , INST_DEACTIVATED_BY = " + CL_userModule.user_name + " where INST_PROGRAM_ID='" + self.QL_installmentNo.text() + "'"

                print("sql2", sql2)
                mycursor.execute(sql2)

                # # unlock table :
                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                self.conn.commit()

            except mysql.connector.Error as error:
                print("Failed to update record to database rollback: {}".format(error))
                # reverting changes because of exception
                self.conn.rollback()
            finally:
                # closing database connection.
                if self.conn.is_connected():
                    mycursor.close()
                    self.conn.close()
                    print("connection is closed")