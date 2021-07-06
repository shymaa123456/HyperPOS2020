from pathlib import Path

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

""""
        #self.dateEdit = QtGui.QDateEdit(self)
        self.Qdate_from.setDateTime(QtCore.QDateTime.currentDateTime())
        self.Qdate_from.setMaximumDate(QtCore.QDate(7999, 12, 28))
        self.Qdate_from.setMaximumTime(QtCore.QTime(23, 59, 59))

        timefrom = str(datetime.today().strftime('%h:%m'))
        xfromt = timefrom.split(":")
        t = QTime(int(xfromt[0]), int(xfromt[1]) )
        self.Qtime_from.setMinimumTime(t)
        
        # self.setWindowTitle('Users')
        #self.Qbtn_saveInstallment.clicked.connect(self.FN_CREATE_Installment)

        #self.Qcombo_company.addItems(["1", "2", "3"])
        #self.Qcombo_branch.addItems(["1", "2", "3"])
        #self.Qcombo_group.addItems(["0", "1"])

    # this function for what enabled or not when start
    def EnabledWhenOpen(self):
        self.checkBox_department.setEnabled(True)
        self.checkBox_section.setEnabled(False)
        self.Qcombo_section.setEnabled(False)
        self.checkBox_BMCLevel.setEnabled(False)
        self.Qcombo_BMCLevel.setEnabled(False)

    #get companys list
    def FN_GET_installment_types_period(self):
        self.Qcombo_installmentType.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT InstT_Installment_Period FROM INSTALLMENT_TYPE")
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.Qcombo_installmentType.addItems([row[0]])

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
         in line 194 create coupon
        to get multselection drop down list items id ex get company id 
                        for j in range(len(self.Qcombo_company.currentData())):
                    for i in range(len(self.Qcombo_branch.currentData())):
                        sql3 = "INSERT INTO COUPON_BRANCH (COMPANY_ID,BRANCH_NO,COUPON_ID,STATUS) VALUES (%s,%s,%s,%s)"
                        val3 = (
                            self.Qcombo_company.currentData()[j], self.Qcombo_branch.currentData()[i],
                            id,
                            '1')
                        mycursor.execute(sql3, val3)
        

    #get branches list
    def FN_GET_Branch(self):
         i=0
         try:
            # Todo: method for fills the Branch combobox
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH")
            records = mycursor.fetchall()
            for row, val in records:
                for bra in CL_userModule.branch :
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1
            mycursor.close()
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
        self.Qcombo_department.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT DEPARTMENT_DESC,DEPARTMENT_ID FROM DEPARTMENT")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_department.addItem(row, val)
        mycursor.close()

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
    # after check Bank check box
    def FN_WhenCheckBank(self):
        if self.checkBox_bank.isChecked():
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
        mycursor.execute("SELECT Bank_Desc FROM BANK")
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.Qcombo_bank.addItems([row[0]])

    # after check Vendor check box
    def FN_WhenCheckVendor(self):
        if self.checkBox_vendor.isChecked():
            self.FN_GET_Vendor()
            self.Qcombo_vendor.setEnabled(True)
        else:
            self.Qcombo_vendor.setEnabled(False)
            self.Qcombo_vendor.clear()

    #get Vendor list
    def FN_GET_Vendor(self):
        self.Qcombo_vendor.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT SPONSER_NAME FROM SPONSER")
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.Qcombo_vendor.addItems([row[0]])

    #When click upload button to sellect csv file
    def FN_UploadAcceptedItems(self,QTableWidgit):
        def FN_UploadAcceptedItems_internal():
            self.window_upload = CL_installment(self)
            self.window_upload.FN_LOAD_UPLOAD(QTableWidgit)
            self.window_upload.show()
        return FN_UploadAcceptedItems_internal

    #Create Ui for upload screen
    def FN_LOAD_UPLOAD(self,QTableWidgit):
            filename = self.dirname + '/uploadBarcodes.ui'
            loadUi(filename, self)
            self.fileName = ''
            print("QTableWidgit1", QTableWidgit)
            self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
            self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD(QTableWidgit))
            self.BTN_saveTemp.clicked.connect(self.FN_DISPLAY_TEMP)

    #get sellected file name
    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName( self, "QFileDialog.getOpenFileName()", "",
                                                   " Files (*.xls)", options=options )
        self.LE_fileName.setText(self.fileName)

    #Save Uploaded csv
    def FN_SAVE_UPLOAD(self,QTableWidgit):
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
                self.msgBox.setWindowTitle( "Information" )
                self.msgBox.setStandardButtons( QMessageBox.Ok)
                self.msgBox.setText(error_message)
                self.msgBox.show()
                self.close()
            #Extracting number of rows
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Choose a file")

        return FN_SAVE_UPLOAD_internal
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


    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyUser.ui'
        loadUi(filename , self)
        records = self.FN_GET_USERS()
        for row in records:
            self.CMB_userName.addItems( [row[0]] )


        self.FN_GET_USER()
        self.CMB_userName.currentIndexChanged.connect( self.FN_GET_USER )
        self.BTN_modifyUser.clicked.connect(self.FN_MODIFY_USER)
        self.CMB_branch.addItems(["1", "2", "3"])
        self.CMB_userType.addItems(["1", "2", "3"])
        self.CMB_userStatus.addItems(["0", "1"])

    

    def FN_CREATE_Installment(self):
        DT_from = self.Qdate_from.dateTime()
        DT_fromString = DT_from.toString(self.Qdate_from.displayFormat())
        print(DT_fromString)
        DT_fromTime= self.Qtime_from.dateTime()
        # dt.toString("dd.MM.yyyy hh:mm:ss.zzz"))
        DT_fromTime_string = DT_fromTime.toString(self.Qtime_from.displayFormat())
        print(DT_fromTime_string)

        '''
        self.installmentDesc = self.Qline_descInstallment.text().strip()
        self.password = self.Qdate_from.text().strip()
        self.branch = self.CMB_branch.currentText()
        self.fullName = self.LE_fullName.text().strip()
        self.hrId = self.LE_hrId.text().strip()
        self.userType = self.CMB_userType.currentText()
        self.status = self.CMB_userStatus.currentText()

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(cast(USER_ID  AS UNSIGNED)) FROM SYS_USER")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if self.name == '' or self.password =='' or self.fullName == ''  or self.hrId == '' :
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )

        else:

            sql = "INSERT INTO SYS_USER (USER_ID, BRANCH_NO, USER_NAME, USER_PASSWORD, USER_FULLNAME, USER_HR_ID, USER_CREATED_ON, USER_CREATED_BY, USER_CHANGED_ON, USER_CHENGED_BY,USER_STATUS, USER_TYPE_ID)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (
            self.id, self.branch, self.name, self.password, self.fullName, self.hrId, creationDate, CL_userModule.user_name , '', '', self.status,
            self.userType)
            mycursor.execute(sql, val)
            # mycursor.execute(sql)
            print(CL_userModule.user_name)
            mycursor.close()

            print(mycursor.rowcount, "record inserted.")
            db1.connectionCommit( self.conn )
            db1.connectionClose(self.conn)
            self.close()
    '''
    def FN_LOAD_COPY(self):
        filename = self.dirname + '/copyUser.ui'
        loadUi( filename, self )

        records = self.FN_GET_USERS()
        for row in records:
            self.CMB_userName.addItems( [row[0]] )
            self.CMB_userName1.addItems( [row[0]] )

        self.BTN_copyUser.clicked.connect(self.FN_COPY_USER)
        self.CMB_userName.currentIndexChanged.connect( self.FN_ASSIGN_ID )
        self.CMB_userName1.currentIndexChanged.connect(self.FN_ASSIGN_ID)
        self.FN_ASSIGN_ID()

    def FN_ASSIGN_ID (self):
        self.user1 = self.CMB_userName.currentText()
        self.user2 = self.CMB_userName1.currentText()
        self.LB_userID.setText( self.FN_GET_USERID_N( self.user1 ) )
        self.LB_userID2.setText( self.FN_GET_USERID_N( self.user2 ) )
    def FN_COPY_USER(self):
        newUser=  self.LB_userID2.text()

        if self.user1 == self.user2 :
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter 2 different users" )
        else:
            mycursor = self.conn.cursor()
            mycursor1 = self.conn.cursor()
            mycursor2 = self.conn.cursor()

            sql_select_query = "select ur.ROLE_ID ,ur.BRANCH_NO ,ur.UR_STATUS  " \
                               "from SYS_USER_ROLE  ur  inner join SYS_USER u ON u.USER_ID = ur.USER_ID  " \
                               "where  u.USER_NAME = %s "
            x = (self.user1,)
            mycursor.execute( sql_select_query, x )
            records = mycursor.fetchall()
            #delete current assignment if found
            mycursor2 = self.conn.cursor()
            sql_select_query1 = "delete from SYS_USER_ROLE where USER_ID = '" + newUser + "'"
            mycursor2.execute( sql_select_query1 )
            db1.connectionCommit( self.conn )

            mycursor1.execute( "SELECT max(cast(UR_USER_ROLE_ID  AS UNSIGNED)) FROM SYS_USER_ROLE" )
            myresult = mycursor1.fetchone()

            creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
            id = int( myresult[0] ) + 1
            for row in records:

                mycursor3 = self.conn.cursor()
                # sql = " INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS) VALUES ( "+id+", "+newUser+", "+row[0]+", '"+row[1]+"','"+CL_userModule.user_name+"', '"+creationDate+"',' ',' ' ,'"+row[2]+"')"
                sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
                      "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"

                val = (id, newUser, row[0], row[1], '', creationDate, '', '', row[2])
                print( str( sql ) )
                # val = (id,newUser,  row[0], row[1], CL_userModule.user_name, creationDate, '', '', row[2],)
                mycursor3.execute( sql, val )

                db1.connectionCommit( self.conn )
                print( mycursor3.rowcount, "record inserted." )
                id = id + 1

                # sql_select_query = "select * from SYS_USER_ROLE where USER_ID ='"+newUser+"' and ROLE_ID = '"+row[0]+"'"
                # print(sql_select_query)
                #
                # mycursor2.execute( sql_select_query)
                # print("mycursor2.rowcount is "+ str(mycursor2.rowcount))
                # if mycursor2.rowcount > 0:
                #     print("h")
                # else:
                #     mycursor3 = self.conn.cursor()
                #     #sql = " INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS) VALUES ( "+id+", "+newUser+", "+row[0]+", '"+row[1]+"','"+CL_userModule.user_name+"', '"+creationDate+"',' ',' ' ,'"+row[2]+"')"
                #     sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
                #           "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"
                #
                #     val = (id, newUser,row[0], row[1], '', creationDate, '', '', row[2])
                #     print(str(sql))
                #     #val = (id,newUser,  row[0], row[1], CL_userModule.user_name, creationDate, '', '', row[2],)
                #     mycursor3.execute( sql, val)
                #
                #
                #     db1.connectionCommit( self.conn )
                #     print( mycursor3.rowcount, "record inserted." )
                #     id = id + 1
            mycursor2.close()
            mycursor1.close()
            mycursor.close()
            self.close()

    def FN_GET_USER(self):
        user = self.CMB_userName.currentText()

        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_USER where user_name = %s"
        x = (user,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        self.LB_userID.setText( record[0] )
        self.LE_name.setText(record[2])
        self.LE_fullName.setText(record[4])
        self.LE_hrId.setText(record[5])
        self.CMB_branch.setCurrentText(record[1])
        self.CMB_userType.setCurrentText(record[11])
        self.CMB_userStatus.setCurrentText(record[10])


        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_USER(self):
        self.id = self.LB_userID.text()
        self.name = self.LE_name.text().strip()
        self.password = self.LE_password.text().strip
        self.branch = self.CMB_branch.currentText()
        self.fullName = self.LE_fullName.text().strip()
        self.hrId = self.LE_hrId.text().strip()
        self.userType = self.CMB_userType.currentText()
        self.status = self.CMB_userStatus.currentText()
        if self.name == '' or self.password =='' or self.fullName == ''  or self.hrId == '' :
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )
        else:
            mycursor = self.conn.cursor()

            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            sql = "UPDATE SYS_USER   set USER_NAME= %s ,  USER_PASSWORD= %s  ,  BRANCH_NO = %s, USER_FULLNAME = %s , USER_HR_ID = %s, USER_CHANGED_ON = %s , USER_CHENGED_BY = %s, USER_STATUS = %s, USER_TYPE_ID = %s where USER_id= %s "
            val = (self.name  , self.password, self.branch, self.fullName,self.hrId, changeDate, CL_userModule.user_name , self.status, self.userType , self.id)
            print(val)
            mycursor.execute(sql, val)

            mycursor.close()
            db1.connectionCommit( self.conn )
            print(mycursor.rowcount, "record Modified.")
            db1.connectionClose( self.conn )
            self.close()

    def FN_GET_USERS(self):

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT USER_NAME USER_ID FROM SYS_USER order by USER_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        return  records
    # def FN_GET_USERID(self):
    #     self.user = self.CMB_userName.currentText()
    #     mycursor = self.conn.cursor()
    #     sql_select_query= "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s "
    #     x = (self.user,)
    #     mycursor.execute(sql_select_query, x)
    #     myresult = mycursor.fetchone()
    #     self.LB_userID.setText(myresult [0])

    def FN_GET_USERID_N(self,user):

        mycursor = self.conn.cursor()
        sql_select_query= "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s "
        x = (user,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        return myresult[0]


    def FN_RESET_USER(self):
        mycursor = self.conn.cursor()

        changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
        if self.LE_password.text()  == self.LE_password2.text() :

            sql = "UPDATE SYS_USER   set   USER_PASSWORD= %s  , USER_CHANGED_ON = %s , USER_CHENGED_BY = %s where USER_NAME= %s "
            val = ( self.LE_password.text(), changeDate, CL_userModule.user_name,CL_userModule.user_name)
            #print( val )
            mycursor.execute( sql, val )
            mycursor.close()
            db1.connectionCommit( self.conn )
            print( mycursor.rowcount, "password changed" )
            db1.connectionClose( self.conn )
            self.close()
        else:
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter 2 different Passwords" )


    def FN_LOAD_RESET(self):
        filename = self.dirname + '/resetUserPassword.ui'
        loadUi( filename, self )
        self.BTN_resetPass.clicked.connect(self.FN_RESET_USER)
"""