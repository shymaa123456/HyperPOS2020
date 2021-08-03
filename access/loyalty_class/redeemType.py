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


class CL_redeemType(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_redeemType, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()

    ###

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyRedeemType.ui'
        loadUi(filename, self)
        conn = db1.connect()
        mycursor = conn.cursor()
        self.FN_GET_REDEEMTPS()
        # self.FN_GET_CustGPID()
        # self.FN_GET_CUSTGP()
        try:
            self.CMB_redeemType.addItems(["Active", "Inactive"])
            self.LB_status.setText('1')
            self.CMB_redeemType.activated.connect(self.FN_GET_STATUS)

            self.Qtable_redeemTp.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.BTN_searchRedeemTp.clicked.connect(self.FN_SEARCH_REDEEMTP)
            self.BTN_searchRedeemTp_all.clicked.connect(self.FN_GET_REDEEMTPS)
            # self.setFixedWidth(380)
            # self.setFixedHeight(448)

            # Set Style
            # self.voucher_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

            self.Qtable_redeemTp.setColumnHidden(0, True)
            self.Qtable_redeemTp.doubleClicked.connect(self.FN_GET_REDEEMTYPE)
            for row_number, row_data in enumerate(CL_userModule.myList):
                if row_data[1] == 'Redeem_Type':
                    if row_data[4] == 'None':
                        print('hh')
                    else:
                        sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                        x = (row_data[4],)
                        mycursor.execute(sql_select_query, x)

                        result = mycursor.fetchone()
                        # print(result)
                        if result[0] == 'create':
                            self.BTN_createRedeemTp.setEnabled(True)
                            self.BTN_createRedeemTp.clicked.connect(self.FN_CREATE_REDEEMTP)
                        elif result[0] == 'modify':
                            self.BTN_modifyRedeemTp.setEnabled(True)
                            self.BTN_modifyRedeemTp.clicked.connect(self.FN_MODIFY_REDEEMTP)
        except Exception as err:
            print(err)

    def FN_SEARCH_REDEEMTP(self):
        self.conn1 = db1.connect()
        try:
            for i in reversed(range(self.Qtable_redeemTp.rowCount())):
                self.Qtable_redeemTp.removeRow(i)

            mycursor = self.conn1.cursor()

            name = self.LE_desc.text().strip()
            redeemTp = self.CMB_redeemType.currentText()
            if redeemTp == 'Active':

                whereClause = "where REDEEMT_STATUS =1  "
            else:
                whereClause = "where REDEEMT_STATUS = 0 "

            if name != '' :
                whereClause = whereClause + "and REDEEMT_DESC like '%" + str(name) + "%'"

            sql_select_query = "select REDEEMT_TYPE_ID,REDEEMT_DESC,REDEEMT_STATUS  from Hyper1_Retail.REDEEM_TYPE " + whereClause + "  order by REDEEMT_TYPE_ID*1 asc"
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_redeemTp.insertRow(row_number)

                for column_number, data in enumerate(row_data):


                    item = QTableWidgetItem(str(data))

                    if column_number == 2:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable_redeemTp.setItem(row_number, column_number, item)

        except Exception as err:
             print(err)

    def FN_GET_REDEEMTPS(self):
        self.conn = db1.connect()
        try:
            for i in reversed(range(self.Qtable_redeemTp.rowCount())):
                self.Qtable_redeemTp.removeRow(i)

            mycursor = self.conn.cursor()
            mycursor.execute("SELECT REDEEMT_TYPE_ID,REDEEMT_DESC,REDEEMT_STATUS FROM Hyper1_Retail.REDEEM_TYPE order by REDEEMT_TYPE_ID*1   asc")
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_redeemTp.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))

                    if column_number == 2:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))

                    self.Qtable_redeemTp.setItem(row_number, column_number, item)
            #self.Qtable_redeemTp.doubleClicked.connect(self.FN_GET_CUSTGP)

            #mycursor.close()
        except Exception as err:
            print(err)

    def FN_GET_REDEEMTYPE(self):
        try:
            if len(self.Qtable_redeemTp.selectedIndexes()) >= 0:
                rowNo = self.Qtable_redeemTp.selectedItems()[0].row()
                id = self.Qtable_redeemTp.item(rowNo, 0).text()
                desc = self.Qtable_redeemTp.item(rowNo, 1).text()
                status = self.Qtable_redeemTp.item(rowNo, 2).text()
                self.LE_desc.setText(desc)
                self.LB_redeemTpId.setText(id)
                self.LB_status.setText(util.FN_GET_STATUS_id(status))
                self.CMB_redeemType.setCurrentText(status)
                # self.FN_MODIFY_CUSTTP()
        except Exception as err:
            print(err)
    def FN_CHECK_DUP_NAME(self,name,id=''):
        self.conn1 = db1.connect()
        mycursor1 = self.conn1.cursor()
        sql = "SELECT REDEEMT_DESC  FROM Hyper1_Retail.REDEEM_TYPE where REDEEMT_DESC = '"+name+"' and REDEEMT_TYPE_ID !='"+id+"'"
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
        status = self.CMB_redeemType.currentText()
        if status == 'Active'  :
            self.LB_status.setText('1')
        else :
            self.LB_status.setText('0')

    def FN_CREATE_REDEEMTP(self):
        self.conn = db1.connect()
        self.name = self.LE_desc.text().strip()
        self.redeemTp = self.CMB_redeemType.currentText()
        if self.redeemTp == 'Active':
            self.status = 1
        else:
            self.status = 0

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(cast(REDEEMT_TYPE_ID  AS UNSIGNED)) FROM Hyper1_Retail.REDEEM_TYPE")
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

                    sql = "INSERT INTO Hyper1_Retail.REDEEM_TYPE  " \
                          "         VALUES ( %s, %s, %s)"

                    # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                    val = (self.id, self.name, self.status                           )
                    mycursor.execute(sql, val)
                    # mycursor.execute(sql)

                    mycursor.close()

                    print(mycursor.rowcount, "Redeem type inserted.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                    db1.connectionCommit(self.conn)
                    self.FN_GET_REDEEMTPS()
                    self.FN_CLEAR_FEILDS()
                    #db1.connectionClose(self.conn)
                    #self.close()
            except Exception as err:
                print(err)

        # insert into db

    def FN_MODIFY_REDEEMTP(self):
        self.conn1 = db1.connect()
        if len(self.Qtable_redeemTp.selectedIndexes()) >0 :
            rowNo = self.Qtable_redeemTp.selectedItems()[0].row()
            id = self.LB_redeemTpId.text().strip()
            desc_old = self.Qtable_redeemTp.item(rowNo, 1).text()
            desc = self.LE_desc.text().strip()
            redeemTp = self.CMB_redeemType.currentText()
            old_status = self.Qtable_redeemTp.item(rowNo, 2).text()
            old_status = util.FN_GET_STATUS_id(str(old_status))
            if redeemTp == 'Active':
                status = 1
            else:
                status = 0
            #
            error = 0
            if desc == '':
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")

            else:
                if desc != desc_old:
                    if self.FN_CHECK_DUP_NAME(desc,id) != False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                        error=1

                if error!=1:
                    mycursor = self.conn1.cursor()

                    sql = "update  Hyper1_Retail.REDEEM_TYPE  set REDEEMT_STATUS= %s ,REDEEMT_DESC = %s   where REDEEMT_TYPE_ID = %s"
                    val = (status,desc, id)
                    mycursor.execute(sql, val)

                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                    db1.connectionCommit(self.conn1)
                    self.FN_GET_REDEEMTPS()

                    self.FN_CLEAR_FEILDS ()
                    if str(status) != str(old_status):
                        util.FN_INSERT_IN_LOG("REDEEM_TYPE", "status", status, old_status,id)
                    if str(desc) != str(desc_old):
                        util.FN_INSERT_IN_LOG("REDEEM_TYPE", "desc", desc, desc_old,id)

        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

    def FN_CLEAR_FEILDS (self):
        self.LB_redeemTpId.clear()
        self.LE_desc.clear()
        self.CMB_redeemType.setCurrentText('Active')
        self.LB_status.setText('1')
