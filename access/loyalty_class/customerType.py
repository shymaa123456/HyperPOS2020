from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator ,QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime
class CL_customerTP(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super( CL_customerTP, self ).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()


    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyCustomerGp.ui'
        loadUi( filename, self )
        self.CMB_custType.addItems( ["Active", "Inactive"] )
        self.FN_GET_CUSTTPS()
        self.FN_GET_CustTPID()
        self.FN_GET_CUSTTP()
        self.CMB_custTypeDesc.currentIndexChanged.connect( self.FN_GET_CUSTTP )
        self.BTN_modifyCustTp.clicked.connect( self.FN_MODIFY_CUSTGP )

    def FN_GET_CUSTTPS(self):
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT LOYCT_DESC   FROM LOYALITY_CUSTOMER_TYPE  order by LOYCT_TYPE_ID   asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_custTypeDesc.addItems( [row[0]] )
        mycursor.close()

    def FN_GET_CustTPID(self):
        self.cust = self.CMB_custTypeDesc.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT LOYCT_TYPE_ID   FROM LOYALITY_CUSTOMER_TYPE   WHERE LOYCT_DESC  = %s  "
        x = (self.cust,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        self.LB_custTpID.setText( myresult[0] )
        mycursor.close()

    def FN_GET_CUSTTP(self):
        self.FN_GET_CustTPID()

        self.id = self.LB_custTpID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "select LOYCT_STATUS , 	LOYCT_POINTS_TO_PROMOTE   from LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID = %s "
        x = (self.id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()
        print( record )
        if record[0] == '0' :
            self.CMB_custType.setCurrentText( 'Inactive' )

        else:
            self.CMB_custType.setCurrentText( 'Active' )
        self.LE_points.setText(record[1])
        mycursor.close()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createCustomerGp.ui'
        loadUi( filename, self )
        self.BTN_createCustTp.clicked.connect( self.FN_CREATE_CUSTTP )
        self.CMB_custType.addItems( ["Active", "Inactive"] )

    def FN_CREATE_CUSTTP (self):

        self.name = self.LE_desc.text().strip()
        self.points = self.LE_points.text().strip()
        self.custType = self.CMB_custType.currentText()
        if self.custType == 'Active':
            self.status = 1
        else:
            self.status = 0

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute( "SELECT max(cast(LOYCT_TYPE_ID   AS UNSIGNED))   FROM LOYALITY_CUSTOMER_TYPE " )
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int( myresult[0] ) + 1

        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

        if self.name == '' :
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter all required fields" )

        else:

            sql = "INSERT INTO LOYALITY_CUSTOMER_TYPE " \
                  "         VALUES ( %s, %s, %s,  %s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id, self.name ,self.points, self.status
                   )
            mycursor.execute( sql, val )
            # mycursor.execute(sql)

            mycursor.close()

            print( mycursor.rowcount, "Cust Type inserted." )
            db1.connectionCommit( self.conn )
            db1.connectionClose( self.conn )
            self.close()

        print( "in create cust", self.name )
        # insert into db


    def FN_MODIFY_CUSTTP (self):

        self.id = self.LB_custTpID.text().strip()
        self.custType = self.CMB_custType.currentText()
        self.points = self.LE_points.text().strip()
        if self.custType == 'Active':
            status =  1
        else:
            status = 0

        mycursor = self.conn.cursor()

        changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )



        sql = "update  LOYALITY_CUSTOMER_TYPE set LOYCT_STATUS= %s ,LOYCT_POINTS_TO_PROMOTE=%s where LOYCT_TYPE_ID = %s"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (status, self.points,  self.id)
        mycursor.execute( sql, val )
        # mycursor.execute(sql)

        mycursor.close()

        print( mycursor.rowcount, "record updated." )
        db1.connectionCommit( self.conn )
        db1.connectionClose( self.conn )
        self.close()


