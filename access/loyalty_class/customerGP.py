from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
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

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyCustGp.ui'
        loadUi(filename, self)

        self.FN_GET_CUSTGPS()
        # self.FN_GET_CustGPID()
        # self.FN_GET_CUSTGP()
        try:
            self.CMB_custGroup.addItems(["Active", "Inactive"])
            self.BTN_createCustGp.clicked.connect(self.FN_CREATE_CUSTGP)
            self.BTN_modifyCustGp.clicked.connect(self.FN_MODIFY_CUSTGP)
            #self.Qtable_custGP.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        except Exception as err:
            print(err)

    def FN_GET_STATUS_DESC(self,id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    def FN_GET_CUSTGPS(self):
        for i in reversed(range(self.Qtable_custGP.rowCount())):
            self.Qtable_custGP.removeRow(i)

        mycursor = self.conn.cursor()
        mycursor.execute("SELECT  CG_group_id, CG_DESC ,cg_status  FROM Hyper1_Retail.CUSTOMER_GROUP  order by CG_GROUP_ID   asc")
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_custGP.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 2:
                    data = self.FN_GET_STATUS_DESC(str(data))
                self.Qtable_custGP.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        mycursor.close()



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
        mycursor.execute("SELECT max(cast(CG_GROUP_ID  AS UNSIGNED)) FROM Hyper1_Retail.CUSTOMER_GROUP")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if self.name == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        else:

            sql = "INSERT INTO Hyper1_Retail.CUSTOMER_GROUP(CG_GROUP_ID, CG_DESC , CG_CREATED_ON, CG_CREATED_BY , CG_Status) " \
                  "         VALUES ( %s, %s, %s,  %s,%s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id, self.name, creationDate, CL_userModule.user_name, self.status
                   )
            mycursor.execute(sql, val)
            # mycursor.execute(sql)

            mycursor.close()

            print(mycursor.rowcount, "Cust Gp inserted.")
            db1.connectionCommit(self.conn)
            self.FN_GET_CUSTGPS()
            #db1.connectionClose(self.conn)
            #self.close()

        print("in create cust", self.name)

        # insert into db

    def FN_MODIFY_CUSTGP(self):
        try:

            rowNo = self.Qtable_custGP.selectedItems()[0].row()
            #rowNo.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
            print(rowNo)

            #if rowNo > 0:
            id = self.Qtable_custGP.item(rowNo, 0).text()
            desc = self.Qtable_custGP.item(rowNo, 1).text()
            status = self.Qtable_custGP.item(rowNo, 2).text()

        except Exception as err:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select the row you want to modify ")
            print(err)
        print('kkk')
        # self.id = self.LB_custGpID.text().strip()
        # self.custGroup = self.CMB_custGroup.currentText()
        if status == 'Active':
            status = 1
        else:
            status = 0
        #
        mycursor = self.conn.cursor()

        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        sql = "update  Hyper1_Retail.CUSTOMER_GROUP  set CG_Status= %s ,CG_DESC = %s ,CG_CHANGED_ON=%s , 	CG_CHANGED_BY =%s  where CG_GROUP_ID = %s"


        val = (status,desc, changeDate,CL_userModule.user_name,id)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)

        mycursor.close()
        #
        print(mycursor.rowcount, "record updated.")
        db1.connectionCommit(self.conn)
        db1.connectionClose(self.conn)
        self.close()
