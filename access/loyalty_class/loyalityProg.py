from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from mysql.connector import Error
import xlrd
from datetime import datetime
import xlwt.Workbook

class CL_loyProg(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    def __init__(self):
        super(CL_loyProg, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    def onClicked(self):
        #radioButton = self.sender()
        #print(radioButton.name)
        if self.Qradio_barcode.isChecked ():
            self.Qline_barcode.setEnabled(True)
            self.CMB_department.setEnabled(False)
            self.CMB_section.setEnabled(False)
            self.CMB_level4.setEnabled(False)

        elif self.Qradio_bmc.isChecked ():
            self.Qline_barcode.setEnabled(False)
            self.CMB_department.setEnabled(True)
            self.CMB_section.setEnabled(True)
            self.CMB_level4.setEnabled(True)


    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/createModifyLoyalityProg.ui'
        loadUi(filename, self)
        mycursor = self.conn.cursor()

        self.Qradio_barcode.clicked.connect(self.onClicked)
        self.Qradio_bmc.clicked.connect(self.onClicked)
        self.Qradio_bmc.setChecked(True)
        self.Qradio_active.setChecked(True)
        self.FN_GET_BRANCHES()
        self.FN_GET_COMPANIES()
        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()
    #
        self.FN_GET_DEPARTMENTS()
        self.FN_GET_SECTIONS()
        self.FN_GET_LEVEL4()
    # #     #check authorization
        print(CL_userModule.myList)
        for row_number, row_data in enumerate( CL_userModule.myList ):
           if  row_data[1] =='Display_Loyality':
               if row_data[4] =='None':
                print('hh')
               else:
                   sql_select_query = "select  i.ITEM_DESC from SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                   x = (row_data[4],)
                   mycursor.execute(sql_select_query, x)

                   result = mycursor.fetchone()
                   print(result)
                   if result[0] == 'create' :
                        self.Qbtn_create.setEnabled(True)
                        self.Qbtn_create.clicked.connect(self.FN_CREATE_LOYPROG)
                   elif result[0] == 'modify':
                        self.Qbtn_modify.setEnabled(True)
                        self.Qbtn_modify.clicked.connect(self.FN_MODIFY_LOYPROG)
                   elif result[0] == 'upload':
                        self.Qbtn_upload.setEnabled(True)
                        self.Qbtn_upload.clicked.connect(self.FN_UPLOAD_LOYPROG)


    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadLoyalityProg.ui'
        loadUi( filename, self )
        self.BTN_browse.clicked.connect( self.openFileNameDialog )
    #
    #
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName( self, "QFileDialog.getOpenFileName()", "",
                                                   " Files (*.xlsx)", options=options )
        if fileName:
            self.LE_fileName.setText(fileName)
            wb = xlrd.open_workbook( fileName )
            sheet = wb.sheet_by_index( 0 )
            mycursor = self.conn.cursor()
            errorMsg =''
            createdCust =0
            nonCreatedCust=0

            for i in range( sheet.nrows ):

                self.name = sheet.cell_value( i, 0 )
                self.custGroup = int(sheet.cell_value( i, 1 ))
                self.loyalityType = int(sheet.cell_value( i, 2 ))
                self.phone = int(sheet.cell_value( i, 3))
                self.mobile = int(sheet.cell_value( i, 4))
                self.job = sheet.cell_value( i, 5)
                self.address = sheet.cell_value( i, 6)
                self.city = sheet.cell_value( i, 7 )
                self.district = sheet.cell_value( i, 8 )
                self.building = sheet.cell_value( i, 9 )
                self.LE_floor = int(sheet.cell_value( i, 10 ))
                self.email = sheet.cell_value( i, 11 )
                self.company = sheet.cell_value( i, 12 )
                self.workPhone = int(sheet.cell_value( i, 13 ))
                self.workAddress = sheet.cell_value( i, 14 )
                self.status = int (sheet.cell_value( i, 15 ) )
                self.notes = sheet.cell_value( i, 16 )
                if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.city == '' or self.district == '' or self.building == '' \
                        or self.email == '':
                    nonCreatedCust=nonCreatedCust+1

                else:
                # get max userid
                    mycursor.execute( "SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM POS_CUSTOMER" )
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        self.id = "1"
                    else:
                        self.id = int( myresult[0] ) + 1

                    creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
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
                    #print(val)
                    mycursor.execute( sql, val )
                    createdCust=createdCust+1
                    db1.connectionCommit( self.conn )
            mycursor.close()
            db1.connectionClose( self.conn )
            #QtWidgets.QMessageBox.warning( self, "Information", "No of created user ",counter)
            self.msgBox = QMessageBox()

            # Set the various texts
            self.msgBox.setWindowTitle( "Information" )
            self.msgBox.setStandardButtons( QMessageBox.Ok)
            self.msgBox.setText("No of created Cust '"+str(createdCust) +"'  No of non created Cust '"+str(nonCreatedCust)+"'")
            self.msgBox.show()
            self.close()

    def FN_UPLOAD_LOYPROG(self, funct):
        self.window_two = CL_loyProg()
        self.window_two.FN_LOAD_UPLOAD()
        self.window_two.show()
    # endregion
    def FN_GET_BRANCHES(self):
        mycursor = self.conn.cursor()
        self.company = self.CMB_company.currentText()
        mycursor.execute("SELECT COMPANY_ID FROM COMPANY where COMPANY_DESC = '" + self.company + "'")
        myresult = mycursor.fetchone()
        self.companyId = myresult[0]


        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM BRANCH where BRANCH_STATUS   = 1 and COMPANY_ID = '"+self.companyId+"'"
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_branch.addItems( [row[0]] )
        mycursor.close()

    def FN_GET_COMPANIES(self):
        mycursor = self.conn.cursor()
        self.CMB_company.clear()
        sql_select_query = "SELECT COMPANY_DESC  FROM COMPANY where COMPANY_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_company.addItems( [row[0]] )
        mycursor.close()

    def FN_GET_DEPARTMENTS(self):
        mycursor = self.conn.cursor()
        self.CMB_department.clear()
        sql_select_query = "SELECT DEPARTMENT_DESC FROM DEPARTMENT where DEPARTMENT_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_department.addItems( [row[0]] )
        mycursor.close()

    def FN_GET_SECTIONS(self):
        mycursor = self.conn.cursor()
        self.CMB_section.clear()
        sql_select_query = "SELECT SECTION_DESC  FROM SECTION where SECTION_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_section.addItems( [row[0]] )
        mycursor.close()

    def FN_GET_LEVEL4(self):
        mycursor = self.conn.cursor()
        self.CMB_level4.clear()
        sql_select_query = "SELECT BMC_LEVEL4_DESC  FROM BMC_LEVEL4 where BMC_LEVEL4_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_level4.addItems( [row[0]] )
        mycursor.close()


    def FN_GET_CUSTGP(self):
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT CG_DESC FROM CUSTOMER_GROUP order by CG_GROUP_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.CMB_custGroup.addItems( [row[0]] )

    def FN_GET_CUSTTP(self):
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT LOYCT_DESC FROM LOYALITY_CUSTOMER_TYPE order by LOYCT_TYPE_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.CMB_loyalityType.addItems( [row[0]] )

    def FN_GET_CUSTTP_ID(self,desc):
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+desc+"'" )
        records = mycursor.fetchone()
        mycursor.close()
        return records[0]
    def FN_CREATE_LOYPROG(self):
        #get customer data
        # check validation
        print('pt1')
        self.name = self.Qline_name.text().strip()
        self.desc = self.Qtext_desc.toPlainText().strip()
        self.date_from =self.Qdate_from.dateTime().toString('yyyy-MM-dd')
        self.date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')

        print('pt2')
        self.company = self.CMB_company.currentText()
        self.branch = self.CMB_branch.currentText()
        self.department = self.CMB_department.currentText()
        self.section = self.CMB_section.currentText()
        self.level4 = self.CMB_level4.currentText()
        self.barcode = self.Qline_barcode.text().strip()
        print('pt3')
        self.purchAmount = self.Qline_purchAmount.text().strip()
        self.points = self.Qline_points.text().strip()

        print('pt4')
        self.custGroup = self.CMB_custGroup.currentText()
        self.loyalityType =self.CMB_loyalityType.currentText()

        if self.Qradio_active.isChecked():
             self.status = 1
        else :
              self.status = 0


        mycursor = self.conn.cursor()
        # get max id
        mycursor.execute( "SELECT max(cast(LOY_PROGRAM_ID AS UNSIGNED)) FROM LOYALITY_PROGRAM" )
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int( myresult[0] ) + 1

        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

        # get branch
        sql="SELECT BRANCH_NO FROM BRANCH where BRANCH_DESC_A = '" + self.branch + "'"
        print(sql)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        self.branch= myresult[0]

        # get COMPANY

        mycursor.execute("SELECT COMPANY_ID FROM COMPANY where COMPANY_DESC = '" + self.company + "'")
        myresult = mycursor.fetchone()
        self.company = myresult[0]

        # get department
        mycursor.execute("SELECT DEPARTMENT_ID FROM DEPARTMENT where DEPARTMENT_DESC = '" + self.department + "'")
        myresult = mycursor.fetchone()
        self.department = myresult[0]

        # get sECTION
        # mycursor.execute("SELECT SECTION_ID FROM branch where SECTION_DESC = '" + self.section + "'")
        # myresult = mycursor.fetchone()
        # self.section = myresult[0]
        #
        # # get BMC_LEVEL4
        # mycursor.execute("SELECT BMC_LEVEL4_ID FROM BMC_LEVEL4 where BMC_LEVEL4_DESC = '" + self.level4 + "'")
        # myresult = mycursor.fetchone()
        # self.level4 = myresult[0]

        #get customer gp id
        mycursor.execute( "SELECT CG_GROUP_ID FROM CUSTOMER_GROUP where CG_DESC = '"+self.custGroup+"'" )
        myresult = mycursor.fetchone()
        self.custGroup = myresult[0]

        #get customer type
        mycursor.execute( "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+self.loyalityType +"'" )
        myresult = mycursor.fetchone()
        self.loyalityType = myresult[0]


        if self.name == '' or self.desc == '' or self.purchAmount  == '' or self.points== '' or self.date_from == '' or self.date_to== '' \
                 :
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter all required fields" )

        else:
            try:
                sql = "INSERT INTO LOYALITY_PROGRAM (LOY_PROGRAM_ID,COPMAPNY_ID," \
                      "BRANCH_NO,CG_GROUP_ID,BMC_ID,POS_GTIN,LOY_NAME,LOY_DESC,LOY_CREATED_ON,LOY_CREATED_BY," \
                      "LOY_VALID_FROM,LOY_VALID_TO,LOY_VALUE,LOY_POINTS,LOYCT_TYPE_ID,LOY_STATUS)" \
                      "values (%s, %s, %s,  %s,%s,%s, %s, %s, %s, %s,%s, %s, %s,  %s,  %s,  %s)"

                           # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                val = (self.id,self.company,self.branch,self.custGroup,'',self.barcode,self.name,
                       self.desc, creationDate, CL_userModule.user_name,  self.date_from,self.date_to,
                       self.purchAmount,self.points,self.loyalityType,self.status            )
                mycursor.execute( sql, val )
            except (Error, Warning) as e:
                print(e)
            # mycursor.execute(sql)

            mycursor.close()

            print( mycursor.rowcount, "record inserted." )
            db1.connectionCommit( self.conn )
            db1.connectionClose( self.conn )
            QtWidgets.QMessageBox.information(self, "Success", "program is created successfully")

            self.close()


    def FN_MODIFY_LOYPROG(self):

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

        changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
        # get customer gp id
        mycursor.execute( "SELECT CG_GROUP_ID FROM CUSTOMER_GROUP where CG_DESC = '" + self.custGroup + "'" )
        myresult = mycursor.fetchone()
        self.custGroup = myresult[0]

        # get customer type
        mycursor.execute(
            "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + self.loyalityType + "'" )
        myresult = mycursor.fetchone()
        self.loyalityType = myresult[0]

        self.status = self.CMB_status.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0

        if  self.lE_mobile == '' or self.LE_job == '' or self.LE_address == '' or self.LE_city == '' or self.LE_district == '' or self.LE_building == '' \
                or self.LE_floor == '' or self.LE_email == '':
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter all required fields" )

        else:

            sql = "update  POS_CUSTOMER  set  LOYCT_TYPE_ID=%s, CG_GROUP_ID=%s,   POSC_PHONE=%s," \
                  " POSC_MOBILE=%s, POSC_JOB=%s, POSC_ADDRESS=%s, POSC_CITY=%s, POSC_DISTICT=%s, POSC_BUILDING=%s,POSC_FLOOR=%s, POSC_EMAIL=%s, " \
                  "POSC_CHANGED_BY =%s, POSC_CHANGED_ON =%s, POSC_COMPANY=%s, " \
                  "POSC_WORK_PHONE=%s, POSC_WORK_ADDRESS=%s, POSC_NOTES=%s, POSC_STATUS=%s where POSC_CUST_ID = %s"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = ( self.loyalityType, self.custGroup,  self.phone, self.mobile,
                   self.job, self.address, self.city, self.district, self.building, self.LE_floor ,self.email,
                   CL_userModule.user_name, changeDate,  self.company, self.workPhone, self.workAddress,
                   self.notes, self.status ,self.id  )
            mycursor.execute( sql, val )
            # mycursor.execute(sql)

            mycursor.close()

            print( mycursor.rowcount, "record updated." )
            QtWidgets.QMessageBox.information(self, "Success", "Customer is modified successfully")

            db1.connectionCommit( self.conn )
            db1.connectionClose( self.conn )
            self.close()

        print( "in modify cust", self.CMB_custName )
