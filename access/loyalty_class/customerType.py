import sys
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
        #mycursor = self.conn.cursor()

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyCustTp.ui'
        loadUi(filename, self)

        self.FN_GET_CUSTTPS()
        records=self.FN_GET_NEXTlEVEL()
        #id = self.FN_GET_NEXTlEVEL_ID
        #self.LB_nextLvlId.setText ()
        for row in records:
            self.CMB_nextLevel.addItems([row[0]])
        try:
            self.CMB_custType.addItems(["Active", "Inactive"])
            self.BTN_createCustTp.clicked.connect(self.FN_CREATE_CUSTTP)
            self.BTN_modifyCustTp.clicked.connect(self.FN_MODIFY_CUSTTP)
            self.BTN_searchCustTp.clicked.connect(self.FN_SEARCH_CUSTTP)
            #self.BTN_getCustTp.clicked.connect(self.FN_GET_CUSTTP)
            self.CMB_nextLevel.activated.connect (self.FN_GET_ID)
            self.CMB_custType.activated.connect (self.FN_GET_ID_STS)
            self.FN_GET_ID()
            self.FN_GET_ID_STS()
        except Exception as err:
            print(err)

    def FN_GET_CUSTTP(self):
     try:
        if len(self.Qtable_custTP.selectedIndexes()) >= 0:
            rowNo = self.Qtable_custTP.selectedItems()[0].row()
            id = self.Qtable_custTP.item(rowNo, 0).text()
            desc = self.Qtable_custTP.item(rowNo, 1).text()
            points = self.Qtable_custTP.item(rowNo, 2).text()

            status = self.Qtable_custTP.item(rowNo, 4).text()
            if  rowNo != 0 :
                nextLevel = self.Qtable_custTP.item(rowNo, 3).text()
                self.LB_nextLvlId.setText(nextLevel )
                nextLevel = self.FN_GET_NEXTlEVEL_DESC(nextLevel)
                self.CMB_nextLevel.setCurrentText(nextLevel)

            self.LE_desc.setText(desc)
            self.LE_points.setText(points)
            self.LB_custTpId.setText(id)
            self.CMB_custType.setCurrentText(status)

            #print(rowNo)
            #self.FN_MODIFY_CUSTTP()
     except Exception as err:
         print(err)
    def FN_GET_ID_STS(self):

        sts = self.CMB_custType.currentText()
        if sts == 'Active':
            id= 1
        else:
            id = 0
        self.LB_status.setText (str(id))
    def FN_GET_ID(self):

        desc = self.CMB_nextLevel.currentText()
        id = self.FN_GET_NEXTlEVEL_ID(desc)
        self.LB_nextLvlId.setText (id)
    def FN_SEARCH_CUSTTP(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            for i in reversed(range(self.Qtable_custTP.rowCount())):
                self.Qtable_custTP.removeRow(i)
            name = self.LE_desc.text().strip()
            self.custType = self.CMB_custType.currentText()
            if self.custType == 'Active':
                whereClause = "where LOYCT_STATUS =1  "
            else:
                whereClause = "where LOYCT_STATUS = 0 "
            if name != '':
                whereClause = whereClause + "and LOYCT_DESC = '" + str(name) + "'"
            whereClause = whereClause  + " and LOYCT_TYPE_ID != 'H1'"
            sql_select_query = "select  LOYCT_TYPE_ID,LOYCT_DESC , LOYCT_POINTS_TO_PROMOTE,LOYCT_TYPE_NEXT,LOYCT_STATUS from  Hyper1_Retail.LOYALITY_CUSTOMER_TYPE " + whereClause
            print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            print(sql_select_query)
            for row_number, row_data in enumerate(records):
                self.Qtable_custTP.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable_custTP.setItem(row_number, column_number, QTableWidgetItem(item ))
            mycursor.close()
            self.Qtable_custTP.doubleClicked.connect(self.FN_GET_CUSTTP)
        except :
            print(sys.exc_info())
    def FN_GET_NEXTlEVEL(self):
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT LOYCT_DESC ,LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  order by LOYCT_TYPE_ID   asc")
        records = mycursor.fetchall()
        #mycursor.close()
        return records

    def FN_GET_NEXTlEVEL_ID(self,desc):
        try:
            mycursor3 = self.conn.cursor()
            mycursor3.execute("SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_DESC= '"+desc+"'")
            records = mycursor3.fetchone()
            mycursor3.close()
            return records[0]
        except Exception as err:
            print(err)

    def FN_GET_NEXTlEVEL_DESC(self,id):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT  LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_TYPE_ID= '"+id+"'")
        records = mycursor.fetchone()
        #mycursor3.close()
        return records[0]

    def FN_GET_STATUS_DESC(self, id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    def FN_GET_CUSTTPS(self):
        for i in reversed(range(self.Qtable_custTP.rowCount())):
            self.Qtable_custTP.removeRow(i)
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT  LOYCT_TYPE_ID, LOYCT_DESC, LOYCT_POINTS_TO_PROMOTE, LOYCT_TYPE_NEXT, LOYCT_STATUS FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID != 'H1' order by LOYCT_TYPE_ID   asc")
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_custTP.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                self.Qtable_custTP.setItem(row_number, column_number, item)
        self.Qtable_custTP.doubleClicked.connect(self.FN_GET_CUSTTP)
        mycursor.close()

    def FN_CHECK_STATUS(self, status):
        if status == 1 or status == 0 :
            return True
        else :
            return False

    def FN_CHECK_DUP_NAME(self, name):
        mycursor1 = self.conn.cursor()
        # get max userid
        sql = "SELECT LOYCT_DESC  FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC ='"+name+"'"
        #val = (name,)
        mycursor1.execute(sql)
        len = mycursor1.rowcount
        if len > 0:
            return True
        else:
            return False

    def FN_CHECK_DUP_NEXTLEVEL(self, name):
        try:
            mycursor2 = self.conn.cursor()
            print(name)
            sql = "SELECT LOYCT_DESC  FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + name + "'"
            mycursor2.execute(sql)
            len = mycursor2.rowcount
            if len > 0:
                return True
            else:
                return False
        except Exception as err:
            #mycursor2.close()
            print(err)

    def FN_CREATE_CUSTTP(self):
        try:
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
            ret = self.FN_CHECK_DUP_NAME(name)
            if name == '':
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")
            else:
                if ret != True :

                    nextLevel1 = self.FN_GET_NEXTlEVEL_ID(nextLevel)
                    sql = "INSERT INTO Hyper1_Retail.LOYALITY_CUSTOMER_TYPE" \
                          "         VALUES ( %s, %s, %s,  %s,%s)"

                    # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                    val = (self.id, name,points,nextLevel1 ,  status
                           )
                    mycursor.execute(sql, val)
                    mycursor.close()

                    print(mycursor.rowcount, "Cust Tp inserted.")
                    QtWidgets.QMessageBox.information(self, "Success", "Cust Tp inserted.")
                    db1.connectionCommit(self.conn)
                    #self.FN_GET_CUSTTPS()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Name duplicated' ")
                    #mycursor.close()
        except Exception as err:
            #mycursor.close()
            print(err)

    def FN_MODIFY_CUSTTP(self):
        try:
                    id = self.LB_custTpId.text()
                    desc = self.LE_desc.text().strip()
                    points = self.LE_points.text().strip()
                    custType = self.CMB_custType.currentText()
                    nextLevel = self.LB_nextLvlId.text().strip()
                    if custType == 'Active':
                        status = 1
                    else:
                        status = 0
                    mycursor = self.conn.cursor()

                    sql = "update  Hyper1_Retail.LOYALITY_CUSTOMER_TYPE set LOYCT_STATUS= %s ,LOYCT_DESC= %s,LOYCT_POINTS_TO_PROMOTE=%s ,LOYCT_TYPE_NEXT= %s where LOYCT_TYPE_ID = %s"
                    val = (status,desc,points,nextLevel ,id,)
                    mycursor.execute(sql, val)
                    mycursor.close()                #
                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "Success", "Cust Tp updated")
                    db1.connectionCommit(self.conn)
                    #self.FN_GET_CUSTTPS()
        except Exception as err:
            mycursor.close()
            print(err)
        #db1.connectionClose(self.conn)
        #self.close()





