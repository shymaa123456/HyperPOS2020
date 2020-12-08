from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import xlrd
from datetime import datetime
import xlwt.Workbook


class CL_loyProg(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''

    def __init__(self):
        super(CL_loyProg, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    # # region Description
    # def onClickedCheckBox(self):
    #     if self.chk_search_other.isChecked():
    #         #self.Rbtn_custNo.setEnabled(True)
    #         self.Rbtn_custNo.setChecked(True)
    #         self.LE_custNo.setEnabled(True)
    #     else:
    #         self.Rbtn_custNo.setChecked(False)
    #         self.LE_custNo.setEnabled(False)
    #
    #     if self.chk_search_status.isChecked():
    #         #self.Rbtn_stsAll.setEnabled(True)
    #         self.Rbtn_stsAll.setChecked(True)
    #     else :
    #         self.Rbtn_stsAll.setChecked(False)
    def onClicked(self):
        # radioButton = self.sender()
        # print(radioButton.name)
        if self.Qradio_barcode.isChecked():
            self.Qline_barcode.setEnabled(True)
            self.Qcombo_departement.setEnabled(False)
            self.Qcombo_section.setEnabled(False)
            self.Qcombo_level4.setEnabled(False)

        elif self.Qradio_bmc.isChecked():
            self.Qline_barcode.setEnabled(False)
            self.Qcombo_departement.setEnabled(True)
            self.Qcombo_section.setEnabled(True)
            self.Qcombo_level4.setEnabled(True)

    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/createModifyLoyalityProg.ui'
        loadUi(filename, self)
        mycursor = self.conn.cursor()
        # self.Qbtn_create.clicked.connect(self.FN_CREATE_LOYPROG)
        # self.Qbtn_modify.clicked.connect(self.FN_MODIFY_LOYPROG)
        # self.Qbtn_upload.clicked.connect(self.FN_UPLOAD_LOYPROG)
        self.Qradio_barcode.clicked.connect(self.onClicked)
        self.Qradio_bmc.clicked.connect(self.onClicked)

        self.FN_GET_BRANCHES()
        self.FN_GET_COMPANIES()
        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()

        self.FN_GET_DEPARTMENTS()
        self.FN_GET_SECTIONS()
        self.FN_GET_LEVEL4()
        #     #check authorization
        for row_number, row_data in enumerate(CL_userModule.myList):
            if row_data[1] == 'Display_Loyality':
                if row_data[4] == 'None':
                    print('hh')
                else:
                    sql_select_query = "select  i.ITEM_DESC from SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                    x = (row_data[4],)
                    mycursor.execute(sql_select_query, x)
                    result = mycursor.fetchone()
                    if result[0] == 'create':
                        self.Qbtn_create.clicked.connect(self.FN_CREATE_CUST)
                    elif result[0] == 'modify':
                        self.Qbtn_modify.clicked.connect(self.FN_LOAD_MODIFY)
                    elif result[0] == 'upload':
                        self.Qbtn_upload.clicked.connect(self.FN_UP_CUST)

    # def FN_SAVE_CUST(self):
    #
    #     filename = QFileDialog.getSaveFileName(self, "Save File", '', "(*.xls)")
    #     print(filename)
    #
    #     wb = xlwt.Workbook()
    #
    #     # add_sheet is used to create sheet.
    #     sheet = wb.add_sheet('Sheet 1')
    #
    #     for currentColumn in range(self.Qtable_customer.columnCount()):
    #         for currentRow in range(self.Qtable_customer.rowCount()):
    #             teext = str(self.Qtable_customer.item(currentRow, currentColumn).text())
    #             sheet.write(currentRow, currentColumn, teext)
    #     #wb.save('test11.xls')
    #     wb.save( str(filename[0]))
    #     wb.close()
    # def FN_SEARCH_CUST(self):
    #     print('in search')
    #     #self.Qtable_customer.clearcontents()
    #     for i in reversed(range(self.Qtable_customer.rowCount())):
    #         self.Qtable_customer.removeRow(i)
    #
    #
    #     mycursor = self.conn.cursor()
    #     whereClause =""
    #     if self.chk_search_other.isChecked():
    #         if self.Rbtn_custNo.isChecked ():
    #             id= self.LE_custNo.text()
    #             whereClause=" POSC_CUST_ID = '"+id+"'"
    #
    #         elif self.Rbtn_custTp .isChecked ():
    #             type= self.CMB_loyalityType.currentText()
    #             whereClause = " LOYCT_TYPE_ID ='" + self.FN_GET_CUSTTP_ID(type) + "'"
    #
    #         elif self.Rbtn_custPhone.isChecked():
    #             phone = self.LE_custPhone.text()
    #             whereClause = " POSC_PHONE = '"+phone+"'"
    #
    #     if self.chk_search_status.isChecked():
    #         if self.Rbtn_stsActive.isChecked():
    #             if whereClause != '':
    #                 whereClause = whereClause + ' and '
    #             whereClause = whereClause + 'POSC_STATUS = 1'
    #         elif  self.Rbtn_stsInactive.isChecked():
    #             if whereClause != '':
    #                 whereClause = whereClause + ' and '
    #             whereClause = whereClause + 'POSC_STATUS = 0'
    #         elif  self.Rbtn_stsAll.isChecked():
    #             if whereClause != '':
    #                 whereClause = whereClause + ' and '
    #             whereClause = whereClause + 'POSC_STATUS in ( 0,1)'
    #     if self.chk_search_status.isChecked()==False and  self.chk_search_other.isChecked()==False:
    #         QtWidgets.QMessageBox.warning(self, "Error", "أختر أي من محدادات البحث")
    #     else:
    #         print(whereClause)
    #         sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from POS_CUSTOMER where "+ whereClause
    #         print(sql_select_query)
    #         mycursor.execute(sql_select_query)
    #         records = mycursor.fetchall()
    #         for row_number, row_data in enumerate( records ):
    #             self.Qtable_customer.insertRow( row_number )
    #
    #             for column_number, data in enumerate( row_data ):
    #                 self.Qtable_customer.setItem( row_number, column_number, QTableWidgetItem( str( data ) ) )
    #         self.Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    #
    #         mycursor.close()
    #

    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadLoyalityProg.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.openFileNameDialog)

    #
    #
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  " Files (*.xlsx)", options=options)
        if fileName:
            self.LE_fileName.setText(fileName)
            wb = xlrd.open_workbook(fileName)
            sheet = wb.sheet_by_index(0)
            mycursor = self.conn.cursor()
            errorMsg = ''
            createdCust = 0
            nonCreatedCust = 0

            for i in range(sheet.nrows):

                self.name = sheet.cell_value(i, 0)
                self.custGroup = int(sheet.cell_value(i, 1))
                self.loyalityType = int(sheet.cell_value(i, 2))
                self.phone = int(sheet.cell_value(i, 3))
                self.mobile = int(sheet.cell_value(i, 4))
                self.job = sheet.cell_value(i, 5)
                self.address = sheet.cell_value(i, 6)
                self.city = sheet.cell_value(i, 7)
                self.district = sheet.cell_value(i, 8)
                self.building = sheet.cell_value(i, 9)
                self.LE_floor = int(sheet.cell_value(i, 10))
                self.email = sheet.cell_value(i, 11)
                self.company = sheet.cell_value(i, 12)
                self.workPhone = int(sheet.cell_value(i, 13))
                self.workAddress = sheet.cell_value(i, 14)
                self.status = int(sheet.cell_value(i, 15))
                self.notes = sheet.cell_value(i, 16)
                if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.city == '' or self.district == '' or self.building == '' \
                        or self.email == '':
                    nonCreatedCust = nonCreatedCust + 1

                else:
                    # get max userid
                    mycursor.execute("SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM POS_CUSTOMER")
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        self.id = "1"
                    else:
                        self.id = int(myresult[0]) + 1

                    creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "INSERT INTO POS_CUSTOMER(POSC_CUST_ID, LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                          " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                          "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                          "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS) " \
                          "         VALUES ( %s, %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                          "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s)"

                    # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                    val = (self.id, self.loyalityType, self.custGroup, self.name, self.phone, self.mobile,
                           self.job, self.address, self.city, self.district, self.building, self.LE_floor, self.email,
                           CL_userModule.user_name, creationDate, ' ', self.company, self.workPhone, self.workAddress,
                           self.notes, self.status
                           )
                    # print(val)
                    mycursor.execute(sql, val)
                    createdCust = createdCust + 1
                    db1.connectionCommit(self.conn)
            mycursor.close()
            db1.connectionClose(self.conn)
            # QtWidgets.QMessageBox.warning( self, "Information", "No of created user ",counter)
            self.msgBox = QMessageBox()

            # Set the various texts
            self.msgBox.setWindowTitle("Information")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.setText(
                "No of created Cust '" + str(createdCust) + "'  No of non created Cust '" + str(nonCreatedCust) + "'")
            self.msgBox.show()
            self.close()

    #     #Extracting number of rows
    #
    #
    #
    #
    # def FN_GET_CUSTOMERS(self):
    #
    #     mycursor = self.conn.cursor()
    #     mycursor.execute( "SELECT POSC_NAME  FROM POS_CUSTOMER  order by POSC_CUST_ID  asc" )
    #     records = mycursor.fetchall()
    #     for row in records:
    #         self.CMB_custName.addItems( [row[0]] )
    #     mycursor.close()
    #     #print(records)
    # def FN_GET_CUST(self):
    #     self.FN_GET_CustID()
    #
    #     self.id = self.LB_custID.text()
    #     mycursor = self.conn.cursor()
    #     sql_select_query = "select * from POS_CUSTOMER where POSC_CUST_ID = %s "
    #     x = (self.id,)
    #     mycursor.execute( sql_select_query, x )
    #     record = mycursor.fetchone()
    #     #print( record )
    #     self.lE_phone.setText( record[4] )
    #     self.lE_mobile.setText( record[5] )
    #     self.LE_job.setText( record[6] )
    #     self.LE_address.setText( record[7] )
    #     self.LE_city.setText( record[8] )
    #     self.LE_district.setText( record[9] )
    #     self.LE_building.setText( record[10] )
    #     self.LE_floor.setText( record[11] )
    #     self.LE_email.setText( record[12] )
    #     self.LE_company.setText( record[17] )
    #     self.LE_workPhone.setText( record[18] )
    #     self.LE_workAddress.setText( record[19] )
    #     self.LE_notes.setText( record[20] )
    #     if record[21] == '1':
    #         self.CMB_status.setCurrentText('Active')
    #     else:
    #         self.CMB_status.setCurrentText( 'Inactive' )
    #
    #     #self.CMB_status.setCurrentText( record[21] )
    #
    #     self.CMB_custGroup.setCurrentText( record[2] )
    #     self.CMB_loyalityType.setCurrentText( record[1] )
    #     mycursor.close()
    #
    # def FN_GET_CUSTSTATUS(self):
    #     self.FN_GET_CustID()
    #
    #     self.id = self.LB_custID.text()
    #     mycursor = self.conn.cursor()
    #     sql_select_query = "select POSC_STATUS from POS_CUSTOMER where POSC_CUST_ID = %s "
    #     x = (self.id,)
    #     mycursor.execute( sql_select_query, x )
    #     record = mycursor.fetchone()
    #     #print( record )
    #
    #     if record[0] == '1':
    #         self.CMB_status.setCurrentText('Active')
    #     else:
    #         self.CMB_status.setCurrentText( 'Inactive' )
    #
    #     mycursor.close()
    #
    #
    # def FN_GET_CustID(self):
    #     self.cust = self.CMB_custName.currentText()
    #     mycursor = self.conn.cursor()
    #     sql_select_query = "SELECT POSC_CUST_ID  FROM POS_CUSTOMER  WHERE POSC_NAME = %s  "
    #     x = (self.cust,)
    #     mycursor.execute( sql_select_query, x )
    #
    #     myresult = mycursor.fetchone()
    #     self.LB_custID.setText( myresult[0] )
    #     mycursor.close()

    def FN_UP_CUST(self, funct):
        self.window_two = CL_loyProg()
        self.window_two.FN_LOAD_UPLOAD()
        self.window_two.show()

    # endregion
    def FN_GET_BRANCHES(self):
        mycursor = self.conn.cursor()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_branch.addItems([row[0]])
        mycursor.close()

    def FN_GET_COMPANIES(self):
        mycursor = self.conn.cursor()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_branch.addItems([row[0]])
        mycursor.close()

    def FN_GET_DEPARTMENTS(self):
        mycursor = self.conn.cursor()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_branch.addItems([row[0]])
        mycursor.close()

    def FN_GET_SECTIONS(self):
        mycursor = self.conn.cursor()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_branch.addItems([row[0]])
        mycursor.close()

    def FN_GET_LEVEL4(self):
        mycursor = self.conn.cursor()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_branch.addItems([row[0]])
        mycursor.close()

    def FN_GET_CUSTGP(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT CG_DESC FROM CUSTOMER_GROUP order by CG_GROUP_ID asc")
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.CMB_custGroup.addItems([row[0]])

    def FN_GET_CUSTTP(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC FROM LOYALITY_CUSTOMER_TYPE order by LOYCT_TYPE_ID asc")
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.CMB_loyalityType.addItems([row[0]])

    def FN_GET_CUSTTP_ID(self, desc):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + desc + "'")
        records = mycursor.fetchone()
        mycursor.close()
        return records[0]

    def FN_CREATE_CUST(self):
        # get customer data

        self.name = self.LE_name.text().strip()
        self.custGroup = self.CMB_custGroup.currentText()
        self.loyalityType = self.CMB_loyalityType.currentText()
        self.phone = self.lE_phone.text().strip()
        self.mobile = self.lE_mobile.text().strip()
        self.job = self.LE_job.text().strip()
        self.address = self.LE_address.text().strip()
        self.city = self.LE_city.text().strip()
        self.district = self.LE_district.text().strip()
        self.building = self.LE_building.text().strip()
        self.LE_floor = self.LE_floor.text().strip()
        self.email = self.LE_email.text().strip()
        self.company = self.LE_company.text().strip()
        self.workPhone = self.LE_workPhone.text().strip()
        self.workAddress = self.LE_workAddress.text().strip()
        self.status = self.CMB_status.currentText()
        self.notes = self.LE_notes.text().strip()

        mycursor = self.conn.cursor()
        # get max id
        mycursor.execute("SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM POS_CUSTOMER")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        # get customer gp id
        mycursor.execute("SELECT CG_GROUP_ID FROM CUSTOMER_GROUP where CG_DESC = '" + self.custGroup + "'")
        myresult = mycursor.fetchone()
        self.custGroup = myresult[0]

        # get customer type
        mycursor.execute(
            "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + self.loyalityType + "'")
        myresult = mycursor.fetchone()
        self.loyalityType = myresult[0]

        self.status = self.CMB_status.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0
        if self.name == '' or self.lE_mobile == '' or self.LE_job == '' or self.LE_address == '' or self.LE_city == '' or self.LE_district == '' or self.LE_building == '' \
                or self.LE_floor == '' or self.LE_email == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        else:

            sql = "INSERT INTO POS_CUSTOMER(POSC_CUST_ID, LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                  " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                  "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                  "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS) " \
                  "         VALUES ( %s, %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                  "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id, self.loyalityType, self.custGroup, self.name, self.phone, self.mobile,
                   self.job, self.address, self.city, self.district, self.building, self.LE_floor, self.email,
                   CL_userModule.user_name, creationDate, ' ', self.company, self.workPhone, self.workAddress,
                   self.notes, self.status
                   )
            mycursor.execute(sql, val)
            # mycursor.execute(sql)

            mycursor.close()

            print(mycursor.rowcount, "record inserted.")
            db1.connectionCommit(self.conn)
            db1.connectionClose(self.conn)
            QtWidgets.QMessageBox.information(self, "Success", "Customer is created successfully")

            self.close()

        print("in create cust", self.name)

    def FN_DEACTIVATE_CUST(self):
        mycursor = self.conn.cursor()
        self.id = self.LB_custID.text().strip()
        self.status = self.CMB_status.currentText()
        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
        # get customer gp id
        mycursor.execute("SELECT CG_GROUP_ID FROM CUSTOMER_GROUP where CG_DESC = '" + self.custGroup + "'")
        myresult = mycursor.fetchone()
        self.custGroup = myresult[0]

        # get customer type
        mycursor.execute(
            "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + self.loyalityType + "'")
        myresult = mycursor.fetchone()
        self.loyalityType = myresult[0]

        self.status = self.CMB_status.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0

        sql = "update   POSC_STATUS=%s where POSC_CUST_ID = %s"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (self.status, self.id)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)

        mycursor.close()

        print(mycursor.rowcount, "customer deactivate.")
        db1.connectionCommit(self.conn)
        db1.connectionClose(self.conn)
        QtWidgets.QMessageBox.information(self, "Success", "Customer status changed successfully")

        self.close()

    def FN_MODIFY_CUST(self):

        self.id = self.LB_custID.text().strip()
        self.custGroup = self.CMB_custGroup.currentText()
        self.loyalityType = self.CMB_loyalityType.currentText()
        self.phone = self.lE_phone.text().strip()
        self.mobile = self.lE_mobile.text().strip()
        self.job = self.LE_job.text().strip()
        self.address = self.LE_address.text().strip()
        self.city = self.LE_city.text().strip()
        self.district = self.LE_district.text().strip()
        self.building = self.LE_building.text().strip()
        self.LE_floor = self.LE_floor.text().strip()
        self.email = self.LE_email.text().strip()
        self.company = self.LE_company.text().strip()
        self.workPhone = self.LE_workPhone.text().strip()
        self.workAddress = self.LE_workAddress.text().strip()
        self.status = self.CMB_status.currentText()
        self.notes = self.LE_notes.text().strip()

        mycursor = self.conn.cursor()

        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
        # get customer gp id
        mycursor.execute("SELECT CG_GROUP_ID FROM CUSTOMER_GROUP where CG_DESC = '" + self.custGroup + "'")
        myresult = mycursor.fetchone()
        self.custGroup = myresult[0]

        # get customer type
        mycursor.execute(
            "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + self.loyalityType + "'")
        myresult = mycursor.fetchone()
        self.loyalityType = myresult[0]

        self.status = self.CMB_status.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0

        if self.lE_mobile == '' or self.LE_job == '' or self.LE_address == '' or self.LE_city == '' or self.LE_district == '' or self.LE_building == '' \
                or self.LE_floor == '' or self.LE_email == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        else:

            sql = "update  POS_CUSTOMER  set  LOYCT_TYPE_ID=%s, CG_GROUP_ID=%s,   POSC_PHONE=%s," \
                  " POSC_MOBILE=%s, POSC_JOB=%s, POSC_ADDRESS=%s, POSC_CITY=%s, POSC_DISTICT=%s, POSC_BUILDING=%s,POSC_FLOOR=%s, POSC_EMAIL=%s, " \
                  "POSC_CHANGED_BY =%s, POSC_CHANGED_ON =%s, POSC_COMPANY=%s, " \
                  "POSC_WORK_PHONE=%s, POSC_WORK_ADDRESS=%s, POSC_NOTES=%s, POSC_STATUS=%s where POSC_CUST_ID = %s"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.loyalityType, self.custGroup, self.phone, self.mobile,
                   self.job, self.address, self.city, self.district, self.building, self.LE_floor, self.email,
                   CL_userModule.user_name, changeDate, self.company, self.workPhone, self.workAddress,
                   self.notes, self.status, self.id)
            mycursor.execute(sql, val)
            # mycursor.execute(sql)

            mycursor.close()

            print(mycursor.rowcount, "record updated.")
            QtWidgets.QMessageBox.information(self, "Success", "Customer is modified successfully")

            db1.connectionCommit(self.conn)
            db1.connectionClose(self.conn)
            self.close()

        print("in modify cust", self.CMB_custName)
