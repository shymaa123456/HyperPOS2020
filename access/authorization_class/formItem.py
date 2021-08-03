from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from data_connection.h1pos import db1


class CL_formItem(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_formItem, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'

        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        self.conn = db1.connect()

    #Todo: method to load ui of create formitem
    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createFormItem.ui'
        loadUi(filename, self)
        self.BTN_createFormItem.clicked.connect(self.FN_CREATE_FORM_ITEM)
        self.CMB_formItemStatus.addItems(["Active", "Inactive"])
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.FN_GET_FORMS()

    #Todo: method to load ui of create modifyFormItem
    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyFormItem.ui'
        loadUi(filename, self)
        self.BTN_modifyFormItem.clicked.connect(self.FN_MODIFY_FORM)
        self.CMB_formItemStatus.addItems(["Active", "Inactive"])
        self.FN_GET_FORMS()
        self.FN_GET_FORMID()
        self.FN_GET_FORMItems()
        self.CMB_formItemName.currentIndexChanged.connect(self.FN_GET_FORM_ITEM)
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMItems)

    #Todo: method get forms name and id
    def FN_GET_FORMS(self):
        self.CMB_formName.clear()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT FORM_DESC , FORM_ID FROM SYS_FORM   order by FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formName.addItems([row[0]])
        mycursor.close()

    #Todo: method get forms id
    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s "
        x = (self.form,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formID.setText(myresult[0])
            print("form id id", myresult[0])
        mycursor.close()

    #Todo: method get FORMITEMID
    def FN_GET_FORMITEMID(self):
        self.item = self.CMB_formItemName.currentText()
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s "
        x = (self.item,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formItemID.setText(myresult[0])
       # mycursor.close()

    #Todo: method to create FORMITEMID
    def FN_CREATE_FORM_ITEM(self):
        self.desc = self.LE_desc.text().strip()
        self.form = self.LB_formID.text()
        self.status = self.CMB_formItemStatus.currentText()
        if self.status == 'Active':
            self.status = '1'
        else:
            self.status = '0'
        if self.desc == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please all required field")
        else:
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT max(cast(ITEM_ID  AS UNSIGNED)) FROM SYS_FORM_ITEM")
            myresult = mycursor.fetchone()
            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1
            sql = "INSERT INTO SYS_FORM_ITEM (ITEM_ID,FORM_ID,ITEM_DESC, ITEM_STATUS)  VALUES ( %s, %s, %s, %s)"
            val = (self.id, self.form, self.desc, self.status)
            mycursor.execute(sql, val)
            db1.connectionCommit(self.conn)
            mycursor.close()
            db1.connectionClose(self.conn)
            print(mycursor.rowcount, "record inserted.")
            self.close()
            QtWidgets.QMessageBox.information(self, "Success", "Form Item is created successfully")

    #Todo: method to get FORMITEM desc assigned to form
    def FN_GET_FORMItems(self):
        self.CMB_formItemName.clear()
        self.LE_desc.setText('')
        mycursor = self.conn.cursor('')
        self.FN_GET_FORMID()
        formId = self.LB_formID.text()
        sqlQuery = 'SELECT ITEM_DESC FROM SYS_FORM_ITEM where FORM_ID = %s '
        val = (formId,)
        mycursor.execute(sqlQuery, val)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formItemName.addItems([row[0]])
        mycursor.close()
        self.FN_GET_FORMITEMID()
        self.FN_GET_FORM_ITEM()

    #Todo: method to get FORMITEM ITEM_DESC
    def FN_GET_FORM_ITEM(self):
        conn = db1.connect()
        self.LE_desc.clear()
        self.FN_GET_FORMITEMID()
        self.id = self.LB_formItemID.text()
        mycursor = conn.cursor()
        sql_select_query = "select ITEM_DESC ,ITEM_STATUS from SYS_FORM_ITEM where ITEM_ID = %s "
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchall()
        for row in record:
            self.LE_desc.setText(row[0])
            if row[1] == '1':
                self.CMB_formItemStatus.setCurrentText('Active')
            else:
                self.CMB_formItemStatus.setCurrentText('Inactive')
        mycursor.close()
        print(mycursor.rowcount, "record retrieved.")

    #Todo: method to modify form
    def FN_MODIFY_FORM(self):
        self.id = self.LB_formItemID.text()
        self.form = self.LB_formID.text()
        self.desc = self.LE_desc.text().strip()
        self.status = self.CMB_formItemStatus.currentText()
        if self.status == 'Active':
            self.status = '1'
        else:
            self.status = '0'
        if self.desc == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please all required field")
        else:
            mycursor = self.conn.cursor()
            sql = "UPDATE SYS_FORM_ITEM  set FORM_ID= %s ,ITEM_DESC= %s  , ITEM_STATUS = %s where ITEM_id= %s "
            val = (self.form, self.desc, self.status, self.id)
            mycursor.execute(sql, val)
            mycursor.close()
            db1.connectionCommit(self.conn)
            db1.connectionClose(self.conn)
            print(mycursor.rowcount, "record Modified.")
            self.close()
            QtWidgets.QMessageBox.information(self, "Success", "Form Item is modified successfully")
