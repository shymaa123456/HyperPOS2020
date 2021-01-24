from pathlib import Path

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime


class CL_customerTP(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_customerTP, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyCustTp.ui'
        loadUi(filename, self)

        self.FN_GET_CUSTTPS()
        # self.FN_GET_CustGPID()
        records=self.FN_GET_NEXTlEVEL()
        for row in records:
            self.CMB_nextLevel.addItems([row[0]])
        try:
            self.CMB_custType.addItems(["Active", "Inactive"])
            self.BTN_createCustTp.clicked.connect(self.FN_CREATE_CUSTTP)
            self.BTN_modifyCustTp.clicked.connect(self.FN_MODIFY_CUSTTP)
            #self.Qtable_custGP.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        except Exception as err:
            print(err)

    def FN_GET_NEXTlEVEL(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  order by LOYCT_TYPE_ID   asc")
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_GET_NEXTlEVEL_ID(self,desc):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_DESC= '"+desc+"'")
        records = mycursor.fetchone()

        mycursor.close()
        return records[0]

    def FN_GET_NEXTlEVEL_DESC(self,id):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT  LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_TYPE_ID= '"+id+"'")
        records = mycursor.fetchone()

        mycursor.close()
        return records[0]
    #def FN_VALIDATE_NEXTlEVEL(self,):


    def FN_GET_STATUS_DESC(self, id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    def FN_GET_CUSTTPS(self):
        for i in reversed(range(self.Qtable_custTP.rowCount())):
            self.Qtable_custTP.removeRow(i)

        mycursor = self.conn.cursor()
        mycursor.execute("SELECT  LOYCT_TYPE_ID, LOYCT_DESC, LOYCT_POINTS_TO_PROMOTE, LOYCT_TYPE_NEXT, LOYCT_STATUS FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  order by LOYCT_TYPE_ID   asc")
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_custTP.insertRow(row_number)
            for column_number, data in enumerate(row_data):

                if column_number == 3 :
                    data= self.FN_GET_NEXTlEVEL_DESC(str(data))
                    # comboBox = QtWidgets.QComboBox()
                    # records = self.FN_GET_NEXTlEVEL()
                    # for row in records:
                    #    comboBox.addItems([row[0]])
                    # comboBox.setCurrentText(data)
                    # self.Qtable_custTP.setCellWidget(row_number, column_number, comboBox)
                else:
                    if column_number == 4:
                        data = self.FN_GET_STATUS_DESC(str(data))
                    item = QTableWidgetItem(str(data))
                    if column_number == 0:
                        item.setFlags(QtCore.Qt.NoItemFlags)

                    self.Qtable_custTP.setItem(row_number, column_number, item)
        mycursor.close()


    def FN_CREATE_CUSTTP(self):

        name = self.LE_desc.text().strip()
        points = self.LE_points.text().strip()

        custType = self.CMB_custType.currentText()
        nextLevel = self.CMB_nextLevel.currentText()
        if custType == 'Active':
            status = 1
        else:
           status = 0

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(cast(LOYCT_TYPE_ID   AS UNSIGNED))   FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE ")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        #creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if name == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        else:
            nextLevel = self.FN_GET_NEXTlEVEL_ID(nextLevel)
            sql = "INSERT INTO Hyper1_Retail.LOYALITY_CUSTOMER_TYPE" \
                  "         VALUES ( %s, %s, %s,  %s,%s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (self.id, name,points,nextLevel ,  status
                   )
            mycursor.execute(sql, val)
            # mycursor.execute(sql)

            mycursor.close()

            print(mycursor.rowcount, "Cust Tp inserted.")
            QtWidgets.QMessageBox.information(self, "Success", "Cust Tp inserted.")
            db1.connectionCommit(self.conn)
            self.FN_GET_CUSTTPS()
            #db1.connectionClose(self.conn)
            #self.close()


        # insert into db

    def FN_MODIFY_CUSTTP(self):
        try:

            rowNo = self.Qtable_custTP.selectedItems()[0].row()
            #rowNo.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
            print(rowNo)
            if rowNo == None:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select the row you want to modify ")
            else:

                #if rowNo > 0:
                id = self.Qtable_custTP.item(rowNo, 0).text()
                desc = self.Qtable_custTP.item(rowNo, 1).text()
                points = self.Qtable_custTP.item(rowNo, 2).text()
                nextLevel = self.Qtable_custTP.item(rowNo, 3).text()
                # nextLevel = CMB_nextLevel.currentText()

                status = self.Qtable_custTP.item(rowNo, 4).text()
                nextLevel = self.FN_GET_NEXTlEVEL_ID(nextLevel)
                if status == 'Active':
                    status = 1
                else:
                    status = 0
                #
                mycursor = self.conn.cursor()
                sql = "update  Hyper1_Retail.LOYALITY_CUSTOMER_TYPE set LOYCT_STATUS= %s ,LOYCT_DESC= %s,LOYCT_POINTS_TO_PROMOTE=%s ,LOYCT_TYPE_NEXT= %s where LOYCT_TYPE_ID = %s"
                val = (status,desc,points,nextLevel ,id)
                mycursor.execute(sql, val)
                mycursor.close()                #
                print(mycursor.rowcount, "record updated.")
                QtWidgets.QMessageBox.information(self, "Success", "Cust Tp updated")
                db1.connectionCommit(self.conn)

        except Exception as err:

            print(err)
        #db1.connectionClose(self.conn)
        #self.close()





