from pathlib import Path

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime

from access.utils.util import *
class CL_customerTP(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_customerTP, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyCustTp.ui'
        loadUi(filename, self)
        try:
            self.FN_GET_CUSTTPS()
            self.FN_GET_NEXTLVL()
            self.CMB_custType.addItems(["Active", "Inactive"])
            self.BTN_createCustTp.clicked.connect(self.FN_CREATE_CUSTTP)
            self.BTN_modifyCustTp.clicked.connect(self.FN_MODIFY_CUSTTP)
            self.BTN_searchCustTp.clicked.connect(self.FN_SEARCH_CUSTTP)
            #self.BTN_getCustTp.clicked.connect(self.FN_GET_CUSTTP)
            self.CMB_nextLevel.activated.connect (self.FN_GET_ID)
            self.CMB_custType.activated.connect (self.FN_GET_ID_STS)
            self.BTN_searchCustTp_all.clicked.connect(self.FN_GET_CUSTTPS)
            self.Qtable_custTP.doubleClicked.connect(self.FN_GET_CUSTTP)
            self.FN_GET_ID()
            self.FN_GET_ID_STS()
            self.Qtable_custTP.setColumnHidden(0, True)
            # self.setFixedWidth(520)
            # self.setFixedHeight(415)

            # Set Style
            # self.voucher_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
        except Exception as err:
            print(err)

    def FN_GET_CUSTTP(self):
     try:

        if len(self.Qtable_custTP.selectedIndexes()) >= 0:
            rowNo = self.Qtable_custTP.selectedItems()[0].row()
            id = self.Qtable_custTP.item(rowNo, 0).text()
            desc = self.Qtable_custTP.item(rowNo, 1).text()
            points = self.Qtable_custTP.item(rowNo, 2).text()
            self.CMB_nextLevel.show()
            status = self.Qtable_custTP.item(rowNo, 4).text()
            if  rowNo != 0 :
                nextLevel = self.Qtable_custTP.item(rowNo, 3).text()
                #self.LB_nextLvlId.setText(nextLevel )
                #nextLevel = self.FN_GET_NEXTlEVEL_DESC(nextLevel)
                self.CMB_nextLevel.setCurrentText(nextLevel)
            else:
                self.LB_nextLvlId.setText(' ')
                self.CMB_nextLevel.hide()
            self.LE_desc.setText(desc)
            self.LE_points.setText(points)
            self.LB_custTpId.setText(id)
            self.CMB_custType.setCurrentText(status)
            self.FN_GET_ID_STS()

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
            for i in reversed(range(self.Qtable_custTP.rowCount())):
                self.Qtable_custTP.removeRow(i)
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            name = self.LE_desc.text().strip()
            self.custType = self.CMB_custType.currentText()
            if self.custType == 'Active':
                whereClause = "where LOYCT_STATUS =1  "
            else:
                whereClause = "where LOYCT_STATUS = 0 "

            if name != '':
                whereClause = whereClause + "and LOYCT_DESC like '%" + str(name) + "%'"
            whereClause = whereClause  + " and LOYCT_TYPE_ID != 'H1'"

            sql_select_query = "select  LOYCT_TYPE_ID,LOYCT_DESC , LOYCT_POINTS_TO_PROMOTE,LOYCT_TYPE_NEXT,LOYCT_STATUS from  Hyper1_Retail.LOYALITY_CUSTOMER_TYPE " + whereClause +"order by LOYCT_TYPE_ID*1 asc"
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_custTP.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    if column_number == 3  :
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    if column_number == 2 and row_number!=0 :
                        data = self.FN_GET_NEXTlEVEL_DESC(str(data))
                        item = QTableWidgetItem(str(data))

                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable_custTP.setItem(row_number, column_number, QTableWidgetItem(item ))
            mycursor.close()
            #self.Qtable_custTP.doubleClicked.connect(self.FN_GET_CUSTTP)
        except Exception as err:
            print(err)

    def FN_GET_NEXTlEVEL(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC ,LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID != 'H1'  order by LOYCT_TYPE_ID*1   asc")
        records = mycursor.fetchall()
        #mycursor.close()
        return records

    def FN_GET_NEXTlEVEL_ID(self,desc):
        try:
            self.conn = db1.connect()
            mycursor3 = self.conn.cursor()
            mycursor3.execute("SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_DESC= '"+desc+"'")
            records = mycursor3.fetchone()
            #mycursor3.close()
            return records[0]
        except Exception as err:
            print(err)

    def FN_GET_NEXTlEVEL_DESC(self,id):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT  LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE  where LOYCT_TYPE_ID= '"+id+"'")
        records = mycursor.fetchone()
        #mycursor3.close()
        return records[0]


    def FN_GET_CUSTTPS(self):
        for i in reversed(range(self.Qtable_custTP.rowCount())):
            self.Qtable_custTP.removeRow(i)
        self.conn = db1.connect()
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT  LOYCT_TYPE_ID, LOYCT_DESC, LOYCT_POINTS_TO_PROMOTE, LOYCT_TYPE_NEXT, LOYCT_STATUS FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID != 'H1' order by LOYCT_TYPE_ID*1   asc")
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_custTP.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                if column_number == 4:
                    data = util.FN_GET_STATUS_DESC(str(data))
                    item = QTableWidgetItem(str(data))
                if column_number == 3 and row_number != 0:
                    data = self.FN_GET_NEXTlEVEL_DESC(str(data))
                    item = QTableWidgetItem(str(data))

                item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                self.Qtable_custTP.setItem(row_number, column_number, QTableWidgetItem(item))
        #self.Qtable_custTP.doubleClicked.connect(self.FN_GET_CUSTTP)

    def FN_GET_NEXTLVL(self):
        self.CMB_nextLevel.clear()
        records = self.FN_GET_NEXTlEVEL()
        for row in records:
            self.CMB_nextLevel.addItems([row[0]])



    def FN_CHECK_DUP_NAME(self, name,id=''):
        self.conn = db1.connect()
        mycursor1 = self.conn.cursor()
        # get max userid
        sql = "SELECT LOYCT_DESC  FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC ='"+name+"' and LOYCT_TYPE_ID !='"+id+"'"
        #val = (name,)
        mycursor1.execute(sql)
        myresult = mycursor1.fetchall()
        len = mycursor1.rowcount
        if len > 0:
            return True
        else:
            return False

    def FN_CHECK_DUP_NEXTLEVEL(self, name,id=''):
        try:
            self.conn = db1.connect()
            mycursor2 = self.conn.cursor()
            #print(name)
            sql = "SELECT * FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_NEXT = '" + name + "' and LOYCT_TYPE_ID !='"+id+"'"
            mycursor2.execute(sql)
            myresult = mycursor2.fetchall()
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
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max userid
            mycursor.execute("SELECT max(cast(LOYCT_TYPE_ID   AS UNSIGNED))   FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE ")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1

            if name == '':
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")
            else:
                if self.FN_CHECK_DUP_NAME(name) != False:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")

                else:
                    nextLevel1 = self.FN_GET_NEXTlEVEL_ID(nextLevel)
                    if  self.FN_CHECK_DUP_NEXTLEVEL(nextLevel1)!=False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "المستوى التالي مكرر")
                    else:
                        sql = "INSERT INTO Hyper1_Retail.LOYALITY_CUSTOMER_TYPE" \
                              "         VALUES ( %s, %s, %s,  %s,%s)"

                        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                        val = (self.id, name,points,nextLevel1 ,  status
                               )
                        mycursor.execute(sql, val)
                        #mycursor.close()

                        print(mycursor.rowcount, "Cust Tp inserted.")
                        QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                        db1.connectionCommit(conn)
                        self.FN_GET_CUSTTPS()
                        self.FN_GET_NEXTLVL()
                        self.FN_CLEAR_FEILDS()

        except Exception as err:
            #mycursor.close()
            print(err)

    def FN_MODIFY_CUSTTP(self):
        try:
            if len(self.Qtable_custTP.selectedIndexes()) > 0:
                rowNo = self.Qtable_custTP.selectedItems()[0].row()

                desc_old = self.Qtable_custTP.item(rowNo, 1).text()
                next_level_old = self.Qtable_custTP.item(rowNo, 3).text()
                id = self.LB_custTpId.text()
                desc = self.LE_desc.text().strip()
                points = self.LE_points.text().strip()
                custType = self.CMB_custType.currentText()
                nextLevel = self.LB_nextLvlId.text().strip()
                if custType == 'Active':
                    status = 1
                else:
                    status = 0
                ret = self.FN_CHECK_DUP_NAME(desc,id)
                error = 0
                if desc == '':
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")
                else:
                    if desc != desc_old:
                        if self.FN_CHECK_DUP_NAME(desc,id) != False:
                            QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                            error=1
                    if next_level_old != nextLevel :
                        if self.FN_CHECK_DUP_NEXTLEVEL(nextLevel,id) != False:
                            QtWidgets.QMessageBox.warning(self, "خطأ", "المستوى التالي مكرر")
                            error = 1

                    if error != 1:
                        self.conn = db1.connect()
                        mycursor = self.conn.cursor()

                        sql = "update  Hyper1_Retail.LOYALITY_CUSTOMER_TYPE set LOYCT_STATUS= %s ,LOYCT_DESC= %s,LOYCT_POINTS_TO_PROMOTE=%s ,LOYCT_TYPE_NEXT= %s where LOYCT_TYPE_ID = %s"
                        val = (status,desc,points,nextLevel ,id,)
                        mycursor.execute(sql, val)
                        mycursor.close()                #
                        print(mycursor.rowcount, "record updated.")
                        QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                        db1.connectionCommit(self.conn)
                        self.FN_GET_CUSTTPS()
                        self.FN_CLEAR_FEILDS()
                        mycursor.close()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

        except Exception as err:

            print(err)
        #db1.connectionClose(self.conn)
        #self.close()

    def FN_CLEAR_FEILDS (self):

        self.LE_desc.clear()
        self.LE_points.clear()
        self.LB_nextLvlId.clear()
        self.LB_status.setText('1')
        self.CMB_custType.setCurrentText('Active')
        self.CMB_nextLevel.setCurrentText('')


