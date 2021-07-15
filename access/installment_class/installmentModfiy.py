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

        # Get installment type
        self.FN_GET_installment_types_period()

        #drob down list with multiselection for company
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(570,120,179,20)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Company()

        # TODO Click listner for changing list of company
        self.Qcombo_company.model().dataChanged.connect(self.FN_GET_Branch)

        #drob down list with multiselection for bracnch
        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(570,160,179,20)
        self.Qcombo_branch.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Branch()

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
        self.FN_GET_customerGroupe()

        #Multi selection for department
        self.Qcombo_department = CheckableComboBox(self)
        self.Qcombo_department.setGeometry(570, 250, 171, 22)
        self.Qcombo_department.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_department.setEnabled(False)
        self.Qcombo_department.setStyleSheet("background-color: rgb(198, 207, 199)")

        # TODO Click listner for changing list of department
        self.Qcombo_department.model().dataChanged.connect(self.FN_WhenChecksection)

        # get Department list if check box
        self.checkBox_department.stateChanged.connect(self.FN_WhenCheckDepartment)
        # self.FN_WhenCheckDepartment()

        # Multi selection for sections
        self.Qcombo_section = CheckableComboBox(self)
        self.Qcombo_section.setGeometry(570, 275, 171, 22)
        self.Qcombo_section.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_section.setEnabled(False)
        self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")
        # get sections list if check box
        self.checkBox_section.stateChanged.connect(self.FN_WhenChecksection)
        # self.FN_GET_sections()

        # TODO Click listner for changing list of department
        self.Qcombo_section.model().dataChanged.connect(self.FN_WhenCheckBMC_Level)

        # Multi selection for BMCLevel
        self.Qcombo_BMCLevel = CheckableComboBox(self)
        self.Qcombo_BMCLevel.setGeometry(570, 303, 171, 22)
        self.Qcombo_BMCLevel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_BMCLevel.setEnabled(False)
        self.Qcombo_BMCLevel.setStyleSheet("background-color: rgb(198, 207, 199)")

        # get BMC LEVEL4 list if check box
        self.checkBox_BMCLevel.stateChanged.connect(self.FN_WhenCheckBMC_Level)
        # self.FN_GET_BMC_Level()

        # get Banks list if readio button clicked
        self.RBTN_bank.clicked.connect(self.FN_InstallMent_Checked)

        # get Vendor list if readio button clicked
        self.RBTN_vendor.clicked.connect(self.FN_InstallMent_Checked)

        # if readio button clicked hyperone
        self.RBTN_hyperone.clicked.connect(self.FN_InstallMent_Checked)

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



    #TODO Get basic data
    # get installments period list
    def FN_GET_installment_types_period(self):
        self.Qcombo_installmentType.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT InstT_Installment_Period ,INSTT_TYPE_ID FROM INSTALLMENT_TYPE")
        records = mycursor.fetchall()
        mycursor.close()
        for row, val in records:
            self.Qcombo_installmentType.addItem(row, val)

        self.Qcombo_installmentType.setCurrentIndex(-1)


    #get companys list
    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    #get branches list
    def FN_GET_Branch(self):
         self.Qcombo_branch.clear()
         i=0
         try:
            # Todo: method for fills the Branch combobox
            self.conn = db1.connect()
            mycursor = self.conn.cursor()

            val3 = ""
            for a in range(len(self.Qcombo_company.currentData())):
                if a < len(self.Qcombo_company.currentData()) - 1:
                    val3 = val3 + "'" + self.Qcombo_company.currentData()[a] + "',"
                else:
                    val3 = val3 + "'" + self.Qcombo_company.currentData()[a] + "'"

            print("companies", val3)

            sqlite3="SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH WHERE COMPANY_ID in (" + val3 + ")"

            print("Branches_sqlite3", sqlite3)

            mycursor.execute(sqlite3)

            records = mycursor.fetchall()
            for row, val in records:
                for bra in CL_userModule.branch :
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1
            mycursor.close()
            self.Qcombo_branch.setCurrentIndex(-1)
         except:
             print(sys.exc_info())

    #get customer Groupe list
    def FN_GET_customerGroupe(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT CG_DESC,CG_GROUP_ID FROM CUSTOMER_GROUP")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_customerGroupe.addItem(row, val)
        mycursor.close()

    #after check department check box
    def FN_WhenCheckDepartment(self):
        if self.checkBox_department.isChecked():
            self.FN_GET_Department()
            self.Qcombo_department.setEnabled(True)
            self.checkBox_section.setEnabled(True)
            self.Qtable_acceptedItems.setEnabled(False)
            self.FN_ClearAcepptedQTableData()
            self.Qbtn_loadItems.setEnabled(False)
            self.Qbtn_deleteItem.setEnabled(False)
            self.Qcombo_department.setCurrentIndex(-1)

        else:
            self.Qcombo_department.unCheckedList()
            self.Qcombo_department.setEnabled(False)
            self.checkBox_section.setEnabled(False)
            self.checkBox_section.setChecked(False)
            self.checkBox_BMCLevel.setChecked(False)
            self.Qtable_acceptedItems.setEnabled(True)
            self.Qbtn_loadItems.setEnabled(True)
            self.Qbtn_deleteItem.setEnabled(True)
            self.Qcombo_department.setCurrentIndex(-1)


    #get Department list
    def FN_GET_Department(self):
        i = 0
        try:
        # Todo: method for fills the section combobox
            """
            self.Qcombo_department.clear()
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT DEPARTMENT_DESC,DEPARTMENT_ID FROM DEPARTMENT")
            records = mycursor.fetchall()

            for row, val in records:
                for sec in CL_userModule.section :
                    if val in sec:
                        self.Qcombo_department.addItem(row, val)
                    i += 1
            mycursor.close()
            """
            print(CL_userModule.section)

            for row,val,row1,val1 in CL_userModule.section:
                    self.Qcombo_department.addItem( val1 , row1)
        except:
            print(sys.exc_info())

    # after check section check box
    def FN_WhenChecksection(self):
        if self.checkBox_section.isChecked():
            self.FN_GET_sections()
            self.checkBox_BMCLevel.setEnabled(True)
            self.Qcombo_section.setEnabled(True)
            self.Qcombo_section.setCurrentIndex(-1)

        else:
            self.Qcombo_section.unCheckedList()
            self.checkBox_BMCLevel.setChecked(False)
            self.checkBox_BMCLevel.setEnabled(False)
            self.Qcombo_section.setEnabled(False)
            self.Qcombo_section.setCurrentIndex(-1)
            #self.Qcombo_section.unChecked()

    #get sections list
    def FN_GET_sections(self):
        self.Qcombo_section.clear()
        i = 0
        try:
            conn = db1.connect()
            mycursor = conn.cursor()
            print("currentData",self.Qcombo_department.currentData())
            val3=""
            for a in range(len(self.Qcombo_department.currentData())):
                if a< len(self.Qcombo_department.currentData())-1 :
                    val3 =val3+ "'"+self.Qcombo_department.currentData()[a] + "',"
                else:
                    val3 =val3+ "'"+self.Qcombo_department.currentData()[a] + "'"

            print("deparments",val3)

            mycursor.execute("SELECT SECTION_DESC,SECTION_ID FROM SECTION where DEPARTMENT_ID in ("+val3+")")
            #print("Query"+"SELECT SECTION_DESC,SECTION_ID FROM SECTION where DEPARTMENT_ID in ("+val3+")")
            records = mycursor.fetchall()
            mycursor.close()
            for row, val in records:
                self.Qcombo_section.addItem(row, val)
                i += 1
        except:
            print(sys.exc_info())
        # after check department check box

    # after check BMC Level check box
    def FN_WhenCheckBMC_Level(self):
        if self.checkBox_BMCLevel.isChecked():
            self.FN_GET_BMC_Level()
            self.Qcombo_BMCLevel.setEnabled(True)
            self.Qcombo_BMCLevel.setCurrentIndex(-1)
            #self.FN_
        else:
            self.Qcombo_BMCLevel.unCheckedList()
            self.checkBox_BMCLevel.setChecked(False)
            self.Qcombo_BMCLevel.setEnabled(False)
            self.Qcombo_BMCLevel.setCurrentIndex(-1)

    #get BMC LEVEL4 list
    def FN_GET_BMC_Level(self):
        self.Qcombo_BMCLevel.clear()
        i = 0
        try:
            conn = db1.connect()
            mycursor = conn.cursor()

            val3=""
            for a in range(len(self.Qcombo_section.currentData())):
                if a< len(self.Qcombo_section.currentData())-1 :
                    val3 =val3+ "'"+self.Qcombo_section.currentData()[a] + "',"
                else:
                    val3 =val3+ "'"+self.Qcombo_section.currentData()[a] + "'"

            print("sections",val3)
            mycursor.execute("SELECT BMC_LEVEL4_DESC,BMC_LEVEL4 FROM BMC_LEVEL4 where SECTION_ID in ("+val3+")")
            records = mycursor.fetchall()
            mycursor.close()
            for row, val in records:
                self.Qcombo_BMCLevel.addItem(row, val)
                i += 1
        except:
            print(sys.exc_info())

    #TODO when any radio button checked(bank ,vendor ,hyperone)
    def FN_InstallMent_Checked(self):
        if self.RBTN_bank.isChecked():
            self.FN_GET_Banks()
            self.Qcombo_bank.setEnabled(True)
            self.Qcombo_vendor.setEnabled(False)
            self.Qcombo_vendor.clear()
            self.QTEdit_sponsorReason.setEnabled(False)

        elif self.RBTN_vendor.isChecked():
            self.Qcombo_bank.setEnabled(False)
            self.Qcombo_bank.clear()
            self.FN_GET_Vendor()
            self.Qcombo_vendor.setEnabled(True)
            self.QTEdit_sponsorReason.setEnabled(True)

        elif self.RBTN_hyperone.isChecked():
            self.Qcombo_bank.setEnabled(False)
            self.Qcombo_bank.clear()
            self.Qcombo_vendor.setEnabled(False)
            self.Qcombo_vendor.clear()
            self.QTEdit_sponsorReason.setEnabled(False)

    # after check Bank check box
    def FN_WhenCheckBank(self):
        if self.RBTN_bank.isChecked():
            self.FN_GET_Banks()
            self.Qcombo_bank.setEnabled(True)

        else:
            self.Qcombo_bank.setEnabled(False)
            self.Qcombo_bank.clear()

    #get Banks list
    def FN_GET_Banks(self):
        self.Qcombo_bank.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT Bank_Desc,Bank_ID FROM BANK")
        records = mycursor.fetchall()
        mycursor.close()
        for row, val in records:
            self.Qcombo_bank.addItem(row, val)

    # after check Vendor check box
    def FN_WhenCheckVendor(self):
        if self.RBTN_vendor.isChecked():
            self.FN_GET_Vendor()
            self.Qcombo_vendor.setEnabled(True)
            self.QTEdit_sponsorReason.setEnabled(True)
        elif not self.RBTN_vendor.isChecked:
            self.Qcombo_vendor.setEnabled(False)
            self.Qcombo_vendor.clear()
            self.QTEdit_sponsorReason.setEnabled(False)

    #get Vendor list
    def FN_GET_Vendor(self):
        self.Qcombo_vendor.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT SPONSER_NAME,SPONSER_ID FROM SPONSER")
        records = mycursor.fetchall()
        mycursor.close()
        for row, val in records:
            self.Qcombo_vendor.addItem(row, val)

    #Insert in Qtable
    def FN_InsertInQtable(self,QTableWidgit):
        def FN_InsertInQtable_internal():
            if self.fileName !='':
                self.LE_fileName.setText(self.fileName)
                wb = xlrd.open_workbook( self.fileName )
                sheet = wb.sheet_by_index( 0 )
                conn = db1.connect()
                mycursor = conn.cursor()
                errorMsg =''
                createdCust =0
                nonCreatedCust=0
                #print (sheet.nrows)
                error_message = ''
                for i in range( sheet.nrows ):
                    error = 0
                    try:
                        self.barcode = sheet.cell_value( i, 0 )
                        print("rowNo",i,"barcode",self.barcode)
                        error_message = error_message + " \n barcode " + self.barcode
                        self.description = sheet.cell_value( i, 1 )
                        print("rowNo",i,"description",self.description)

                        if self.barcode == '' or self.description == '':
                            error = 1
                            error_message = error_message + " barcode has an empty fields"
                            print("error 1")

                        #Validate if barcode inserted in Qtable before insert it
                        elif self.FN_ValidateIfBarcodeInsertedInQtable(sheet.cell_value(i,0),QTableWidgit) ==1:
                            QtWidgets.QMessageBox.warning(self, "Error", "Barcode Repeated")

                        else:
                            #for row_number, row_data in enumerate(records):
                            QTableWidgit.insertRow(i)

                            QTableWidgit.setItem(i, 0, QTableWidgetItem(str(sheet.cell_value( i, 0 ))))
                            QTableWidgit.setItem(i, 1, QTableWidgetItem(str(sheet.cell_value( i, 1 ))))

                            #to make rows of table not editable
                            QTableWidgit.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

                    except Exception as err:
                         print(err)
                mycursor.close()
                self.msgBox = QMessageBox()

                # Set the various texts
                #self.msgBox.setWindowTitle( "Information" )
                #self.msgBox.setStandardButtons( QMessageBox.Ok)
                #self.msgBox.setText(error_message)
                #self.msgBox.show()
                self.close()
            #Extracting number of rows
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Choose a file")

        return FN_InsertInQtable_internal

    #Get data for installment program
    def FN_SearchForInstallmentProgram(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()

        # insert to INSTALLMENT_PROGRAM
        sql2 = "SELECT INSTR_RULEID ,INST_DESC,INST_STATUS FROM INSTALLMENT_PROGRAM WHERE INST_PROGRAM_ID='"+self.QL_installmentNo.text()+"'"

        mycursor.execute(sql2)
        records = mycursor.fetchall()
        if len(records) >0 :

            for INSTR_RULEID , INST_DESC, INST_STATUS in records:
                print("INST_DESC", INST_DESC)
                print("INST_STATUS", INST_STATUS)
                print("INSTR_RULEID", INSTR_RULEID)

                self.QTEdit_descInstallment.setText (INST_DESC)
                """
                                if INST_STATUS == str(0):
                                    self.QRBTN_inactive.setChecked(True)
                                elif INST_STATUS ==str(1):
                                    self.QRBTN_active.setChecked(True)
                """

                sql3 = "SELECT INSTT_TYPE_ID,INSTR_DESC, INSTR_INTEREST_RATE, INSTR_SPONSOR_RATE , INSTR_HYPER_RATE,  INSTR_CUSTOMER_RATE FROM INSTALLMENT_RULE WHERE INSTR_RULEID='" + str(INSTR_RULEID) + "'"
                mycursor.execute(sql3)
                records2 = mycursor.fetchall()
                for INSTT_TYPE_ID,INSTR_DESC, INSTR_INTEREST_RATE, INSTR_SPONSOR_RATE , INSTR_HYPER_RATE,  INSTR_CUSTOMER_RATE in records2:
                    print("Index_installmentType", INSTT_TYPE_ID)
                    self.Qcombo_installmentType.setCurrentIndex(INSTT_TYPE_ID-1)  # installment type id
                    self.QDubleSpiner_customerRate.setValue(INSTR_CUSTOMER_RATE)
                    self.QDubleSpiner_vendorRate.setValue (INSTR_SPONSOR_RATE)
                    print("INSTR_SPONSOR_RATE",INSTR_SPONSOR_RATE)
                    self.QDubleSpiner_hperoneRate.setValue(INSTR_HYPER_RATE)
                    self.QDubleSpiner_interestRate.setValue(self.QDubleSpiner_customerRate.value()+self.QDubleSpiner_vendorRate.value()+self.QDubleSpiner_hperoneRate.value())
                    print(sql3)

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