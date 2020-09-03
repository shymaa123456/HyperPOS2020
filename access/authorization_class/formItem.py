from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from data_connection.h1pos import db1


class CL_formItem( QtWidgets.QDialog ):
    dirname = ''

    def __init__(self):
        super( CL_formItem, self ).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        self.conn = db1.connect()

    # def FN_DISPLAY_FORM_ITEMS(self):
    #     self.w1.clear()
    #
    #     mycursor = self.conn.cursor()
    #     self.form = self.CMB_formId.currentText()
    #
    #     sql_select_query = "select ITEM_DESC , ITEM_STATUS from SYS_FORM_ITEM where FORM_ID = '"+self.form+"'"
    #
    #     mycursor.execute(sql_select_query)
    #     records = mycursor.fetchall()
    #     for row_number, row_data in enumerate(records):
    #         self.w1.insertRow(row_number)
    #
    #         for column_number, data in enumerate(row_data):
    #
    #             self.w1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    #     # self.w1.setItem(0, 0, QTableWidgetItem("Name"))
    #     db1.connectionClose(self.conn)

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createFormItem.ui'
        loadUi( filename, self )

        self.BTN_createFormItem.clicked.connect( self.FN_CREATE_FORM_ITEM )
        self.CMB_formItemStatus.addItems( ["0", "1"] )
        self.CMB_formName.currentIndexChanged.connect( self.FN_GET_FORMID )
        self.FN_GET_FORMS()
        self.FN_GET_FORMID()

    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyFormItem.ui'
        loadUi( filename, self )

        self.BTN_modifyFormItem.clicked.connect( self.FN_MODIFY_FORM )
        self.CMB_formItemStatus.addItems( ["0", "1"] )

        self.CMB_formItemName.currentIndexChanged.connect( self.FN_GET_FORM_ITEM )
        self.CMB_formName.currentIndexChanged.connect( self.FN_GET_FORMID )
        self.FN_GET_FORMItems()
        self.FN_GET_FORM_ITEM()

    def FN_GET_FORMS(self):
        self.CMB_formName.clear()
        # self.item=  self.LB_formItemID.text()

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT FORM_DESC FROM SYS_FORM  order by FORM_ID asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formName.addItems( [row[0]] )

        mycursor.close()

    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()

        mycursor = self.conn.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s"
        x = (self.form,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formID.setText( myresult[0] )

        mycursor.close()

    def FN_GET_FORMITEMID(self):
        self.item = self.CMB_formItemName.currentText()

        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
        x = (self.item,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        self.LB_formItemID.setText( myresult[0] )

        mycursor.close()

    def FN_CREATE_FORM_ITEM(self):
        self.desc = self.LE_desc.text()
        self.form = self.LB_formID.text()

        self.status = self.CMB_formItemStatus.currentText()

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute( "SELECT max(ITEM_ID) FROM SYS_FORM_ITEM" )
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int( myresult[0] ) + 1

        sql = "INSERT INTO SYS_FORM_ITEM (ITEM_ID,FORM_ID,ITEM_DESC, ITEM_STATUS)  VALUES ( %s, %s, %s, %s)"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (self.id, self.form, self.desc, self.status)
        mycursor.execute( sql, val )
        # mycursor.execute(sql)
        db1.connectionCommit( self.conn )
        mycursor.close()
        db1.connectionClose( self.conn )

        print( mycursor.rowcount, "record inserted." )

        self.close()

    def FN_GET_FORMItems(self):
        mycursor = self.conn.cursor()

        mycursor.execute( "SELECT ITEM_DESC FROM SYS_FORM_ITEM order by FORM_ID asc" )
        records = mycursor.fetchall()

        for row in records:
            self.CMB_formItemName.addItems( [row[0]] )

        mycursor.close()

    def FN_GET_FORM_ITEM(self):
        self.FN_GET_FORMITEMID()
        self.id = self.LB_formItemID.text()
        self.FN_GET_FORMS()
        self.FN_GET_FORMID()
        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_FORM_ITEM where ITEM_ID = %s"
        x = (self.id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()

        self.LE_desc.setText( record[2] )
        self.CMB_formName.setCurrentText( record[1] )

        self.CMB_formItemStatus.setCurrentText( record[3] )

        mycursor.close()

        print( mycursor.rowcount, "record retrieved." )

    def FN_MODIFY_FORM(self):
        self.id = self.LB_formItemID.text()
        self.form = self.LB_formID.text()
        self.desc = self.LE_desc.text()
        self.status = self.CMB_formItemStatus.currentText()

        mycursor = self.conn.cursor()

        sql = "UPDATE SYS_FORM_ITEM  set FORM_ID= %s ,ITEM_DESC= %s  , ITEM_STATUS = %s where ITEM_id= %s "

        val = (self.form, self.desc, self.status, self.id)

        mycursor.execute( sql, val )
        mycursor.close()
        db1.connectionCommit( self.conn )
        db1.connectionClose( self.conn )

        print( mycursor.rowcount, "record Modified." )

        self.close()
