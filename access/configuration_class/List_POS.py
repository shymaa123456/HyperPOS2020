from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from Validation.Validation import CL_validation
from access.Checkable import CheckableComboBox
from access.authorization_class.user_module import CL_userModule
from access.configuration_class.List import CL_List
from data_connection.h1pos import db1
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox


class CL_List_POS(QtWidgets.QDialog):

    def __init__(self):
        super(CL_List_POS, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/List_POS.ui'
        loadUi(filename, self)

        self.Qcombo_List = CheckableComboBox(self)
        self.Qcombo_List.setGeometry(210, 130, 280, 25)
        self.Qcombo_List.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_List.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Parameter()

        self.Qcombo_Comapny = CheckableComboBox(self)
        self.Qcombo_Comapny.setGeometry(210, 180, 280, 25)
        self.Qcombo_Comapny.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_Comapny.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Company()

        self.Qcombo_Branch = CheckableComboBox(self)
        self.Qcombo_Branch.setGeometry(210, 220, 280, 25)
        self.Qcombo_Branch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Qcombo_Branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_Branchs()

        self.setWindowTitle('list')
        self.BTN_CreateList.clicked.connect(self.FN_CREATEList)
        self.BTN_ModifyList.clicked.connect(self.FN_ModifyList)
        self.CMB_Status.addItems(["Active", "Inactive"])
        self.FN_DISPLAY_PRIVILAGE()

    def FN_GET_Parameter(self):
        # Todo: method for fills the Parameter combobox
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT distinct LIST_DESC , LIST_ID  FROM Hyper1_Retail.SYS_CKECK_LIST")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_List.addItem(row, val)
        mycursor.close()

    def FN_GET_Company(self):
        # Todo: method for fills the Parameter combobox
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT distinct COMPANY_DESC , COMPANY_ID  FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_Comapny.addItem(row, val)
        mycursor.close()

    def FN_GET_Branchs(self):
        # Todo: method for fills the Parameter combobox
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT distinct BRANCH_DESC_A , BRANCH_NO  FROM BRANCH")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_Branch.addItem(row, val)
        mycursor.close()

    def FN_CREATEList(self):
        if len(self.Qcombo_List.currentData()) == 0:
            QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
        sql_select_Query = "SELECT * FROM Hyper1_Retail.SYS_CKECK_LIST_POS where  STATUS = 2"
        print(sql_select_Query)
        mycursor = self.conn.cursor()
        mycursor.execute(sql_select_Query)
        print(mycursor.fetchall())
        if mycursor.rowcount > 0:
            QtWidgets.QMessageBox.warning(self, "Error", "List is already exists")
        else:
            self.name = self.LE_name.text().strip()
            # self.Notes = self.LE_Notes.text().strip()
            self.status = self.CMB_Status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0
            mycursor = self.conn.cursor()
            # get max userid
            # mycursor.execute("SELECT max(cast(LIST_ID  AS UNSIGNED)) FROM Hyper1_Retail.SYS_CKECK_LIST")
            # myresult = mycursor.fetchone()

            # if myresult[0] == None:
            #    self.id = "1"
            # else:
            #    self.id = int(myresult[0]) + 1

            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            if CL_validation.FN_isEmpty(self.name):
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

            else:
                #sql = "INSERT INTO Hyper1_Retail.SYS_CKECK_LIST_POS (POS_NO, Company_ID,BRANCH_NO,LIST_ID , CHANGED_ON, CHANGED_BY, STATUS)         VALUES ( %s, %s, %s, %s,%s, %s, %s)"
                #val = (
                #    self.name, self.Notes, creationDate,
                #    CL_userModule.user_name, self.status)
                #mycursor.execute(sql, val)

                for i in range(len(self.Qcombo_Comapny.currentData())):
                    for j in range(len(self.Qcombo_Branch.currentData())):
                        for x in range(len(self.Qcombo_List.currentData())):
                            sql3 = "INSERT INTO Hyper1_Retail.SYS_CKECK_LIST_POS (POS_NO, Company_ID,BRANCH_NO,LIST_ID , CHANGED_ON, CHANGED_BY, STATUS)         VALUES ( %s, %s, %s, %s,%s, %s, %s)"
                            val3 = (self.name,
                                    self.Qcombo_Comapny.currentData()[i],
                                    self.Qcombo_Branch.currentData()[j],
                                    self.Qcombo_List.currentData()[x],
                                    creationDate,
                                    CL_userModule.user_name, self.status)
                            mycursor.execute(sql3, val3)

                mycursor.close()
                print(mycursor.rowcount, "Record inserted.")
                QtWidgets.QMessageBox.information(self, "Success", "List is created successfully")
                db1.connectionCommit(self.conn)
                db1.connectionClose(self.conn)
            self.FN_DISPLAY_PRIVILAGE()

    def FN_DISPLAY_PRIVILAGE(self):
        self.conn = db1.connect()
        self.w1.clear()
        self.w1.setRowCount(0)
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT * FROM Hyper1_Retail.SYS_CKECK_LIST_POS"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        records = list(dict.fromkeys(records))
        mycursor.close()
        for row_number, row_data in enumerate(records):
            self.w1.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.w1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            val = self.w1.item(row_number, 5).text()
        self.w1.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header_labels = ['POS ID', 'Company', 'Branch','List', 'Created Date', 'Created By', 'Status']
        self.w1.setHorizontalHeaderLabels(header_labels)
        self.w1.doubleClicked.connect(self.Fn_Get_selected_row)

    def Fn_Get_selected_row(self):
        try:
            if len(self.w1.selectedIndexes()) > 0:
                rowNo = self.w1.selectedItems()[0].row()
                id = self.w1.item(rowNo, 0).text()
                company = self.w1.item(rowNo, 1).text()
                branch = self.w1.item(rowNo, 2).text()
                list = self.w1.item(rowNo, 3).text()
                status = self.w1.item(rowNo, 6).text()
                if status == '0':
                    status = 'Inactive'
                else:
                    status = 'Active'

                self.LE_name.setText(id)
                self.CMB_Status.setCurrentText(status)

        except Exception as err:
            print(err)

    def FN_ModifyList(self):
        self.name = self.LE_name.text().strip()
        self.status = self.CMB_Status.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if CL_validation.FN_isEmpty(self.name):
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        else:
            try:
                rowNo = self.w1.selectedItems()[0].row()
                desc = self.w1.item(rowNo, 0).text().strip()
                if self.LE_name.text().strip() != desc:
                    QtWidgets.QMessageBox.warning(self, "Error", "List Name Can't be change")
                    return
                else:
                    mycursor = self.conn.cursor()
                    sql = "delete  from Hyper1_Retail.SYS_CKECK_LIST_POS   where POS_NO = %s "
                    val = (desc,)
                    mycursor.execute(sql, val)
                    mycursor.close()

                    self.FN_CREATEList()

                    db1.connectionCommit(self.conn)
                    db1.connectionClose(self.conn)

                    QtWidgets.QMessageBox.information(self, "Success", "List is Updated successfully")

                    self.LE_name.setText("")
            except Exception as err:
                print(err)
        self.FN_DISPLAY_PRIVILAGE()
