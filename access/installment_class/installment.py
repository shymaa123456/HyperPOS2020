from pathlib import Path
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import sys

from pathlib import Path
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate ,QTime
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QAbstractItemView

from access.Checkable import CheckableComboBox
import mysql.connector

#from access.promotion_class.Promotion_Add import CheckableComboBox

from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule

from datetime import datetime
from Validation.Validation import CL_validation

import xlrd
from datetime import datetime
import xlwt.Workbook

import webbrowser
from decimal import Decimal

class CL_installment(QtWidgets.QDialog):
    dirname = ''
    parent = ''
    def __init__(self,parentInit):
        super(CL_installment, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/installment_ui'
        self.conn = db1.connect()
        self.parent = parentInit


    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Installment_create.ui'
        loadUi(filename, self)

        #Get installment type
        self.FN_GET_installment_types_period()

        # test Multi selection for company
        #self.Qcombo_company = CheckableComboBoxM(self, self.Qcombo_installmentTest)

        #drob down list with multiselection for company
        self.Qcombo_company = CheckableComboBox(self)
        self.Qcombo_company.setGeometry(570,20,179,20)
        self.Qcombo_company.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Company()

        # TODO Click listner for changing list of company
        self.Qcombo_company.model().dataChanged.connect(self.FN_GET_Branch)

        #drob down list with multiselection for bracnch
        self.Qcombo_branch = CheckableComboBox(self)
        self.Qcombo_branch.setGeometry(570,60,179,20)
        self.Qcombo_branch.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Branch()

        #validation for not pick date before today
        datefrom = str(datetime.today().strftime('%Y-%m-%d'))
        xfrom = datefrom.split("-")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        self.Qdate_from.setMinimumDate(d)
        self.Qdate_to.setMinimumDate(d)

        # set minimum time
        # this_moment PyQt5.QtCore.QTime(10, 43, 1, 872)
        # print(self.Qdate_from.dateTime().toString('yyyy-MM-dd'))
        this_moment = QtCore.QTime.currentTime()
        #this_moment = this_moment.toString('hh:mm')
        print("this_moment", this_moment)
        self.Qtime_to.setTime(this_moment)
        self.Qtime_from.setTime(this_moment)
        self.Qtime_from.setMinimumTime(this_moment)
        self.Qtime_to.setMinimumTime(this_moment)

        """
        datefrom = str(datetime.today().strftime('hh:mm:ss'))
        print("datefrom",datefrom)
        xfrom = datefrom.split(":")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        self.Qdate_from.setMinimumDate(d)
        
        #validation for not pick time before now
        timefrom = str(datetime.today().strftime('%h:%m'))
        xfromt = timefrom.split(":")
        t = QTime(xfromt[0], xfromt[1] ,0 ,0)
        print("t",t)
        self.Qtime_from.setMinimumTime(t)
        """

        # Get customer Groupe
        self.Qcombo_customerGroupe = CheckableComboBox(self)
        self.Qcombo_customerGroupe.setGeometry(570, 100, 179, 20)
        self.Qcombo_customerGroupe.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_customerGroupe.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_customerGroupe()


        #Multi selection for department
        self.Qcombo_department = CheckableComboBox(self)
        self.Qcombo_department.setGeometry(570, 150, 171, 22)
        self.Qcombo_department.setEnabled(False)
        self.Qcombo_department.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_department.setStyleSheet("background-color: rgb(198, 207, 199)")

        #TODO Click listner for changing list of department
        self.Qcombo_department.model().dataChanged.connect(self.FN_WhenChecksection)

        # get Department list if check box
        self.checkBox_department.stateChanged.connect(self.FN_WhenCheckDepartment)
        #self.FN_WhenCheckDepartment()

        # Multi selection for sections
        self.Qcombo_section = CheckableComboBox(self)
        self.Qcombo_section.setGeometry(570, 175, 171, 22)
        self.Qcombo_section.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_section.setEnabled(False)
        self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")

        # get sections list if check box
        self.checkBox_section.stateChanged.connect(self.FN_WhenChecksection)
        #self.FN_GET_sections()

        # TODO Click listner for changing list of department
        self.Qcombo_section.model().dataChanged.connect(self.FN_WhenCheckBMC_Level)

        # Multi selection for BMCLevel
        self.Qcombo_BMCLevel = CheckableComboBox(self)
        self.Qcombo_BMCLevel.setGeometry(570, 200, 171, 22)
        self.Qcombo_BMCLevel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Qcombo_BMCLevel.setEnabled(False)
        self.Qcombo_BMCLevel.setStyleSheet("background-color: rgb(198, 207, 199)")

        # get BMC LEVEL4 list if check box
        self.checkBox_BMCLevel.stateChanged.connect(self.FN_WhenCheckBMC_Level)
        #self.FN_GET_BMC_Level()

        # get Banks list if readio button clicked
        self.RBTN_bank.clicked.connect(self.FN_InstallMent_Checked)

        # get Vendor list if readio button clicked
        self.RBTN_vendor.clicked.connect(self.FN_InstallMent_Checked)

        # if readio button clicked hyperone
        self.RBTN_hyperone.clicked.connect(self.FN_InstallMent_Checked)

        #click button for upload accepted items                      Qtable_acceptedItems
        self.Qbtn_loadItems.clicked.connect(self.FN_UploadAcceptedItems(
            self.Qtable_acceptedItems , self.checkBox_department ,self.Qcombo_department,
            self.checkBox_section,self.Qcombo_section,self.checkBox_BMCLevel,self.Qcombo_BMCLevel))

        #click button for upload rejected items
        self.Qbtn_loadRejectItem.clicked.connect(self.FN_UploadAcceptedItems(self.Qtable_rejectedItems ,self.checkBox_department ,self.Qcombo_department,
            self.checkBox_section,self.Qcombo_section,self.checkBox_BMCLevel,self.Qcombo_BMCLevel))

        # click button for remove selected item from accepted Qtable
        self.Qbtn_deleteItem.clicked.connect(self.FN_remove_selected(self.Qtable_acceptedItems))

        # click button for remove selected item from rejected Qtable
        self.Qbtn_deleteRejectItem.clicked.connect(self.FN_remove_selected(self.Qtable_rejectedItems))

        #clicke in search button for Qtable_acceptedItems
        self.Qbtn_findItem_acceptedItem.clicked.connect(self.FN_Search_ByBarcode(self.Qtable_acceptedItems ,self.QLE_SearchAcceptedBarcode))

        # clicke in search button for Qtable_rejectedItems
        self.Qbtn_findItem_rejected.clicked.connect(self.FN_Search_ByBarcode(self.Qtable_rejectedItems,self.QLE_SearchRejectedBarcode))

        # Total interest rate
        self.QDubleSpiner_customerRate.valueChanged.connect(self.FN_PutInterestRate)
        self.QDubleSpiner_vendorRate.valueChanged.connect(self.FN_PutInterestRate)
        self.QDubleSpiner_hperoneRate.valueChanged.connect(self.FN_PutInterestRate)

        #Save installment
        self.Qbtn_saveInstallment.clicked.connect(self.FN_SaveInstallemt)

        # this function for what enabled or not when start
        self.EnabledWhenOpen()

        """"
        timefrom = str(datetime.today().strftime('%h:%m'))
        xfromt = timefrom.split(":")
        t = QTime(int(xfromt[0]), int(xfromt[1]) )
        self.Qtime_from.setMinimumTime(t)
        """

    # this function for what enabled or not when start
    def EnabledWhenOpen(self):
        self.checkBox_department.setEnabled(True)
        self.checkBox_section.setEnabled(False)
        self.Qcombo_section.setEnabled(False)
        self.checkBox_BMCLevel.setEnabled(False)
        self.Qcombo_BMCLevel.setEnabled(False)

    #get installments period list
    def FN_GET_installment_types_period(self):
        self.Qcombo_installmentType.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT InstT_Installment_Period ,INSTT_TYPE_ID FROM INSTALLMENT_TYPE")
        records = mycursor.fetchall()
        mycursor.close()
        for row, val in records:
            self.Qcombo_installmentType.addItem(row, val)

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

    #When click upload button to sellect csv file
    def FN_UploadAcceptedItems(self,QTableWidgit ,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel):
        def FN_UploadAcceptedItems_internal():
            self.window_upload = CL_installment(self)
            self.window_upload.FN_LOAD_UPLOAD(QTableWidgit,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel)
            self.window_upload.show()
        return FN_UploadAcceptedItems_internal

    #Create Ui for upload screen
    def FN_LOAD_UPLOAD(self,QTableWidgit,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel):
            filename = self.dirname + '/uploadBarcodes.ui'
            loadUi(filename, self)
            self.fileName = ''
            print("QTableWidgit1", QTableWidgit)
            self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
            self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD(QTableWidgit,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel))
            self.BTN_saveTemp.clicked.connect(self.FN_DISPLAY_TEMP)

    #get sellected file name
    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName( self, "QFileDialog.getOpenFileName()", "",
                                                   " Files (*.xls)", options=options )
        self.LE_fileName.setText(self.fileName)

    #Save Uploaded csv
    def FN_SAVE_UPLOAD(self,QTableWidgit,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel):
        def FN_SAVE_UPLOAD_internal():
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

                        #validate for check if barcode belong to selected BMC
                        elif self.FN_ValidateIfRelateToDepartmentSectionBMC(str(sheet.cell_value(i,0)),checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel) == False:
                            QtWidgets.QMessageBox.warning(self, "Error", "Barcode doesn't belong to same BMC"+str(sheet.cell_value(i,0)))
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

        return FN_SAVE_UPLOAD_internal

    # Validate if barcode inserted in Qtable before insert it
    def FN_ValidateIfBarcodeInsertedInQtable(self,ValidateBarcode , ValidateQTableWidgit):
        BarcodeFound=0

        # validate if barcode in ValidateQTableWidgit
        for i in range(ValidateQTableWidgit.rowCount()):
            barcode = ValidateQTableWidgit.item(i, 0).text()
            print("repeatedBarcode", barcode)

            if ValidateBarcode == barcode:
                BarcodeFound = 1
                break
            else:
                BarcodeFound = 0

        """
        #validate if barcode in Qtable_acceptedItems
        for i in range(self.Qtable_acceptedItems.rowCount()):
            barcode = self.Qtable_acceptedItems.item(i, 0).text()
            print("repeatedBarcode",barcode)

            if ValidateBarcode == barcode:
                BarcodeFound=1
                break
            else:
                BarcodeFound=0

        #validate if barcode in Qtable_rejectedItems
        for i in range(self.Qtable_rejectedItems.rowCount()):
            barcode = self.Qtable_rejectedItems.item(i, 0).text()
            print("repeatedBarcode",barcode)

            if ValidateBarcode == barcode:
                BarcodeFound=1
                break
            else:
                BarcodeFound=0
        """

        return  BarcodeFound

    # TODO Validate if barcode belong to selected BMC
    def FN_ValidateIfRelateToDepartmentSectionBMC(self,ValidateBarcode,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel ):
        if checkBox_BMCLevel.isChecked() and len(Qcombo_BMCLevel.currentData()) > 0:
            for k in range(len(Qcombo_BMCLevel.currentData())):
                self.conn = db1.connect()
                mycursor = self.conn.cursor()
                #sql="SELECT BMC_ID FROM POS_ITEM WHERE POS_GTIN ='"+ValidateBarcode+"' BMC_ID AND '"+self.Qcombo_BMCLevel.currentData()[k]+"'"
                sql="select a.POS_GTIN , a.BMC_ID  from Hyper1_Retail.POS_ITEM a inner join  Hyper1_Retail.POS_BMC B on a.BMC_ID = B.BMC_ID where a.POS_GTIN ='"+ValidateBarcode+"' AND B.BMC_ID ='"+Qcombo_BMCLevel.currentData()[k]+"'"

                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                print("FN_ValidateIfRelateToDepartmentSectionBMC",len(myresult))
                if len(myresult) == 0:
                    if k == len(Qcombo_BMCLevel.currentData()) :
                        return False
                else:
                    return True

        elif checkBox_section.isChecked() and len(Qcombo_section.currentData()) > 0 and not checkBox_BMCLevel.isChecked():
            for k in range(len(Qcombo_section.currentData())):
                self.conn = db1.connect()
                mycursor = self.conn.cursor()
                #sql="SELECT BMC_ID FROM POS_ITEM WHERE POS_GTIN ='"+ValidateBarcode+"' BMC_ID AND '"+self.Qcombo_BMCLevel.currentData()[k]+"'"
                sql="select a.POS_GTIN , a.BMC_ID  from Hyper1_Retail.POS_ITEM a inner join  Hyper1_Retail.POS_BMC B on a.BMC_ID = B.BMC_ID where a.POS_GTIN ='"+ValidateBarcode+"' AND B.SECTION_ID ='"+Qcombo_section.currentData()[k]+"'"

                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                print("FN_ValidateIfRelateToDepartmentSectionBMC",len(myresult))
                if len(myresult) == 0:
                    if k == len(Qcombo_section.currentData()) :
                        return False
                else:
                    return True

        elif checkBox_department.isChecked() and len(Qcombo_department.currentData()) > 0 and not checkBox_section.isChecked() and not checkBox_BMCLevel.isChecked():
            for k in range(len(Qcombo_department.currentData())):
                self.conn = db1.connect()
                mycursor = self.conn.cursor()
                #sql="SELECT BMC_ID FROM POS_ITEM WHERE POS_GTIN ='"+ValidateBarcode+"' BMC_ID AND '"+self.Qcombo_BMCLevel.currentData()[k]+"'"
                sql="select a.POS_GTIN , a.BMC_ID  from Hyper1_Retail.POS_ITEM a inner join  Hyper1_Retail.POS_BMC B on a.BMC_ID = B.BMC_ID where a.POS_GTIN ='"+ValidateBarcode+"' AND B.DEPARTMENT_ID ='"+Qcombo_department.currentData()[k]+"'"

                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                print("FN_ValidateIfRelateToDepartmentSectionBMC",len(myresult))
                if len(myresult) == 0:
                    if k == len(Qcombo_BMCLevel.currentData()) :
                        return False
                else:
                    return True

    # TODO Validate if barcode belong to selected Department or sections or BMC
    def FN_ValidateRejectedBarcodeWhenSelectDapartmentOrSectionsOrBMC(self,QTableWidgit ,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel):
        print("FN_ValidateRejectedBarcodeWhenSelectDapartmentOrSectionsOrBMC")
        for i in range(QTableWidgit.rowCount()):
            barcode = QTableWidgit.item(i, 0).text()
            if self.FN_ValidateIfRelateToDepartmentSectionBMC(barcode,checkBox_department,Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel) == False:
                #QtWidgets.QMessageBox.warning(self, "Error","Barcode doesn't belong to same BMC" + str(barcode))
                QTableWidgit.item(i, 0).setBackground(QtGui.QColor(100, 100, 150))

                return False #this barcode desn't belong to any selected department or selection ot BMC
            elif self.FN_ValidateIfRelateToDepartmentSectionBMC(barcode,checkBox_department,
                                                                Qcombo_department,checkBox_section,Qcombo_section,checkBox_BMCLevel,Qcombo_BMCLevel) == True:
                if i ==QTableWidgit.rowCount():
                    return True #this barcode belong to any selected department or selection ot BMC


    # search in Qtable csv
    def FN_Search_ByBarcode(self, QTableWidgit , QlabelEdit):
        def FN_Search_ByBarcode_internal():
                #remove selection in qtable
                for i in range(QTableWidgit.rowCount()):
                        # 198, 207, 199
                    QTableWidgit.item(i, 0).setBackground(QtGui.QColor(198, 207, 199))

                SearchedBarcode=QlabelEdit.text()
                print("SearchedBarcode",SearchedBarcode)
                for i in range(QTableWidgit.rowCount()):
                    barcode = QTableWidgit.item(i, 0).text()
                    if barcode in SearchedBarcode:
                        # 198, 207, 199
                        QTableWidgit.item(i, 0).setBackground(QtGui.QColor(100,100,150))
                        print("search_in")
                    elif not barcode in SearchedBarcode:
                        # 198, 207, 199
                        QtWidgets.QMessageBox.warning(self, "Error", " الباركود غير موجود")
                        print("search_Not_in")
        return FN_Search_ByBarcode_internal

    #SAve Tem of csv that you use it for upload
    def FN_DISPLAY_TEMP(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)
             wb = xlwt.Workbook()
             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'الباركود')
             sheet.write(0, 1, 'الوصف')

             #wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()

             webbrowser.open(filename[0])
         except Exception as err:
             print(err)

    #TO clear Data From QTable
    def FN_ClearAcepptedQTableData(self):
        for i in reversed(range(self.Qtable_acceptedItems.rowCount())):
            self.Qtable_acceptedItems.removeRow(i)

    #remove selected Row from QTable
    def FN_remove_selected(self,QTableWidgit):
        def FN_remove_selected_internal():
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to delete selected rows ?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # get index of selected rows
                indexes = QTableWidgit.selectionModel().selectedRows()
                for index in reversed(sorted(indexes)):
                    QTableWidgit.removeRow(index.row())

        return FN_remove_selected_internal

    #put interest rate
    def FN_PutInterestRate(self):
        if (self.QDubleSpiner_customerRate.value()
            +self.QDubleSpiner_vendorRate.value()
            +self.QDubleSpiner_hperoneRate.value()) <= 100 :

            self.QDubleSpiner_interestRate.setValue(
                self.QDubleSpiner_customerRate.value()
                +self.QDubleSpiner_vendorRate.value()
                +self.QDubleSpiner_hperoneRate.value()
            )
        else:
            QtWidgets.QMessageBox.warning(self, "Error",  "summation of rate  is more than 100")
            self.QDubleSpiner_customerRate.setValue(0)
            self.QDubleSpiner_vendorRate.setValue(0)
            self.QDubleSpiner_hperoneRate.setValue(0)

    #TODO save installment

    #to save installment
    def FN_SaveInstallemt(self):
        error = 0
        Validation_For_installmentProgramm=0

        error = self.FN_ValidateInstallemt()
        print(error)
        if error !=0:

            try:
                self.conn = db1.connect()
                self.conn.autocommit = False
                mycursor = self.conn.cursor()
                self.conn.start_transaction()

                # # lock table for new record:
                sql0 = "  LOCK  TABLES    Hyper1_Retail.INSTALLMENT_BRANCH   WRITE , " \
                       "  Hyper1_Retail.INSTALLMENT_GROUP   WRITE ,  Hyper1_Retail.INSTALLMENT_ITEM   WRITE," \
                       " Hyper1_Retail.INSTALLMENT_REJECTED_ITEM   WRITE ,  Hyper1_Retail.INSTALLMENT_SECTION   WRITE ," \
                       " Hyper1_Retail.INSTALLMENT_SPONSOR   WRITE ,  Hyper1_Retail.INSTALLMENT_PROGRAM   WRITE ," \
                       " Hyper1_Retail.INSTALLMENT_RULE    WRITE , Hyper1_Retail.INSTALLMENT_TYPE    WRITE "
                mycursor.execute(sql0)

                #Check if this program create before or not
                #Validation_For_installmentProgramm = 1
                Validation_For_installmentProgramm = self.FN_ValidateInstallemtProgram(mycursor)
                print("Validation_For_installmentProgramm",Validation_For_installmentProgramm)
                #self.FN_ValidateInstallemtProgram(mycursor )
                if Validation_For_installmentProgramm == False:
                    #  Get installment Type
                    Index_installmentType = self.Qcombo_installmentType.currentData()  # installment type id
                    print("Index_installmentType",Index_installmentType)

                    #insert installment type in INSTALLMENT_RULE Table
                    sql1 = "INSERT INTO INSTALLMENT_RULE (INSTT_TYPE_ID,INSTR_DESC, INSTR_INTEREST_RATE, INSTR_SPONSOR_RATE , INSTR_HYPER_RATE,  INSTR_CUSTOMER_RATE, INSTR_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    val1 = (
                        Index_installmentType,self.QTEdit_descInstallment.toPlainText(),str(self.QDubleSpiner_interestRate.value()),str(self.QDubleSpiner_customerRate.value()),
                           str(self.QDubleSpiner_vendorRate.value()),str(self.QDubleSpiner_hperoneRate.value()),
                        '1')
                    print("val1",val1)
                    mycursor.execute(sql1, val1)


                    #Get max index INSTALLMENT_RULE -- index of inserted
                    mycursor.execute(
                        "SELECT max(cast(INSTR_RULEID  AS UNSIGNED)) FROM Hyper1_Retail.INSTALLMENT_RULE")
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        self.id_INSTR_RULEID = "1"
                    else:
                        self.id_INSTR_RULEID = int(myresult[0])

                    print("self.id_INSTR_RULEID",self.id_INSTR_RULEID)

                    #get values for insert in INSTALLMENT_PROGRAM table
                    FromDateTime = self.Qdate_from.dateTime().toString('yyyy-MM-dd')+" "+ str(self.Qtime_from.dateTime().toString('hh:mm'))
                    print("creationDateTime",FromDateTime)
                    ToDateTime = self.Qdate_to.dateTime().toString('yyyy-MM-dd') + " " + str(self.Qtime_to.dateTime().toString('hh:mm'))

                    creationDateTime = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

                    #insert to INSTALLMENT_PROGRAM
                    sql2 = "INSERT INTO INSTALLMENT_PROGRAM (INST_DESC, INSTR_RULEID, INST_CREATED_ON ,  INST_CREATED_BY, INST_VALID_FROM ,INST_VALID_TO ,INST_ADMIN_EXPENSES , INST_ADMIN_EXPENSES_MIN , INST_ADMIN_EXPENSES_MAX ,INST_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val2 = (
                         self.QTEdit_descInstallment.toPlainText(), self.id_INSTR_RULEID ,creationDateTime,
                        CL_userModule.user_name, FromDateTime,ToDateTime   ,self.QDSpinBox_adminExpendses.value(),
                        self.QDSpinBox_Min_adminExpendses.value(),self.QDSpinBox_Max_adminExpendses.value(),'0')
                    mycursor.execute(sql2, val2)

                    # Get max index Installment_programm -- index of inserted
                    mycursor.execute(
                        "SELECT max(cast(inst_Program_ID  AS UNSIGNED)) FROM Hyper1_Retail.INSTALLMENT_PROGRAM")
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        self.inst_Program_ID = "1"
                    else:
                        self.inst_Program_ID = int(myresult[0])

                    #to get company and branch Qcombo Data and insert it in DB
                    for j in range(len(self.Qcombo_company.currentData())):
                        for i in range(len(self.Qcombo_branch.currentData())):
                            sql3 = "INSERT INTO INSTALLMENT_BRANCH (COMPANY_ID,BRANCH_NO,inst_Program_ID,STATUS) VALUES (%s,%s,%s,%s)"
                            val3 = (
                                self.Qcombo_company.currentData()[j], self.Qcombo_branch.currentData()[i],
                                self.inst_Program_ID,
                                '1')
                            mycursor.execute(sql3, val3)

                    #insert Installment_GROUP
                    for j in range(len(self.Qcombo_customerGroupe.currentData())):
                        sql4 = "INSERT INTO INSTALLMENT_GROUP (CG_group_id,inst_Program_ID,STATUS) VALUES (%s,%s,%s)"
                        val4 = (
                            self.Qcombo_customerGroupe.currentData()[j], self.inst_Program_ID,
                                '1')
                        mycursor.execute(sql4, val4)

                    #insert Installment_item
                    if self.Qtable_acceptedItems.rowCount() != 0 :
                        for i in range(self.Qtable_acceptedItems.rowCount()):
                            barcode = self.Qtable_acceptedItems.item(i, 0).text()
                            sql5 = "INSERT INTO INSTALLMENT_ITEM (POS_GTIN,instR_RuleID,STATUS) VALUES (%s,%s,%s)"
                            val5 = (
                                barcode, self.id_INSTR_RULEID,
                                '1')
                            mycursor.execute(sql5, val5)

                    #insert Installment_department_section_BMC
                    elif self.checkBox_department.isChecked():
                        self.FN_SaveDepartmentSectionBMCLeve(mycursor)

                    #insert rejected items to Installment_rejected_item
                    if self.Qtable_rejectedItems.rowCount() != 0 :
                        for i in range(self.Qtable_rejectedItems.rowCount()):
                            barcode_rejected = self.Qtable_rejectedItems.item(i, 0).text()
                            sql7 = "INSERT INTO INSTALLMENT_REJECTED_ITEM (POS_GTIN,instR_RuleID,STATUS) VALUES (%s,%s,%s)"
                            val7 = (
                                barcode_rejected, self.id_INSTR_RULEID,
                                '1')
                            mycursor.execute(sql7, val7)

                    #insert to Installment_Sponsor table
                    if self.RBTN_bank.isChecked() or self.RBTN_vendor.isChecked() or self.RBTN_hyperone.isChecked():
                        self.FN_Insert_If_Bank_Vendor_hyperone_Checked(self.id_INSTR_RULEID , mycursor)

                    QtWidgets.QMessageBox.information(self, "Success", "Installment Program Has Been Saved No: "+str(self.inst_Program_ID))
                    self.QL_lastInstallmentNO.setText(str(self.inst_Program_ID))
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "This Installment Program Has Been Created Before")

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

    #insert to Installment_Sponsor table if checked bank or vendor or hyperone for installment type
    def FN_Insert_If_Bank_Vendor_hyperone_Checked(self,id_INSTR_RULEID , mycursor) :
        if self.RBTN_bank.isChecked():
            print("Bank_ID",self.Qcombo_bank.currentData())
            sql8 = "INSERT INTO INSTALLMENT_SPONSOR ( INSTR_RULEID ,BANK_ID,STATUS) VALUES (%s,%s,%s)"
            val8 = (
                id_INSTR_RULEID, self.Qcombo_bank.currentData(),
                '1')
            mycursor.execute(sql8, val8)
        elif self.RBTN_vendor.isChecked():
            print("sponsor_Id",self.Qcombo_vendor.currentData())
            sql8 = "INSERT INTO INSTALLMENT_SPONSOR ( INSTR_RULEID ,SPONSOR_ID ,INSTS_SPONSOR_REASONS ,STATUS) VALUES (%s,%s,%s,%s)"
            val8 = (
                id_INSTR_RULEID, self.Qcombo_vendor.currentData(), self.QTEdit_sponsorReason.toPlainText(),
                '1')
            mycursor.execute(sql8, val8)
        elif self.RBTN_hyperone.isChecked():
            print("HYPERONE")
            sql8 = "INSERT INTO INSTALLMENT_SPONSOR ( INSTR_RULEID , HYPERONE ,STATUS) VALUES (%s,%s,%s)"
            val8 = (
                id_INSTR_RULEID, '1',
                '1')
            mycursor.execute(sql8, val8)

    # insert Installment_department_section_BMC
    def FN_SaveDepartmentSectionBMCLeve(self, mycursor):
        if self.checkBox_department.isChecked() and self.checkBox_section.isChecked() and self.checkBox_BMCLevel.isChecked():
            for j in range(len(self.Qcombo_department.currentData())):
                for i in range(len(self.Qcombo_section.currentData())):
                    for k in range(len(self.Qcombo_BMCLevel.currentData())):
                        sql6 = "INSERT INTO INSTALLMENT_SECTION (INSTR_RULEID, DEPARTMENT_ID, SECTION_ID , BMC_ID ,STATUS) VALUES (%s,%s,%s,%s,%s)"
                        val6 = (
                            self.id_INSTR_RULEID,
                            self.Qcombo_department.currentData()[j],
                            self.Qcombo_section.currentData()[i],
                            self.Qcombo_BMCLevel.currentData()[k],
                            '1')
                        mycursor.execute(sql6, val6)

        elif self.checkBox_department.isChecked() and self.checkBox_section.isChecked() and not self.checkBox_BMCLevel.isChecked():
            for j in range(len(self.Qcombo_department.currentData())):
                for i in range(len(self.Qcombo_section.currentData())):
                    sql6 = "INSERT INTO INSTALLMENT_SECTION (INSTR_RULEID, DEPARTMENT_ID, SECTION_ID  ,STATUS) VALUES (%s,%s,%s,%s)"
                    val6 = (
                        self.id_INSTR_RULEID,
                        self.Qcombo_department.currentData()[j],
                        self.Qcombo_section.currentData()[i],
                        '1')
                    mycursor.execute(sql6, val6)

        elif self.checkBox_department.isChecked() and not self.checkBox_section.isChecked() and not self.checkBox_BMCLevel.isChecked():
            for j in range(len(self.Qcombo_department.currentData())):
                sql6 = "INSERT INTO INSTALLMENT_SECTION (INSTR_RULEID, DEPARTMENT_ID, STATUS) VALUES (%s,%s,%s)"
                val6 = (
                    self.id_INSTR_RULEID,
                    self.Qcombo_department.currentData()[j],
                    '1')
                mycursor.execute(sql6, val6)


    # TODO Validat before save program
    # to save installment
    def FN_ValidateInstallemt(self):
        print(self.Qcombo_installmentType.currentText())
        error = 0

        if self.Qcombo_installmentType.currentText() == '':
            QtWidgets.QMessageBox.warning(self, "Error", "installment type is empty")
            error = 0

        elif len(self.QTEdit_descInstallment.toPlainText()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى إدخال الوصف")
            error = 0

        elif len(self.Qcombo_company.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار الشركه ")
            error = 0

        elif len(self.Qcombo_branch.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار الفرع ")
            error = 0

        elif len(self.Qcombo_customerGroupe.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار العملاء ")
            error = 0

        elif self.Qtable_acceptedItems.rowCount() == 0 and not self.checkBox_department.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى إدخال اصناف التقسيط او اختيار الاقسام")
            error = 0

        elif self.checkBox_department.isChecked() and len(self.Qcombo_department.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار الأداره")
            error = 0

        elif self.checkBox_section.isChecked() and len(self.Qcombo_section.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار القسم")
            error = 0

        elif self.checkBox_BMCLevel.isChecked() and len(self.Qcombo_BMCLevel.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار القسم الفرعى")
            error = 0

            """
        elif self.checkBox_department.isChecked() and not self.checkBox_section.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار القسم")
            error = 0

        elif self.checkBox_section.isChecked() and not self.checkBox_BMCLevel.isChecked() :
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار القسم الفرعى")
            error = 0
            """
        elif self.RBTN_bank.isChecked() and self.Qcombo_bank.currentText() == '' :
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار البنك")
            error = 0

        elif self.RBTN_vendor.isChecked() and len(self.Qcombo_vendor.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى أختيار الممول")
            error = 0

        elif self.QDubleSpiner_customerRate.value() == 0 \
                and self.QDubleSpiner_vendorRate.value() == 0 \
                and self.QDubleSpiner_hperoneRate.value() == 0:
            QtWidgets.QMessageBox.warning(self, "Error", "يرجى أدخال نسبه الفائده للعميل او للممول او للهايبر")
            error = 0
        elif self.FN_ValidateRejectedBarcodeWhenSelectDapartmentOrSectionsOrBMC(self.Qtable_rejectedItems ,self.checkBox_department ,self.Qcombo_department,
            self.checkBox_section,self.Qcombo_section,self.checkBox_BMCLevel,self.Qcombo_BMCLevel) == False:
            QtWidgets.QMessageBox.warning(self, "Error", " يوجد باركودات مرفوضه ولا تنتمى لنفس القسم ")
            error = 0

        else:
            error = 1

        return error

    #validate if installment program created before or not
    def FN_ValidateInstallemtProgram(self,mycursor):
        Return_FN_ValidateInstallemtProgram=True

        print("FN_ValidateInstallemtProgram")
        Index_installmentType = self.Qcombo_installmentType.currentData()  # installment type id
        print("Validate_Index_installmentType", Index_installmentType)

        # VALIDATE INSTT_TYPE_ID in INSTALLMENT_RULE Table
        sql1 = "SELECT INSTR_RULEID FROM INSTALLMENT_RULE WHERE INSTT_TYPE_ID = "+str(Index_installmentType)
        mycursor.execute(sql1)
        print("VALIDATEsql1",sql1)
        myresult = mycursor.fetchall()
        print("len(myresult)",len(myresult))

        if len(myresult) == 0 :
            Return_FN_ValidateInstallemtProgram = False
            return Return_FN_ValidateInstallemtProgram
        else:
            for row_number, row_data in enumerate(myresult):
                for column_number, INSTR_RULEID_ID in enumerate(row_data):
                    print("column_number ",column_number, " INSTR_RULEID_ID ",INSTR_RULEID_ID)

                    #Validate installmentRuleWithBankAndVendorAndHyper
                    Validate_installmentRuleWithBankAndVendorAndHyper = self.FN_ValidateInstallmentRuleWithBankORVendorORHyper(INSTR_RULEID_ID,mycursor)

                    #Validate AcceptedItems OR deparments and sections and BMC
                    Validate_AcceptedItems_deparments_sections_BMC =self.FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC(INSTR_RULEID_ID,mycursor)

                    print("Validate_installmentRuleWithBankAndVendorAndHyper",Validate_installmentRuleWithBankAndVendorAndHyper)
                    print("Validate_AcceptedItems_deparments_sections_BMC",Validate_AcceptedItems_deparments_sections_BMC)

                    if Validate_installmentRuleWithBankAndVendorAndHyper == False \
                            and Validate_AcceptedItems_deparments_sections_BMC ==False :
                        print("Validate_if","False")
                        Return_FN_ValidateInstallemtProgram = False
                    elif Validate_installmentRuleWithBankAndVendorAndHyper == True \
                            and Validate_AcceptedItems_deparments_sections_BMC ==True:
                        Return_FN_ValidateInstallemtProgram =  True
                        return  Return_FN_ValidateInstallemtProgram

            return  Return_FN_ValidateInstallemtProgram

        """
                for installmentType
        if myresult[0] == None:
            Validation_For_installmentProgramm_INSTT_TYPE_ID = 1
        else:
            Validation_For_installmentProgramm_INSTT_TYPE_ID = 0

        print("Validate INSTT_TYPE_ID",Validation_For_installmentProgramm_INSTT_TYPE_ID)

        #validate Bank or vendor or hyperone is checked
        if self.RBTN_bank.isChecked():
            print("Bank_ID",self.Qcombo_bank.currentData())
            sql8 = "INSERT INTO INSTALLMENT_SPONSOR ( INSTR_RULEID ,BANK_ID,STATUS) VALUES (%s,%s,%s)"
            val8 = (
                id_INSTR_RULEID, self.Qcombo_bank.currentData(),
                '1')
            mycursor.execute(sql8, val8)
        elif self.RBTN_vendor.isChecked():
            print("sponsor_Id",self.Qcombo_vendor.currentData())
            sql8 = "INSERT INTO INSTALLMENT_SPONSOR ( INSTR_RULEID ,SPONSOR_ID ,INSTS_SPONSOR_REASONS ,STATUS) VALUES (%s,%s,%s,%s)"
            val8 = (
                id_INSTR_RULEID, self.Qcombo_vendor.currentData(), self.QTEdit_sponsorReason.toPlainText(),
                '1')
            mycursor.execute(sql8, val8)
        elif self.RBTN_hyperone.isChecked():
            print("HYPERONE")
            sql8 = "INSERT INTO INSTALLMENT_SPONSOR ( INSTR_RULEID , HYPERONE ,STATUS) VALUES (%s,%s,%s)"
            val8 = (
                id_INSTR_RULEID, '1',
                '1')
            mycursor.execute(sql8, val8)
        
        #elif self.Qtable_acceptedItems.rowCount() == 0 and not self.checkBox_department.isChecked():

        sql1 = "select INST_DESC from INSTALLMENT_PROGRAM "
        
                val2 = (
                    self.QTEdit_descInstallment.toPlainText(), self.id_INSTR_RULEID, creationDateTime,
                    CL_userModule.user_name, FromDateTime, ToDateTime, self.QDSpinBox_adminExpendses.value(),
                    '0')
                    sql1 = "INSERT INTO INSTALLMENT_RULE (INSTT_TYPE_ID,INSTR_DESC, INSTR_INTEREST_RATE, INSTR_SPONSOR_RATE , INSTR_HYPER_RATE,  INSTR_CUSTOMER_RATE, INSTR_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    val1 = (
                        Index_installmentType,self.QTEdit_descInstallment.toPlainText(),str(self.QDubleSpiner_interestRate.value()),str(self.QDubleSpiner_customerRate.value()),
                           str(self.QDubleSpiner_vendorRate.value()),str(self.QDubleSpiner_hperoneRate.value()),
                        '1')
       
        mycursor.execute(sql1)
        myresult = mycursor.fetchone()
        if myresult[0] == None:
            Validation_For_installmentProgramm=1
        else:
            Validation_For_installmentProgramm=0

        return  Validation_For_installmentProgramm
        """

    # Validate installmentRuleWithBankAndVendorAndHyper
    def FN_ValidateInstallmentRuleWithBankORVendorORHyper(self,INSTR_RULEID_ID , mycursor):
        print("FN_ValidateInstallmentRuleWithBankORVendorORHyper")
        if self.RBTN_bank.isChecked():
            print("Bank_ID", self.Qcombo_bank.currentData())
            sql8 = "SELECT BANK_ID FROM INSTALLMENT_SPONSOR WHERE INSTR_RULEID =" + str(
                INSTR_RULEID_ID) + " AND BANK_ID ='" + str(self.Qcombo_bank.currentData())+"'"

        elif self.RBTN_vendor.isChecked():
            print("sponsor_Id", self.Qcombo_vendor.currentData())
            sql8 = "SELECT SPONSOR_ID FROM INSTALLMENT_SPONSOR WHERE INSTR_RULEID =" + str(
                INSTR_RULEID_ID) + " AND SPONSOR_ID ='" + str(self.Qcombo_vendor.currentData())+"'"

        elif self.RBTN_hyperone.isChecked():
            print("HYPERONE")
            sql8 = "SELECT SPONSOR_ID FROM INSTALLMENT_SPONSOR WHERE INSTR_RULEID =" + str(
                INSTR_RULEID_ID) + " AND HYPERONE = '1'"

        print("sql8 ",sql8)
        mycursor.execute(sql8)
        myresult = mycursor.fetchall()

        print("FN_ValidateInstallmentRuleWithBankORVendorORHyper_len(myresult)",len(myresult))
        if len(myresult) == 0 :
            return False
        else:
            return True

    # Validate AcceptedItems OR deparments and sections and BMC
    def FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC(self,INSTR_RULEID_ID,mycursor):
        print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC")
        # validate if barcode in Qtable_acceptedItems
        returnResult = True
        if self.Qtable_acceptedItems.rowCount() > 0 :
            for i in range(self.Qtable_acceptedItems.rowCount()):
                barcode = self.Qtable_acceptedItems.item(i, 0).text()

                sql5 = "SELECT POS_GTIN FROM INSTALLMENT_ITEM WHERE POS_GTIN ="+str(barcode) +" AND INSTR_RULEID ="+str(INSTR_RULEID_ID)
                mycursor.execute(sql5)
                myresult = mycursor.fetchall()

                print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_sql5", sql5)

                print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_len(myresult)", len(myresult))

                if len(myresult) == 0:
                    returnResult = False
                else:
                    returnResult = True
                    break

            print("Qtable_acceptedItems_V_returnResult",returnResult)
            return returnResult

        # validate for Department or sections or mbc  Befor save program
        elif self.checkBox_department.isChecked():
            if self.checkBox_department.isChecked() and self.checkBox_section.isChecked() and self.checkBox_BMCLevel.isChecked():
                        for k in range(len(self.Qcombo_BMCLevel.currentData())):
                            sql6 = "SELECT BMC_ID FROM INSTALLMENT_SECTION WHERE BMC_ID =" + str(self.Qcombo_BMCLevel.currentData()[k]) + " AND INSTR_RULEID =" + str(INSTR_RULEID_ID)
                            mycursor.execute(sql6)
                            myresult = mycursor.fetchall()
                            print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_sql6", sql6)

                            print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_len(myresult)", len(myresult))

                            if len(myresult) == 0:
                                returnResult = False
                            else:
                                returnResult = True
                                break
            elif self.checkBox_department.isChecked() and self.checkBox_section.isChecked() and not self.checkBox_BMCLevel.isChecked():
                    for i in range(len(self.Qcombo_section.currentData())):
                        sql6 = "SELECT SECTION_ID FROM INSTALLMENT_SECTION WHERE SECTION_ID =" + str(
                            self.Qcombo_section.currentData()[i]) + " AND INSTR_RULEID =" + str(INSTR_RULEID_ID)
                        mycursor.execute(sql6)

                        myresult = mycursor.fetchall()
                        print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_sql6", sql6)
                        print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_len(myresult)", len(myresult))

                        if len(myresult) == 0:
                            returnResult = False
                        else:
                            returnResult = True
                            break

            elif self.checkBox_department.isChecked() and not self.checkBox_section.isChecked() and not self.checkBox_BMCLevel.isChecked():
                for j in range(len(self.Qcombo_department.currentData())):
                    sql6 = "SELECT BMC_ID FROM INSTALLMENT_SECTION WHERE DEPARTMENT_ID =" + str(
                        self.Qcombo_department.currentData()[j]) + " AND INSTR_RULEID =" + str(INSTR_RULEID_ID)
                    mycursor.execute(sql6)
                    myresult = mycursor.fetchall()

                    print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_sql6", sql6)

                    print("FN_ValidateIfAcceptedItems_OR_DepartmentAndSectionsBC_len(myresult)", len(myresult))

                    if len(myresult) == 0:
                        returnResult = False
                    else:
                        returnResult = True
                        break

            print("checkBox_department_V_returnResult", returnResult)
            return returnResult





