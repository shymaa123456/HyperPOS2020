from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator ,QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import xlrd
from datetime import datetime
class CL_customer(QtWidgets.QDialog):
    dirname = ''
    def __init__(self):
        super(CL_customer, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    def FN_LOAD_DEACTIVATE(self):
        filename = self.dirname + '/deactivateCustomer.ui'
        loadUi(filename, self)
        self.FN_GET_CUSTOMERS()
        self.FN_GET_CustID()
        self.FN_GET_CUSTSTATUS()
        self.BTN_deactivateCustomer.clicked.connect(self.FN_DEACTIVATE_CUST)
    def FN_LOAD_MODIFY(self):

        filename = self.dirname + '/modifyCustomer.ui'
        loadUi( filename, self )
        self.FN_GET_CUSTOMERS()
        self.FN_GET_CustID()
        self.FN_GET_CUST()
        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()
        self.CMB_custName.currentIndexChanged.connect( self.FN_GET_CUST )
        self.BTN_modifyCustomer.clicked.connect( self.FN_MODIFY_CUST )
        self.CMB_status.addItems( ["Active", "Inactive"] )
    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadCustomers.ui'
        loadUi( filename, self )
        self.BTN_browse.clicked.connect( self.openFileNameDialog )


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
        #Extracting number of rows



    def FN_GET_CUSTOMERS(self):

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT POSC_NAME  FROM POS_CUSTOMER  order by POSC_CUST_ID  asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_custName.addItems( [row[0]] )
        mycursor.close()
        #print(records)
    def FN_GET_CUST(self):
        self.FN_GET_CustID()

        self.id = self.LB_custID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "select * from POS_CUSTOMER where POSC_CUST_ID = %s "
        x = (self.id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()
        #print( record )
        self.lE_phone.setText( record[4] )
        self.lE_mobile.setText( record[5] )
        self.LE_job.setText( record[6] )
        self.LE_address.setText( record[7] )
        self.LE_city.setText( record[8] )
        self.LE_district.setText( record[9] )
        self.LE_building.setText( record[10] )
        self.LE_floor.setText( record[11] )
        self.LE_email.setText( record[12] )
        self.LE_company.setText( record[17] )
        self.LE_workPhone.setText( record[18] )
        self.LE_workAddress.setText( record[19] )
        self.LE_notes.setText( record[20] )
        if record[21] == '1':
            self.CMB_status.setCurrentText('Active')
        else:
            self.CMB_status.setCurrentText( 'Inactive' )

        #self.CMB_status.setCurrentText( record[21] )

        self.CMB_custGroup.setCurrentText( record[2] )
        self.CMB_loyalityType.setCurrentText( record[1] )
        mycursor.close()

    def FN_GET_CUSTSTATUS(self):
        self.FN_GET_CustID()

        self.id = self.LB_custID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "select POSC_STATUS from POS_CUSTOMER where POSC_CUST_ID = %s "
        x = (self.id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()
        #print( record )

        if record[0] == '1':
            self.CMB_status.setCurrentText('Active')
        else:
            self.CMB_status.setCurrentText( 'Inactive' )

        mycursor.close()


    def FN_GET_CustID(self):
        self.cust = self.CMB_custName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT POSC_CUST_ID  FROM POS_CUSTOMER  WHERE POSC_NAME = %s  "
        x = (self.cust,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        self.LB_custID.setText( myresult[0] )
        mycursor.close()



    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createCustomer.ui'
        loadUi( filename, self )
        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()
        self.CMB_status.addItems( ["Active", "Inactive"] )
        self.BTN_createCustomer.clicked.connect(self.FN_CREATE_CUST)


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

    def FN_CREATE_CUST(self):
        #get customer data

        self.name = self.LE_name.text().strip()
        self.custGroup = self.CMB_custGroup.currentText()
        self.loyalityType =self.CMB_loyalityType.currentText()
        self.phone = self.lE_phone .text().strip()
        self.mobile = self.lE_mobile.text().strip()
        self.job = self.LE_job.text().strip()
        self.address = self.LE_address.text().strip()
        self.city = self.LE_city.text().strip()
        self.district = self.LE_district.text().strip()
        self.building = self.LE_building.text().strip()
        self.LE_floor = self.LE_floor.text().strip()
        self.email = self.LE_email.text().strip()
        self.company = self.LE_company.text().strip()
        self.workPhone =  self.LE_workPhone.text().strip()
        self.workAddress = self.LE_workAddress.text().strip()
        self.status = self.CMB_status.currentText()
        self.notes = self.LE_notes.text().strip()

        mycursor = self.conn.cursor()
        # get max id
        mycursor.execute( "SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM POS_CUSTOMER" )
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int( myresult[0] ) + 1

        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

        #get customer gp id
        mycursor.execute( "SELECT CG_GROUP_ID FROM CUSTOMER_GROUP where CG_DESC = '"+self.custGroup+"'" )
        myresult = mycursor.fetchone()
        self.custGroup = myresult[0]

        #get customer type
        mycursor.execute( "SELECT LOYCT_TYPE_ID FROM LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+self.loyalityType +"'" )
        myresult = mycursor.fetchone()
        self.loyalityType = myresult[0]

        self.status = self.CMB_status.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0
        if self.name == '' or self.lE_mobile == '' or self.LE_job  == '' or self.LE_address== '' or self.LE_city == '' or self.LE_district== '' or self.LE_building  == '' \
                or self.LE_floor == '' or self.LE_email=='' :
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter all required fields" )

        else:

            sql = "INSERT INTO POS_CUSTOMER(POSC_CUST_ID, LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                  " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                  "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                  "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS) " \
                  "         VALUES ( %s, %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                  "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s)"

                       # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id,self.loyalityType,self.custGroup,self.name,self.phone,self.mobile,
                   self.job, self.address, self.city, self.district, self.building, self.LE_floor ,self.email,
                   CL_userModule.user_name, creationDate, ' ',self.company, self.workPhone, self.workAddress,
                   self.notes, self.status
            )
            mycursor.execute( sql, val )
            # mycursor.execute(sql)

            mycursor.close()

            print( mycursor.rowcount, "record inserted." )
            db1.connectionCommit( self.conn )
            db1.connectionClose( self.conn )
            QtWidgets.QMessageBox.information(self, "Success", "Customer is created successfully")

            self.close()

        print("in create cust" ,self.name)

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
        val = ( self.status, self.id)
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
