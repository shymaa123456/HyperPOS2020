from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime


class CL_customerGP(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_customerGP, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    ###

    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyCustomerGp.ui'
        loadUi(filename, self)
        self.CMB_custGroup.addItems(["Active", "Inactive"])
        self.FN_GET_CUSTGPS()
        self.FN_GET_CustGPID()
        self.FN_GET_CUSTGP()
        self.CMB_custGroupDesc.currentIndexChanged.connect(self.FN_GET_CUSTGP)
        self.BTN_modifyCustGp.clicked.connect(self.FN_MODIFY_CUSTGP)

    def FN_GET_CUSTGPS(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT CG_DESC  FROM CUSTOMER_GROUP  order by CG_GROUP_ID   asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_custGroupDesc.addItems([row[0]])
        mycursor.close()

    def FN_GET_CustGPID(self):
        self.cust = self.CMB_custGroupDesc.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT CG_GROUP_ID  FROM CUSTOMER_GROUP   WHERE CG_DESC  = %s  "
        x = (self.cust,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_custGpID.setText(myresult[0])
        mycursor.close()

    def FN_GET_CUSTGP(self):
        self.FN_GET_CustGPID()

        self.id = self.LB_custGpID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "select CG_Status  from CUSTOMER_GROUP where CG_GROUP_ID = %s "
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        print(record)
        if record[0] == '0':
            self.CMB_custGroup.setCurrentText('Inactive')

        else:
            self.CMB_custGroup.setCurrentText('Active')

        mycursor.close()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createCustomerGp.ui'
        loadUi(filename, self)
        self.BTN_createCustGp.clicked.connect(self.FN_CREATE_CUSTGP)
        self.CMB_custGroup.addItems(["Active", "Inactive"])

    def FN_CREATE_CUSTGP(self):
        print('kkk')
        self.name = self.LE_desc.text().strip()
        self.custGroup = self.CMB_custGroup.currentText()
        if self.custGroup == 'Active':
            self.status = 1
        else:
            self.status = 0

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(cast(CG_GROUP_ID  AS UNSIGNED)) FROM CUSTOMER_GROUP")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if self.name == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        else:

            sql = "INSERT INTO CUSTOMER_GROUP(CG_GROUP_ID, CG_DESC , CG_CREATED_ON, CG_CREATED_BY , CG_Status) " \
                  "         VALUES ( %s, %s, %s,  %s,%s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id, self.name, creationDate, CL_userModule.user_name, self.status
                   )
            mycursor.execute(sql, val)
            # mycursor.execute(sql)

            mycursor.close()

            print(mycursor.rowcount, "Cust Gp inserted.")
            db1.connectionCommit(self.conn)
            db1.connectionClose(self.conn)
            self.close()

        print("in create cust", self.name)
        # insert into db

    def FN_MODIFY_CUSTGP(self):
        print('kkk')
        self.id = self.LB_custGpID.text().strip()
        self.custGroup = self.CMB_custGroup.currentText()
        if self.custGroup == 'Active':
            status = 1
        else:
            status = 0

        mycursor = self.conn.cursor()

        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        sql = "update  CUSTOMER_GROUP  set CG_Status= %s ,CG_CHANGED_ON=%s , 	CG_CHANGED_BY =%s  where CG_GROUP_ID = %s"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (status, changeDate,
               CL_userModule.user_name, self.id)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)

        mycursor.close()

        print(mycursor.rowcount, "record updated.")
        db1.connectionCommit(self.conn)
        db1.connectionClose(self.conn)
        self.close()
