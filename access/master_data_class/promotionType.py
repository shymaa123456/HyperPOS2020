from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from access.utils.util import *
from datetime import datetime


class CL_promotionType(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(CL_promotionType, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/master_data_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()

    ###

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/promotionType.ui'
        loadUi(filename, self)

        self.FN_GET_ALL()
        try:
            self.CMB_status.addItems(["Active", "Inactive"])
            self.LB_status.setText('1')
            self.CMB_status.activated.connect(self.FN_GET_STATUS)
            self.BTN_create.clicked.connect(self.FN_CREATE)
            self.BTN_modify.clicked.connect(self.FN_MODIFY)
            #self.Qtable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.BTN_search.clicked.connect(self.FN_SEARCH)
            self.BTN_search_all.clicked.connect(self.FN_GET_ALL)
            #self.setFixedWidth(368)
            #self.setFixedHeight(430)
            self.Qtable.setColumnHidden(0, True)
            self.Qtable.doubleClicked.connect(self.FN_GET_ONE)

            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

        except Exception as err:
            print(err)

    def FN_SEARCH(self):
        self.conn1 = db1.connect()
        try:
            for i in reversed(range(self.Qtable.rowCount())):
                self.Qtable.removeRow(i)

            mycursor = self.conn1.cursor()

            name = self.LE_desc.text().strip()
            status = self.CMB_status.currentText()
            if status == 'Active':

                whereClause = "where `PROMOTION_STATUS` = 1  "
            else:
                whereClause = "where `PROMOTION_STATUS` = 0 "

            if name != '' :
                whereClause = whereClause + "and `PROMT_NAME_AR` like '%" + str(name) + "%'"

            sql_select_query = "select  PROMOTION_TYPE_ID, `PROMT_NAME_AR` , `PROMOTION_STATUS` from Hyper1_Retail.PROMOTION_TYPE " + whereClause + "  order by PROMOTION_TYPE_ID*1 asc"
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable.insertRow(row_number)

                for column_number, data in enumerate(row_data):


                    item = QTableWidgetItem(str(data))

                    if column_number == 2:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable.setItem(row_number, column_number, item)
            #self.Qtable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #
            self.Qtable.doubleClicked.connect(self.FN_GET_ONE)
            #mycursor.close()
        #self.Qtable.setItem(0, 0, QTableWidgetItem(str('11111')))
        except Exception as err:
             print(err)

    def FN_GET_ALL(self):
        self.conn = db1.connect()
        try:
            for i in reversed(range(self.Qtable.rowCount())):
                self.Qtable.removeRow(i)

            mycursor = self.conn.cursor()
            mycursor.execute("SELECT  PROMOTION_TYPE_ID, PROMT_NAME_AR ,PROMOTION_STATUS  FROM Hyper1_Retail.PROMOTION_TYPE   order by PROMOTION_TYPE_ID*1   asc")
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))

                    if column_number == 2:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))

                    self.Qtable.setItem(row_number, column_number, item)
            #self.Qtable.doubleClicked.connect(self.FN_GET_CUSTGP)

            #mycursor.close()
        except Exception as err:
            print(err)

    def FN_GET_ONE(self):
        try:
            if len(self.Qtable.selectedIndexes()) >= 0:
                rowNo = self.Qtable.selectedItems()[0].row()
                id = self.Qtable.item(rowNo, 0).text()
                desc = self.Qtable.item(rowNo, 1).text()
                status = self.Qtable.item(rowNo, 2).text()
                self.LE_desc.setText(desc)
                self.LB_id.setText(id)
                self.LB_status.setText(util.FN_GET_STATUS_id(status))
                self.CMB_status.setCurrentText(status)
                # self.FN_MODIFY_CUSTTP()
        except Exception as err:
            print(err)
    def FN_CHECK_DUP_NAME(self,name,id=''):
        self.conn1 = db1.connect()
        mycursor1 = self.conn1.cursor()
        sql = "SELECT PROMT_NAME_AR  FROM Hyper1_Retail.PROMOTION_TYPE where PROMT_NAME_AR = '"+name+"' and PROMOTION_TYPE_ID !='"+id+"'"
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
        status = self.CMB_status.currentText()
        if status == 'Active'  :
            self.LB_status.setText('1')
        else :
            self.LB_status.setText('0')

    def FN_CREATE(self):
        self.conn = db1.connect()
        self.name = self.LE_desc.text().strip()
        status = self.CMB_status.currentText()
        if status == 'Active':
            self.status = 1
        else:
            self.status = 0

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(cast(PROMOTION_TYPE_ID  AS UNSIGNED)) FROM Hyper1_Retail.PROMOTION_TYPE")
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

                    sql = "INSERT INTO Hyper1_Retail.PROMOTION_TYPE(PROMOTION_TYPE_ID, PROMT_NAME_AR , PROMOTION_STATUS) " \
                          "         VALUES ( %s, %s, %s)"

                    # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                    val = (self.id, self.name,  self.status                          )
                    mycursor.execute(sql, val)
                    # mycursor.execute(sql)

                    mycursor.close()

                    print(mycursor.rowcount, "COMPANY inserted.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                    db1.connectionCommit(self.conn)
                    self.FN_GET_ALL()
                    self.FN_CLEAR_FEILDS()
                    #db1.connectionClose(self.conn)
                    #self.close()
            except Exception as err:
                print(err)
        print("in create company", self.name)

        # insert into db

    def FN_MODIFY(self):
        self.conn1 = db1.connect()
        if len(self.Qtable.selectedIndexes()) >0 :
            rowNo = self.Qtable.selectedItems()[0].row()
            id = self.LB_id.text().strip()
            desc_old = self.Qtable.item(rowNo, 1).text()
            status_old =  self.Qtable.item(rowNo, 0).text()
            desc = self.LE_desc.text().strip()
            status = self.LB_status.text().strip()
            # if status == 'Active':
            #     status = 1
            # else:
            #     status = 0
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
                    sql = "UPDATE `Hyper1_Retail`.`PROMOTION_TYPE` SET `PROMT_NAME_AR` = %s, `PROMOTION_STATUS` = %s WHERE `PROMOTION_TYPE_ID` = %s"
                    val = (desc,status, id)
                    mycursor.execute(sql, val)
                    #mycursor.close()
                    #
                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                    db1.connectionCommit(self.conn1)
                    self.FN_GET_ALL()
                    self.FN_CLEAR_FEILDS ()
                    if str(status) != str(status_old):
                        util.FN_INSERT_IN_LOG("PROMOTION_TYPE", "status", status, status_old, id)
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

    def FN_CLEAR_FEILDS (self):
        self.LB_id.clear()
        self.LE_desc.clear()
        self.CMB_status.setCurrentText('Active')
        self.LB_status.setText('1')
