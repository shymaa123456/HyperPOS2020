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
from PyQt5.QtCore import QDate, QTime, QRegExp
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
    InstallmentNo=""
    oldstatusDateTo=""
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

        #hidden label for status of installment program
        self.QL_hint_youcanonlychange_period.setVisible(False)

        # Get installment type
        self.FN_GET_installment_types_period()

        #drob down list with multiselection for company
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(570,120,179,20)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.Qcombo_company.setEnabled(False)
        self.FN_GET_Company()

        # TODO Click listner for changing list of company
        #self.Qcombo_company.model().dataChanged.connect(self.FN_GET_Branch)

        #drob down list with multiselection for bracnch
        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(570,160,179,20)
        self.Qcombo_branch.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.Qcombo_branch.setEnabled(False)
        #self.FN_GET_Branch()

        #validation for not pick date before today
        datefrom = str(datetime.today().strftime('%Y-%m-%d'))
        xfrom = datefrom.split("-")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
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
            mycursorb = self.conn.cursor()

            val3 = ""
            for a in range(len(self.Qcombo_company.currentData())):
                if a < len(self.Qcombo_company.currentData()) - 1:
                    val3 = val3 + "'" + self.Qcombo_company.currentData()[a] + "',"
                else:
                    val3 = val3 + "'" + self.Qcombo_company.currentData()[a] + "'"

            print("companies", val3)

            sqlite3="SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH WHERE COMPANY_ID in (" + val3 + ")"

            print("Branches_sqlite3", sqlite3)

            mycursorb.execute(sqlite3)

            records = mycursorb.fetchall()
            for row, val in records:
                for bra in CL_userModule.branch :
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1
            mycursorb.close()
            self.Qcombo_branch.setCurrentIndex(-1)
         except:
             print(sys.exc_info())

    # get branches list
    def FN_GET_Branch_Wiithoutselectcompany(self,mycursorb,companyID):
        #self.Qcombo_branch.clear()
        i = 0
        try:
            # Todo: method for fills the Branch combobox
            sqlite3 = "SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH WHERE COMPANY_ID in (" + companyID + ")"

            print("Branches_sqlite3_without", sqlite3)

            mycursorb.execute(sqlite3)

            records = mycursorb.fetchall()
            for row, val in records:
                for bra in CL_userModule.branch:
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1

            self.Qcombo_branch.setCurrentIndex(-1)
        except:
            print(sys.exc_info())

    #get customer Groupe list
    def FN_GET_customerGroupe(self):
        self.conn = db1.connect()
        mycursorg = self.conn.cursor()
        mycursorg.execute("SELECT CG_DESC,CG_GROUP_ID FROM CUSTOMER_GROUP")
        records = mycursorg.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_customerGroupe.addItem(row, val)
        mycursorg.close()

    #after check department check box
    def FN_WhenCheckDepartment(self):
        if self.checkBox_department.isChecked():
            self.FN_GET_Department()
            #self.Qcombo_department.setEnabled(True)
            #self.checkBox_section.setEnabled(True)
            self.Qtable_acceptedItems.setEnabled(False)
            self.FN_ClearAcepptedQTableData()
            #self.Qbtn_loadItems.setEnabled(False)
            #self.Qbtn_deleteItem.setEnabled(False)
            self.Qcombo_department.setCurrentIndex(-1)

        else:
            self.Qcombo_department.unCheckedList()
            #self.Qcombo_department.setEnabled(False)
            #self.checkBox_section.setEnabled(False)
            self.checkBox_section.setChecked(False)
            self.checkBox_BMCLevel.setChecked(False)
            #self.Qtable_acceptedItems.setEnabled(True)
            #self.Qbtn_loadItems.setEnabled(True)
            #self.Qbtn_deleteItem.setEnabled(True)
            self.Qcombo_department.setCurrentIndex(-1)


    #get Department list
    def FN_GET_Department(self):
        self.Qcombo_department.clear()
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
            #self.checkBox_BMCLevel.setEnabled(True)
            #self.Qcombo_section.setEnabled(True)
            self.Qcombo_section.setCurrentIndex(-1)

        else:
            self.Qcombo_section.unCheckedList()
            #self.checkBox_BMCLevel.setChecked(False)
            #self.checkBox_BMCLevel.setEnabled(False)
            #self.Qcombo_section.setEnabled(False)
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
            #self.Qcombo_BMCLevel.setEnabled(True)
            self.Qcombo_BMCLevel.setCurrentIndex(-1)
            #self.FN_
        else:
            self.Qcombo_BMCLevel.unCheckedList()
            self.checkBox_BMCLevel.setChecked(False)
            #self.Qcombo_BMCLevel.setEnabled(False)
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
        print("FN_GetVwndor",len(records))
        mycursor.close()
        for row, val in records:
            self.Qcombo_vendor.addItem(row, val)

    #Insert in Qtable
    def FN_InsertInQtable(self,records , QTableWidgit):
        def FN_InsertInQtable_internal():

                i=0
                error_message = ''
                for POS_GTIN, POS_GTIN_DESC_A in records:
                    #for row_number, row_data in enumerate(records):
                    QTableWidgit.insertRow(i)
                    QTableWidgit.setItem(i, 0, QTableWidgetItem(POS_GTIN))
                    QTableWidgit.setItem(i, 1, QTableWidgetItem(POS_GTIN_DESC_A))

                    #to make rows of table not editable
                    QTableWidgit.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                    i=i+1

        return FN_InsertInQtable_internal

    #Get data for installment program
    def FN_SearchForInstallmentProgram(self):
        self.InstallmentNo=self.QL_installmentNo.text()

        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()

            # Select INSTALLMENT_PROGRAM
            sql1 = "SELECT INSTR_RULEID ,INST_DESC,INST_VALID_FROM ,INST_VALID_TO , INST_ADMIN_EXPENSES_PERC ,INST_ADMIN_EXPENSES_MAX , INST_ADMIN_EXPENSES_MIN  , INST_STATUS FROM INSTALLMENT_PROGRAM WHERE INST_PROGRAM_ID='"+self.InstallmentNo+"'"

            mycursor.execute(sql1)
            records = mycursor.fetchall()
            if len(records) >0 :

                for INSTR_RULEID , INST_DESC, INST_VALID_FROM , INST_VALID_TO ,INST_ADMIN_EXPENSES_PERC , INST_ADMIN_EXPENSES_MAX ,INST_ADMIN_EXPENSES_MIN ,INST_STATUS in records:
                    print("INST_DESC", INST_DESC)
                    print("INST_STATUS", INST_STATUS)
                    print("INSTR_RULEID", INSTR_RULEID)

                    if INST_STATUS == str(0):
                        self.QL_hint_youcanonlychange_period.setVisible(True)
                        self.QL_hint_youcanonlychange_period.setText("لم يتم تفعيل البرنامج من قبل مسموح بتعديل الفتره فقط")

                    elif INST_STATUS == str(1):
                        self.QL_hint_youcanonlychange_period.setVisible(True)
                        self.QL_hint_youcanonlychange_period.setText("تم تفعيل البرنامج من قبل مسموح بتعديل الفتره فقط")

                        self.LoadingDataofProgram(INST_VALID_FROM , INST_VALID_TO,INST_ADMIN_EXPENSES_PERC,INST_ADMIN_EXPENSES_MAX ,INST_ADMIN_EXPENSES_MIN,INST_DESC , mycursor,INSTR_RULEID)
                    else:
                        self.QL_hint_youcanonlychange_period.setVisible(False)
                        print("Program is not active")
                        QtWidgets.QMessageBox.information(self, "INFO", " Program is not active")

            else:
                self.QL_hint_youcanonlychange_period.setVisible(False)
                print("Program doesn't exist")
                QtWidgets.QMessageBox.information(self, "INFO", " Program doesn't exist")

            mycursor.close()
        except:
            print(sys.exc_info())

    #
    def LoadingDataofProgram(self,INST_VALID_FROM , INST_VALID_TO ,INST_ADMIN_EXPENSES_PERC,INST_ADMIN_EXPENSES_MAX ,INST_ADMIN_EXPENSES_MIN,INST_DESC , mycursor,INSTR_RULEID):
        self.QDSpinBox_adminExpendses.setValue(INST_ADMIN_EXPENSES_PERC)
        self.QDSpinBox_Max_adminExpendses.setValue(INST_ADMIN_EXPENSES_MAX)
        self.QDSpinBox_Min_adminExpendses.setValue(INST_ADMIN_EXPENSES_MIN)

        self.QTEdit_descInstallment.setText(INST_DESC)

        self.oldstatusDateTo=INST_VALID_TO

        #convert datatime as varchar to date and time
        #todo INST_VALID_TO
        dateto = INST_VALID_TO
        print("dateto",dateto)
        dto = dateto.split("-")
        dtotdd=dto[2].split(" ")                               #'15 13:36'
        print("dtotdd",dtotdd[0])
        print("dtotdd",dtotdd)
        dtotm=dtotdd[1].split(":")
        print("dtotm",dtotm[0])
        print("dtotm", dtotm[1])
        some_dateTo = QtCore.QDate(int(dto[0]), int(dto[1]), int(dtotdd[0]))
        print("some_dateTo",some_dateTo)
        self.Qdate_to.setDate(some_dateTo)
        some_timeTo = QtCore.QTime(int(dtotm[0]), int(dtotm[1]))
        self.Qtime_to.setTime(some_timeTo)
        #Todo INST_VALID_FROM
        dateto = INST_VALID_FROM
        print("dateto", dateto)
        dto = dateto.split("-")
        dtotdd = dto[2].split(" ")  # '15 13:36'
        print("dtotdd", dtotdd[0])
        print("dtotdd", dtotdd)
        dtotm = dtotdd[1].split(":")
        print("dtotm", dtotm[0])
        print("dtotm", dtotm[1])
        some_datefrom = QtCore.QDate(int(dto[0]), int(dto[1]), int(dtotdd[0]))
        print("some_dateTo", some_datefrom)
        self.Qdate_from.setDate(some_datefrom)
        some_timeTo = QtCore.QTime(int(dtotm[0]), int(dtotm[1]))
        self.Qtime_from.setTime(some_timeTo)

        # Get selected Data For company and branch
        self.FN_GetSlectedCompanyAndBranchForThisProgram(mycursor)

        # Get customer groupe
        self.FN_GetSlectedCustomerGroupeForThisProgram(mycursor)

        # Get customer Banck or vendor or hyperone
        self.FN_GetSlectedBankOrVendorOrHyperoneForThisProgram(mycursor, INSTR_RULEID)

        # Get installment Department and sections and BMC
        self.FN_GetSlectedDepartmentAndSectionsAndBMCForThisProgram(mycursor, INSTR_RULEID)

        # Get Data from installment Rule
        sql2 = "SELECT INSTT_TYPE_ID,INSTR_DESC, INSTR_INTEREST_RATE, INSTR_SPONSOR_RATE , INSTR_HYPER_RATE,  INSTR_CUSTOMER_RATE FROM INSTALLMENT_RULE WHERE INSTR_RULEID='" + str(
            INSTR_RULEID) + "'"
        mycursor.execute(sql2)
        records2 = mycursor.fetchall()
        for INSTT_TYPE_ID, INSTR_DESC, INSTR_INTEREST_RATE, INSTR_SPONSOR_RATE, INSTR_HYPER_RATE, INSTR_CUSTOMER_RATE in records2:
            print("Index_installmentType", INSTT_TYPE_ID)
            self.Qcombo_installmentType.setCurrentIndex(INSTT_TYPE_ID - 1)  # installment type id
            self.QDubleSpiner_customerRate.setValue(INSTR_CUSTOMER_RATE)
            self.QDubleSpiner_vendorRate.setValue(INSTR_SPONSOR_RATE)
            print("INSTR_SPONSOR_RATE", INSTR_SPONSOR_RATE)
            self.QDubleSpiner_hperoneRate.setValue(INSTR_HYPER_RATE)
            self.QDubleSpiner_interestRate.setValue(
                self.QDubleSpiner_customerRate.value() + self.QDubleSpiner_vendorRate.value() + self.QDubleSpiner_hperoneRate.value())
            print(sql2)

        # Get Data From INSTALLMENT_REJECTED_ITEM
        sql3 = "select a.POS_GTIN , a.POS_GTIN_DESC_A  from Hyper1_Retail.POS_ITEM a inner join  Hyper1_Retail.INSTALLMENT_REJECTED_ITEM r on a.POS_GTIN = r.POS_GTIN WHERE INSTR_RULEID='" + str(
            INSTR_RULEID) + "'"
        print(sql3)
        mycursor.execute(sql3)
        records3 = mycursor.fetchall()
        self.FN_InsertInQtable(records3, self.Qtable_rejectedItems)

        # Get Data From INSTALLMENT_ITEM
        sql4 = "select a.POS_GTIN , a.POS_GTIN_DESC_A  from Hyper1_Retail.POS_ITEM a inner join  Hyper1_Retail.INSTALLMENT_ITEM i on a.POS_GTIN = i.POS_GTIN WHERE INSTR_RULEID='" + str(
            INSTR_RULEID) + "'"
        print(sql4)
        mycursor.execute(sql4)
        records4 = mycursor.fetchall()
        self.FN_InsertInQtable(records4, self.Qtable_acceptedItems)

    # Get selected Data For company and branch
    def FN_GetSlectedCompanyAndBranchForThisProgram(self,mycursor):
        try:
            sql21 = "SELECT COMPANY_ID ,BRANCH_NO FROM Hyper1_Retail.INSTALLMENT_BRANCH  WHERE INST_PROGRAM_ID='" + self.InstallmentNo + "'"
            mycursor.execute(sql21)
            records21 = mycursor.fetchall()

            sql_select_Companies_branchs = "SELECT COMPANY_ID, BRANCH_NO FROM BRANCH"
            mycursor.execute(sql_select_Companies_branchs)
            record = mycursor.fetchall()
            i = 0
            for row in record:
                for row1 in records21:
                    if row[0] == row1[0]:
                        items = self.Qcombo_company.findText(row[0])
                        for item in range(items + 2):
                            # if int(row1[1]) == 1:
                            self.Qcombo_company.setChecked(i)
                            self.FN_GET_Branch_Wiithoutselectcompany(mycursor,row[0])


                    if row[1] == row1[1]:
                        items = self.Qcombo_branch.findText(row[1])
                        for item in range(items + 2):
                            # if int(row1[1]) == 1:
                            self.Qcombo_branch.setChecked(i)
                i = i + 1
        except:
            print(sys.exc_info())

    # Get selected Data For CustomerGroupe
    def FN_GetSlectedCustomerGroupeForThisProgram(self,mycursor):
        try:
            sql23 = "SELECT CG_GROUP_ID FROM Hyper1_Retail.INSTALLMENT_GROUP   WHERE INST_PROGRAM_ID='" + self.InstallmentNo + "'"
            mycursor.execute(sql23)
            records211 = mycursor.fetchall()

            sql_select_Customer = "SELECT CG_GROUP_ID FROM Hyper1_Retail.CUSTOMER_GROUP "
            mycursor.execute(sql_select_Customer)
            record = mycursor.fetchall()
            print("records21_record",len(records211))
            print("sql_select_Customer_record",len(record))
            i = 0
            for row in record:
                print("row[",i,"]", row)
                for row1 in records211:
                    print("row1",row1)
                    print("row[0]",row[0],"row1[0]",row1[0])

                    #self.Qcombo_customerGroupe.setChecked(i)
                    if str(row[0]) == str(row1[0]):
                        print("if == row[0]", str(row[0]), "row1[0]", str(row1[0]))

                        items = self.Qcombo_customerGroupe.findText(str(row[0]))
                        print("items",items)
                        for item in range(items + 2):
                            self.Qcombo_customerGroupe.setChecked(i)

                i = i + 1
        except:
            print(sys.exc_info())

    #Get customer Banck or vendor or hyperone
    def FN_GetSlectedBankOrVendorOrHyperoneForThisProgram(self,mycursorm , INSTR_RULEID):
        try:
            sql21 = "SELECT SPONSOR_ID , BANK_ID, HYPERONE, INSTS_SPONSOR_REASONS FROM Hyper1_Retail.INSTALLMENT_SPONSOR   WHERE INSTR_RULEID='" + str(INSTR_RULEID) + "'"
            mycursorm.execute(sql21)
            records21 = mycursorm.fetchall()
            for SPONSOR_ID , BANK_ID, HYPERONE, INSTS_SPONSOR_REASONS in records21:
                print("SPONSOR_ID",SPONSOR_ID)
                print("BANK_ID",BANK_ID)
                print("HYPERONE",HYPERONE)
                print("INSTS_SPONSOR_REASONS",INSTS_SPONSOR_REASONS)

                if SPONSOR_ID != None:
                    self.RBTN_vendor.setChecked(True)
                    self.QTEdit_sponsorReason.setText(INSTS_SPONSOR_REASONS)
                    self.FN_GET_Vendor()
                    sql_select_sponser = "SELECT SPONSER_ID ,SPONSER_SAP_CODE FROM Hyper1_Retail.SPONSER"
                    mycursorm.execute(sql_select_sponser)
                    record = mycursorm.fetchall()
                    i = 0
                    for row in record:
                        for row1 in records21:
                            if row[0] == row1[0]:
                                items = self.Qcombo_vendor.findText(row[0])
                                for item in range(items + 2):
                                    #if int(row1[1]) == 1:
                                    self.Qcombo_vendor.setCurrentIndex(i)
                        i = i + 1

                elif BANK_ID != None:
                    self.RBTN_bank.setChecked(True)
                    self.FN_GET_Banks()
                    sql_select_bank = "SELECT Bank_Desc,Bank_ID FROM BANK"
                    mycursorm.execute(sql_select_bank)
                    record = mycursorm.fetchall()
                    i = 0
                    for row in record:
                        for row1 in records21:
                            if row[0] == row1[0]:
                                items = self.Qcombo_bank.findText(row[0])
                                for item in range(items + 2):
                                    # if int(row1[1]) == 1:
                                    self.Qcombo_bank.setCurrentIndex(i)
                        i = i + 1

                elif HYPERONE != None:
                    self.RBTN_hyperone.setChecked(True)
        except:
            print(sys.exc_info())

    # Get installment Department and sections and BMC
    def FN_GetSlectedDepartmentAndSectionsAndBMCForThisProgram(self,mycursorm , INSTR_RULEID):
        try:
            sql21 = "SELECT DEPARTMENT_ID,SECTION_ID,BMC_ID FROM Hyper1_Retail.INSTALLMENT_SECTION  WHERE INSTR_RULEID='" + str(INSTR_RULEID) + "'"
            print("FN_GetSlectedDepartmentAndSectionsAndBMCForThisProgram",sql21)
            mycursorm.execute(sql21)
            records21 = mycursorm.fetchall()
            for DEPARTMENT_ID,SECTION_ID,BMC_ID in records21:
                if DEPARTMENT_ID != None:
                    self.checkBox_department.setChecked(True)
                    #self.FN_GET_Department()
                    sql_select_sponser = "SELECT DEPARTMENT_ID FROM Hyper1_Retail.DEPARTMENT"
                    mycursorm.execute(sql_select_sponser)
                    record = mycursorm.fetchall()
                    i = 0
                    for row in record:
                        for row1 in records21:
                            if str(row[0]) == str(row1[0]):
                                items = self.Qcombo_department.findText(str(row[0]))
                                for item in range(items + 2):
                                    # if int(row1[1]) == 1:
                                    self.Qcombo_department.setChecked(i)
                        i = i + 1

                if SECTION_ID != None:
                    self.checkBox_section.setChecked(True)
                    #self.FN_GET_sections()
                    sql_select_sponser = "SELECT SECTION_ID FROM Hyper1_Retail.SECTION"
                    mycursorm.execute(sql_select_sponser)
                    record = mycursorm.fetchall()
                    i = 0
                    for row in record:
                        for row1 in records21:
                            if str(row[0]) == str(row1[1]):
                                items = self.Qcombo_section.findText(str(row[0]))
                                for item in range(items + 2):
                                    # if int(row1[1]) == 1:
                                    self.Qcombo_section.setChecked(i)


                if BMC_ID != None:
                    self.checkBox_BMCLevel.setChecked(True)
                    #self.FN_GET_BMC_Level()
                    sql_select_sponser = "SELECT BMC_LEVEL4 FROM Hyper1_Retail.BMC_LEVEL4"
                    mycursorm.execute(sql_select_sponser)
                    record = mycursorm.fetchall()
                    i = 0
                    for row in record:
                        for row1 in records21:
                            if str(row[0]) == str(row1[2]):
                                items = self.Qcombo_BMCLevel.findText(str(row[0]))
                                for item in range(items + 2):
                                    # if int(row1[1]) == 1:
                                    self.Qcombo_BMCLevel.setChecked(i)
                i = i + 1

        except:
            print(sys.exc_info())

    #Validate installment program
    def FN_ValidateInstallemt(self):
        error=0
        if len(self.QL_installmentNo.text()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى ادخال رقم البرنامج والبحث اولا")
            error = 0


        elif len(self.QTEdit_descInstallment.toPlainText()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى إدخال الوصف")

            error = 0
        else:
            error = 1

        return error

    # TO clear Data From QTable
    def FN_ClearAcepptedQTableData(self):
        for i in reversed(range(self.Qtable_acceptedItems.rowCount())):
            self.Qtable_acceptedItems.removeRow(i)

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
                sql0 = "  LOCK  TABLES   Hyper1_Retail.INSTALLMENT_PROGRAM   WRITE , Hyper1_Retail.SYS_CHANGE_LOG  WRITE"
                mycursor.execute(sql0)

                ModifingDateTime = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                creationDate = str(datetime.today().strftime('%Y-%m-%d'))

                ToDateTime = self.Qdate_to.dateTime().toString('yyyy-MM-dd') + " " + str(self.Qtime_to.dateTime().toString('hh:mm'))

                # insert to INSTALLMENT_PROGRAM
                if ToDateTime != self.oldstatusDateTo :
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_VALID_TO='"+ToDateTime+"' , INST_CHANGED_ON = '" + ModifingDateTime + "' , INST_CHANGED_BY = " + CL_userModule.user_name + " , INST_ACTIVATED_BY = " + CL_userModule.user_name + " where INST_PROGRAM_ID='" + self.InstallmentNo + "'"
                    print("sql2", sql2)
                    mycursor.execute(sql2)

                    # TODO Insert in log table
                    sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY) VALUES (%s,%s,%s,%s,%s,%s,%s)"

                    val8 = (self.InstallmentNo, 'INSTALLMENT_PROGRAM', 'INST_VALID_TO', self.oldstatusDateTo,
                            ToDateTime,
                            creationDate,
                            CL_userModule.user_name)
                    print("sql8", sql8)
                    mycursor.execute(sql8,val8)

                elif ToDateTime == self.oldstatusDateTo:
                    QtWidgets.QMessageBox.warning(self, "Error", "Data doesn't change")


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