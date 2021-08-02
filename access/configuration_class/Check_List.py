from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox


class CL_HW_Parameter(QtWidgets.QDialog):

    def __init__(self):
        super(CL_HW_Parameter, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

        # Todo: method to Load data and declare Buttons
    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/HW_Parameter.ui'
        loadUi(filename, self)
        self.setWindowTitle('HW_Parameters')
        self.BTN_createParameter.clicked.connect(self.FN_CREATE_Parameters)
        self.BTN_ModifyParameter.clicked.connect(self.FN_Update_Parameters)
        self.CMB_Status.addItems(["Active", "Inactive"])
        self.FN_DISPLAY_PRIVILAGE()

        # Todo: method to Create Parameter if not Exist
    def FN_CREATE_Parameters(self):
        sql_select_Query = "SELECT * FROM Hyper1_Retail.SYS_HW_COMPONENT where HW_PARAMETER_DESC = '"+self.LE_name.text().strip()+"' and STATUS = 1"
        print(sql_select_Query)
        mycursor = self.conn.cursor()
        mycursor.execute(sql_select_Query)
        print(mycursor.fetchall())
        if mycursor.rowcount>0:
            QtWidgets.QMessageBox.warning(self, "Error", "HW Parameter is already exists")
        else:
            self.name = self.LE_name.text().strip()
            self.Notes = self.LE_Notes.text().strip()
            self.status = self.CMB_Status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0
            mycursor = self.conn.cursor()
            # get max userid
            mycursor.execute("SELECT max(cast(HW_PARAMETER_ID  AS UNSIGNED)) FROM SYS_HW_COMPONENT")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1

            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            if CL_validation.FN_isEmpty(self.name) :
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

            else:
                    sql = "INSERT INTO SYS_HW_COMPONENT (HW_PARAMETER_ID, HW_PARAMETER_DESC , NOTES, CHANGED_ON, CHANGED_BY, STATUS)         VALUES ( %s, %s, %s, %s,%s, %s)"
                    val = (
                        self.id, self.name, self.Notes, creationDate,
                        CL_userModule.user_name,self.status)
                    mycursor.execute(sql, val)
                    mycursor.close()
                    print(mycursor.rowcount, "Record inserted.")
                    QtWidgets.QMessageBox.information(self, "Success", "HW Parameter is created successfully")
                    db1.connectionCommit(self.conn)
                    db1.connectionClose(self.conn)
            self.FN_DISPLAY_PRIVILAGE()

        # Todo: method to display data in GridView
    def FN_DISPLAY_PRIVILAGE(self):
            self.conn = db1.connect()
            self.w1.clear()
            self.w1.setRowCount(0)
            mycursor = self.conn.cursor()
            sql_select_query = "SELECT * FROM SYS_HW_COMPONENT"
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            records = list(dict.fromkeys(records))
            mycursor.close()
            for row_number, row_data in enumerate(records):
                self.w1.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.w1.setItem(row_number, column_number, QTableWidgetItem( str( data ) ) )
                val = self.w1.item(row_number, 5).text()
            self.w1.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            header_labels = ['Parameter ID', 'Name', 'Notes', 'Created Date', 'Created By', 'Status']
            self.w1.setHorizontalHeaderLabels(header_labels)
            self.w1.doubleClicked.connect(self.Fn_Get_selected_row)
            # Todo: method to Get Selected row data and fill it on Textbox
    def Fn_Get_selected_row(self):
        try:
            if len(self.w1.selectedIndexes()) > 0:
                rowNo = self.w1.selectedItems()[0].row()
                id = self.w1.item(rowNo, 0).text()
                desc = self.w1.item(rowNo, 1).text()
                Notes = self.w1.item(rowNo, 2).text()
                status = self.w1.item(rowNo, 5).text()
                if status == '0':
                    status = 'Inactive'
                else:
                    status = 'Active'

                self.LE_name.setText(desc)
                self.LE_Notes.setText(Notes)
                self.CMB_Status.setCurrentText(status)
        except Exception as err:
            print(err)

        # Todo: method Update Parameters
    def FN_Update_Parameters(self):
            self.name = self.LE_name.text().strip()
            self.Notes = self.LE_Notes.text().strip()
            self.status = self.CMB_Status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0

            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            if CL_validation.FN_isEmpty(self.name) :
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

            else:
              try:
                rowNo = self.w1.selectedItems()[0].row()
                desc = self.w1.item(rowNo, 1).text().strip()
                if self.LE_name.text().strip() != desc:
                    QtWidgets.QMessageBox.warning(self, "Error", "Parameter Name Can't be change")
                    return
                else:
                    mycursor = self.conn.cursor()
                    sql = "Update SYS_HW_COMPONENT  set  NOTES = %s, CHANGED_ON  = %s, CHANGED_BY = %s, STATUS = %s where HW_PARAMETER_DESC = %s"
                    val = (self.Notes, creationDate,
                        CL_userModule.user_name,self.status,self.name)
                    mycursor.execute(sql, val)
                    mycursor.close()
                    print(mycursor.rowcount, "Record Updated.")
                    QtWidgets.QMessageBox.information(self, "Success", "HW Parameter is Updated successfully")
                    db1.connectionCommit(self.conn)
                    db1.connectionClose(self.conn)
                    self.LE_name.setText("")
                    self.LE_Notes.setText("")
              except Exception as err:
                print(err)
            self.FN_DISPLAY_PRIVILAGE()



