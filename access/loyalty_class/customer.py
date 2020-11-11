from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator ,QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime
class CL_customer(QtWidgets.QDialog):
    dirname = ''
    def __init__(self):
        super(CL_customer, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    def FN_LOAD_MODIFY(self):

        filename = self.dirname + '/modifyCustomer.ui'
        loadUi( filename, self )
        self.FN_GET_CUSTOMERS()
        self.FN_GET_CustID()
        self.FN_GET_CUST()
        self.CMB_custName.currentIndexChanged.connect( self.FN_GET_CUST )
        self.BTN_modifyCustomer.clicked.connect( self.FN_MODIFY_CUST )

    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadCustomers.ui'
        loadUi( filename, self )
        # self.FN_GET_CUSTOMERS()
        # self.FN_GET_CustID()
        # self.FN_GET_CUST()
        # self.CMB_custName.currentIndexChanged.connect( self.FN_GET_CUST )
        self.BTN_browse.clicked.connect( self.openFileNameDialog )


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName( self, "QFileDialog.getOpenFileName()", "",
                                                   " Files (*.csv)", options=options )
        if fileName:
            self.LE_fileName.setText(fileName)
            print( fileName )

    def FN_GET_CUSTOMERS(self):

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT POSC_NAME  FROM POS_CUSTOMER  order by POSC_CUST_ID  asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_custName.addItems( [row[0]] )
        mycursor.close()
        print(records)
    def FN_GET_CUST(self):
        self.FN_GET_CustID()

        self.id = self.LB_custID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "select * from POS_CUSTOMER where POSC_CUST_ID = %s "
        x = (self.id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()
        print( record )
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
        self.CMB_status.setCurrentText( record[21] )

        self.CMB_custGroup.setCurrentText( record[2] )
        self.CMB_loyalityType.setCurrentText( record[1] )
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


        self.BTN_createCustomer.clicked.connect(self.FN_CREATE_CUST)

        self.CMB_custGroup.addItems(["1","2","3"])

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
        # get max userid
        mycursor.execute( "SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM POS_CUSTOMER" )
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int( myresult[0] ) + 1

        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

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
            self.close()

        print("in create cust" ,self.name)
        # insert into db

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
            db1.connectionCommit( self.conn )
            db1.connectionClose( self.conn )
            self.close()

        print( "in modify cust", self.CMB_custName )
