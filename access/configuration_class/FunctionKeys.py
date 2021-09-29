from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from access.utils.util import *
from datetime import datetime


class CL_FunctionKey(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(CL_FunctionKey, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/master_data_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()

    ###
    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/FunctionK.ui'
        loadUi(filename, self)

        self.BTN_create.clicked.connect(self.FN_CREATE)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())


    def FN_CREATE(self):
        self.conn = db1.connect()

        if self.LE_Front_Buttons_Name.text().strip() == '' or self.LE_Front_Buttons_Form.text().strip() == '' \
                or self.LE_Front_Functions_Name.text().strip() == '' or self.LE_Front_Functions_Text.text().strip() == '' :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال ")

        else:
            try:
                    mycursor = self.conn.cursor()
                #if self.FN_CHECK_DUP_NAME(self.name) != False:
                #    QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                #    mycursor.close()
                #else:
                    #insert Front_Buttons
                    mycursor.execute("SELECT max(cast(Front_Buttons_ID  AS UNSIGNED)) FROM Hyper1_Retail.Front_Buttons")
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        Front_Buttons_ID = "1"
                    else:
                       Front_Buttons_ID = int(myresult[0]) + 1

                    creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "INSERT INTO Hyper1_Retail.Front_Buttons(Front_Buttons_ID, Front_Buttons_Name , Front_Buttons_Form) " \
                          " VALUES (%s,  %s, %s)"

                    val = (Front_Buttons_ID,self.LE_Front_Buttons_Name.text().strip() , self.LE_Front_Buttons_Form.text().strip() )
                    mycursor.execute(sql, val)

                    #insert Front_Functions
                    mycursor.execute("SELECT max(cast(Front_Functions_ID  AS UNSIGNED)) FROM Hyper1_Retail.Front_Functions")
                    myresult = mycursor.fetchone()

                    if myresult[0] == None:
                        Front_Functions_ID = "1"
                    else:
                        Front_Functions_ID = int(myresult[0]) + 1

                    creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "INSERT INTO Hyper1_Retail.Front_Functions(Front_Functions_ID, Front_Functions_Name , Front_Functions_Text) " \
                          " VALUES (%s,  %s, %s)"

                    val = (Front_Functions_ID, self.LE_Front_Functions_Name.text().strip(),
                            self.LE_Front_Functions_Text.text().strip())
                    mycursor.execute(sql, val)

                    print(mycursor.rowcount, "Front_Functions  inserted.")

                    #insert Front_Functions_Buttons
                    sql = "INSERT INTO Hyper1_Retail.Front_Functions_Buttons(Front_Functions_ID , Front_Buttons_ID) " \
                          " VALUES (%s,  %s)"

                    val = (Front_Functions_ID, Front_Buttons_ID )
                    mycursor.execute(sql, val)

                    print(mycursor.rowcount, "Front_Functions_Buttons  inserted.")

                    QtWidgets.QMessageBox.information(self, "بنجاح", "تم الإنشاء")
                    db1.connectionCommit(self.conn)


                    mycursor.close()
                    #db1.connectionClose(self.conn)
                    #self.close()
            except Exception as err:
                print(err)

    def FN_SEARCH(self):
        self.conn1 = db1.connect()
        try:
            for i in reversed(range(self.Qtable.rowCount())):
                self.Qtable.removeRow(i)

            mycursor = self.conn1.cursor()
            name = self.LE_desc.text().strip()
            status = self.CMB_status.currentData()
            whereClause = " where Bank_Status = "+status
            if name != '' :
                whereClause = whereClause + " and `Bank_Desc` like '%" + str(name) + "%' "

            sql_select_query = "SELECT  Bank_ID,`Bank_Desc`, `Bank_Status`,Bank_Account_No,Bank_Address FROM Hyper1_Retail.BANK " + whereClause + "  order by Bank_ID*1 asc"
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
        except Exception as err:
             print(err)

    def FN_GET_ALL(self):
        self.conn = db1.connect()
        try:
            for i in reversed(range(self.Qtable.rowCount())):
                self.Qtable.removeRow(i)

            mycursor = self.conn.cursor()
            mycursor.execute("SELECT  Bank_ID,`Bank_Desc`, `Bank_Status` ,Bank_Account_No,Bank_Address FROM Hyper1_Retail.BANK order by Bank_ID*1   asc")
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
        except Exception as err:
            print(err)

    def FN_GET_ONE(self):
        try:
            if len(self.Qtable.selectedIndexes()) >= 0:
                rowNo = self.Qtable.selectedItems()[0].row()
                id = self.Qtable.item(rowNo, 0).text()
                desc = self.Qtable.item(rowNo, 1).text()
                status = self.Qtable.item(rowNo, 2).text()
                accountNo= self.Qtable.item(rowNo, 3).text()
                address = self.Qtable.item(rowNo, 4).text()

                self.LE_desc.setText(desc)
                self.LB_id.setText(id)
                self.LB_status.setText(util.FN_GET_STATUS_id(status))
                self.CMB_status.setCurrentText(status)
                self.LE_accountNo.setText(accountNo)
                self.LE_address.setText(address)


        except Exception as err:
            print(err)
    def FN_CHECK_DUP_NAME(self,name,id=''):
        self.conn1 = db1.connect()
        mycursor1 = self.conn1.cursor()
        sql = "SELECT Bank_Desc  FROM Hyper1_Retail.BANK where Bank_Desc = '"+name+"' and Bank_ID !='"+id+"'"
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

    def FN_GET_Bank_Status(self):
        status = self.CMB_status.currentText()
        if status == 'Active'  :
            self.LB_status.setText('1')
        else :
            self.LB_status.setText('0')

    def FN_MODIFY(self):
        try:
            self.conn1 = db1.connect()
            if len(self.Qtable.selectedIndexes()) >0 :
                rowNo = self.Qtable.selectedItems()[0].row()
                id = self.LB_id.text().strip()
                desc_old = self.Qtable.item(rowNo, 1).text()
                status_old =  self.Qtable.item(rowNo, 2).text()
                desc = self.LE_desc.text().strip()
                status = self.LB_status.text().strip()
                accountNo = self.LE_accountNo.text().strip()
                address = self.LE_address.text().strip()

                error = 0
                if desc == '' or accountNo == '':
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الأسم و رقم الحساب")

                else:
                    if desc != desc_old:
                        if self.FN_CHECK_DUP_NAME(desc,id) != False:
                            QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                            error=1

                    if error!=1:
                        mycursor = self.conn1.cursor()
                        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                        sql = "UPDATE Hyper1_Retail.BANK SET `Bank_Desc` = %s, Bank_Status = %s ,Bank_Account_No=%s , Bank_Address=%s ,Bank_Changed_By=%s,Bank_Changed_On = %s " \
                              " WHERE Bank_ID = %s"
                        val = (desc,status, accountNo,address,CL_userModule.user_name,changeDate,id)
                        mycursor.execute(sql, val)
                        #mycursor.close()
                        #
                        print(mycursor.rowcount, "record updated.")
                        QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                        db1.connectionCommit(self.conn1)
                        self.FN_GET_ALL()
                        self.FN_CLEAR_FEILDS ()
                        if str(status) != str(status_old):
                            util.FN_INSERT_IN_LOG("Bank", "status", status, status_old, id)
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")
        except Exception as err:
                print(err)
    def FN_CLEAR_FEILDS (self):
        self.LB_id.clear()
        self.LE_desc.clear()
        self.LE_accountNo.clear()
        self.LE_address.clear()
        self.CMB_status.setCurrentText('Active')
        self.LB_status.setText('1')
