from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from access.utils.util import *
from datetime import datetime


class CL_customerGP(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self,pp):
        super(CL_customerGP, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()
        self.p=pp
    ###

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyCustGp.ui'
        loadUi(filename, self)

        self.FN_GET_CUSTGPS()
        # self.FN_GET_CustGPID()
        # self.FN_GET_CUSTGP()
        try:
            self.CMB_custGroup.addItems(["Active", "Inactive"])
            self.LB_status.setText('1')
            self.CMB_custGroup.activated.connect(self.FN_GET_STATUS)
            self.BTN_createCustGp.clicked.connect(self.FN_CREATE_CUSTGP)
            self.BTN_modifyCustGp.clicked.connect(self.FN_MODIFY_CUSTGP)
            #self.Qtable_custGP.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.BTN_searchCustGp.clicked.connect(self.FN_SEARCH_CUSTGP)
            self.BTN_searchCustGp_all.clicked.connect(self.FN_GET_CUSTGPS)
            self.setFixedWidth(368)
            self.setFixedHeight(430)
            self.Qtable_custGP.setColumnHidden(0, True)
            self.Qtable_custGP.doubleClicked.connect(self.FN_GET_CUSTGP)
        except Exception as err:
            print(err)

    def FN_SEARCH_CUSTGP(self):
        self.conn1 = db1.connect()
        try:
            for i in reversed(range(self.Qtable_custGP.rowCount())):
                self.Qtable_custGP.removeRow(i)

            mycursor = self.conn1.cursor()

            name = self.LE_desc.text().strip()
            self.custGroup = self.CMB_custGroup.currentText()
            if self.custGroup == 'Active':

                whereClause = "where CG_Status =1  "
            else:
                whereClause = "where CG_Status = 0 "

            if name != '' :
                whereClause = whereClause + "and CG_DESC like '%" + str(name) + "%'"

            sql_select_query = "select  CG_GROUP_ID, CG_DESC , CG_Status from Hyper1_Retail.CUSTOMER_GROUP " + whereClause + " and CG_DESC !='H1' order by CG_GROUP_ID*1 asc"
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_custGP.insertRow(row_number)

                for column_number, data in enumerate(row_data):


                    item = QTableWidgetItem(str(data))

                    if column_number == 2:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable_custGP.setItem(row_number, column_number, item)
            #self.Qtable_custGP.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #
            self.Qtable_custGP.doubleClicked.connect(self.FN_GET_CUSTGP)
            #mycursor.close()
        #self.Qtable_custGP.setItem(0, 0, QTableWidgetItem(str('11111')))
        except Exception as err:
             print(err)

    def FN_GET_CUSTGPS(self):
        self.conn = db1.connect()
        try:
            for i in reversed(range(self.Qtable_custGP.rowCount())):
                self.Qtable_custGP.removeRow(i)

            mycursor = self.conn.cursor()
            mycursor.execute("SELECT  CG_group_id, CG_DESC ,cg_status  FROM Hyper1_Retail.CUSTOMER_GROUP  where  CG_DESC !='H1' order by CG_GROUP_ID*1   asc")
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_custGP.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))

                    if column_number == 2:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))

                    self.Qtable_custGP.setItem(row_number, column_number, item)
            #self.Qtable_custGP.doubleClicked.connect(self.FN_GET_CUSTGP)

            #mycursor.close()
        except Exception as err:
            print(err)

    def FN_GET_CUSTGP(self):
        try:
            if len(self.Qtable_custGP.selectedIndexes()) >= 0:
                rowNo = self.Qtable_custGP.selectedItems()[0].row()
                id = self.Qtable_custGP.item(rowNo, 0).text()
                desc = self.Qtable_custGP.item(rowNo, 1).text()
                status = self.Qtable_custGP.item(rowNo, 2).text()
                self.LE_desc.setText(desc)
                self.LB_custGpId.setText(id)
                self.LB_status.setText(util.FN_GET_STATUS_id(status))
                self.CMB_custGroup.setCurrentText(status)
                # self.FN_MODIFY_CUSTTP()
        except Exception as err:
            print(err)
    def FN_CHECK_DUP_NAME(self,name,id=''):
        self.conn1 = db1.connect()
        mycursor1 = self.conn1.cursor()
        sql = "SELECT CG_DESC  FROM Hyper1_Retail.CUSTOMER_GROUP where CG_DESC = '"+name+"' and CG_GROUP_ID !='"+id+"'"
        mycursor1.execute(sql)
        myresult = mycursor1.fetchall()
        len = mycursor1.rowcount
        print(len)
        if len > 0:
            #mycursor1.close()
            return True
        else:
            #mycursor1.close()
            return False

    def FN_GET_STATUS(self):
        status = self.CMB_custGroup.currentText()
        if status == 'Active'  :
            self.LB_status.setText('1')
        else :
            self.LB_status.setText('0')

    def FN_CREATE_CUSTGP(self):
        self.conn = db1.connect()
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

        if self.name == '' :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاءادخال الاسم")

        else:
            try:
                if self.FN_CHECK_DUP_NAME(self.name) != False:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                    mycursor.close()
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
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                    db1.connectionCommit(self.conn)
                    self.FN_GET_CUSTGPS()
                    self.FN_CLEAR_FEILDS()
                    #db1.connectionClose(self.conn)
                    #self.close()
            except Exception as err:
                print(err)
        print("in create cust", self.name)

        # insert into db

    def FN_MODIFY_CUSTGP(self):
        self.conn1 = db1.connect()
        if len(self.Qtable_custGP.selectedIndexes()) >0 :
            rowNo = self.Qtable_custGP.selectedItems()[0].row()
            id = self.LB_custGpId.text().strip()
            desc_old = self.Qtable_custGP.item(rowNo, 1).text()
            desc = self.LE_desc.text().strip()
            custGroup = self.CMB_custGroup.currentText()
            if custGroup == 'Active':
                status = 1
            else:
                status = 0
            #
            error = 0
            if self.desc == '':
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")

            else:
                if desc != desc_old:
                    if self.FN_CHECK_DUP_NAME(desc,id) != False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                        error=1

                if error!=1:
                    mycursor = self.conn1.cursor()
                    changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "update  Hyper1_Retail.CUSTOMER_GROUP  set CG_Status= %s ,CG_DESC = %s ,CG_CHANGED_ON=%s , 	CG_CHANGED_BY =%s  where CG_GROUP_ID = %s"
                    val = (status,desc, changeDate,CL_userModule.user_name,id)
                    mycursor.execute(sql, val)
                    #mycursor.close()
                    #
                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                    db1.connectionCommit(self.conn1)
                    self.FN_GET_CUSTGPS()
                    self.FN_CLEAR_FEILDS ()
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

    def FN_CLEAR_FEILDS (self):
        self.LB_custGpId.clear()
        self.LE_desc.clear()
        self.CMB_custGroup.setCurrentText('Active')
        self.LB_status.setText('1')
