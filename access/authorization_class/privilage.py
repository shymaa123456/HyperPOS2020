from pathlib import Path
from mysql.connector import Error
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi

from data_connection.h1pos import db1
from access.authorization_class.form import CL_form

class CL_privilage( QtWidgets.QDialog ):
    dirname = ''

    def __init__(self):
        super( CL_privilage, self ).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createPrivilage.ui'
        loadUi( filename, self )

        self.BTN_createPrivilage.clicked.connect( self.FN_CREATE_PRIVILAGE )
        self.FN_GET_ROLES()
        #self.FN_GET_FORMS()
        records = CL_form.FN_GET_FORMS(self)
        self.CMB_formName.clear()
        for row in records:
            self.CMB_formName.addItems([row[0]])

        self.FN_GET_ACTIONS()
        self.FN_GET_ROLEID()
        self.FN_GET_FORMID()
        self.FN_GET_ACTIONID()
        self.FN_GET_FORMItems()
        self.FN_GET_FORMITEMID()
        self.FN_DISPLAY_PRIVILAGE()
        self.CMB_roleName.currentIndexChanged.connect( self.FN_GET_ROLEID )
        self.CMB_formName.currentIndexChanged.connect( self.FN_GET_FORMID )
        self.CMB_actionName.currentIndexChanged.connect( self.FN_GET_ACTIONID )
        self.CMB_formItemName.currentIndexChanged.connect( self.FN_GET_FORMITEMID )
        self.BTN_add.clicked.connect( self.FN_ADD_PRIVILAGE )
        self.BTN_delete.clicked.connect( self.FN_DELETE_PRIVILAGE )

    def FN_DELETE_PRIVILAGE(self):
        rows = []
        for idx in self.w1.selectionModel().selectedRows():
            rows.append( idx.row() )
        # print(rows)
        for row in rows:
            self.w1.removeRow( row )
        #QtWidgets.QMessageBox.information( self, "Success", "Privilage is deleted successfully" )

    def FN_ADD_PRIVILAGE(self):
        self.role = self.LB_roleId.text()
        self.form = self.LB_formId.text()

        self.formItem = self.LB_formItemID.text()
        self.roleName = self.CMB_roleName.currentText()
        self.formName = self.CMB_formName.currentText()
        self.actionName = self.CMB_actionName.currentText()
        self.actionId = self.LB_actionId.text()
        self.formItemName = self.CMB_formItemName.currentText()

        x = self.FN_CHECK_DB_AVAILABILITY( self.role, self.form, self.actionId, self.formItem )

        if x == True:
            QtWidgets.QMessageBox.warning( self, "Error", "Privilage already exists" )
        else:

            if self.FN_CHECK_TABLE_WIDGET_AVAILABILITY( self.role, self.form, self.actionId, self.formItem ) == True:
                QtWidgets.QMessageBox.warning( self, "Error", "You already entered this Priviliage in the grid" )
            else:

                rowPosition = self.w1.rowCount()
                self.w1.setRowCount( rowPosition )
                self.w1.insertRow( self.w1.rowCount() )

                self.w1.setItem( rowPosition, 0, QTableWidgetItem( str( self.roleName ) ) )
                self.w1.setItem( rowPosition, 1, QTableWidgetItem( str( self.role ) ) )
                self.w1.setItem( rowPosition, 2, QTableWidgetItem( str( self.formName ) ) )
                self.w1.setItem( rowPosition, 3, QTableWidgetItem( str( self.form ) ) )
                self.w1.setItem( rowPosition, 4, QTableWidgetItem( str( self.actionName ) ) )
                self.w1.setItem( rowPosition, 5, QTableWidgetItem( str( self.formItemName ) ) )

    def FN_CHECK_TABLE_WIDGET_AVAILABILITY(self, var11, var2, var3, var4):

        mycursor = self.conn.cursor()
        allRows = self.w1.rowCount()

        for row in range( 0, allRows ):

            sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT WHERE ACTION_DESC = %s"
            x = (self.w1.item( row, 4 ).text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                actionId = myresult[0]

            formItemName = self.w1.item( row, 5 )
            sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s and ITEM_STATUS  = 1"
            x = (formItemName.text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                formItemId = myresult[0]

            if var11 == self.w1.item( row, 1 ).text() and var2 == self.w1.item( row,  3 ).text() and var3 == actionId and var4 == formItemId:
                return True
        mycursor.close()
        # if chk:
        #     return True

    def FN_CHECK_DB_AVAILABILITY(self, var11, var2, var3, var4):
        # print(var11, var2, var3, var4)
        mycursor = self.conn.cursor()
        sqlStat = "Select  *      " \
                  "from SYS_PRIVILEGE p inner join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  " \
                  "and p.FORM_ID = pi.FORM_ID                 " \
                  "where  p.ROLE_ID = " + var11 + " and p.FORM_ID = " + var2 + " and p.ACTION_ID = " + var3 + " and pi.ITEM_ID=" + var4 + ""
        # print(sqlStat)
        mycursor.execute( sqlStat )

        records = mycursor.fetchall()

        if mycursor.rowcount > 0:
            return True
        else:
            return False

    def FN_GET_ACTIONS(self):
        mycursor = self.conn.cursor()

        mycursor.execute( "SELECT ACTION_DESC FROM SYS_PRINT_EXPORT order by ACTION_ID asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_actionName.addItems( [row[0]] )

        mycursor.close()

    def FN_GET_ROLES(self):
        mycursor = self.conn.cursor()

        mycursor.execute( "SELECT ROLE_NAME FROM SYS_ROLE where ROLE_STATUS =1  order by ROLE_ID asc " )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems( [row[0]] )

        mycursor.close()


    def FN_GET_FORMItems(self):

        mycursor = self.conn.cursor()
        self.CMB_formItemName.clear()

        self.form = self.LB_formId.text()

        sql_select_query = "SELECT ITEM_DESC FROM SYS_FORM_ITEM where ITEM_STATUS  = 1 and FORM_ID = '" + self.form + "'"

        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()

        for row in records:
            self.CMB_formItemName.addItems( [row[0]] )

        mycursor.close()

    def FN_GET_FORMITEMID(self):
        mycursor = self.conn.cursor()
        self.item = self.CMB_formItemName.currentText()

        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s and ITEM_STATUS  = 1 "
        x = (self.item,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formItemID.setText( myresult[0] )

        mycursor.close()

    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_Name = %s and ROLE_STATUS  = 1 "
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_roleId.setText( myresult[0] )

        mycursor.close()
        self.FN_DISPLAY_PRIVILAGE()

    def FN_GET_ROLENAME(self):
        self.role = self.LB_roleId.text()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_DESC FROM SYS_ROLE WHERE ROLE_ID = %s and ROLE_STATUS  = 1"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.CMB_roleName.setText( myresult[0] )

        mycursor.close()

    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s "
        x = (self.form,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formId.setText( myresult[0] )

        mycursor.close()
        self.FN_GET_FORMItems()

    def FN_GET_ACTIONID(self):
        self.action = self.CMB_actionName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT WHERE ACTION_DESC = %s"
        x = (self.action,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_actionId.setText( myresult[0] )

        mycursor.close()


    def FN_DISPLAY_PRIVILAGE(self):
        self.w1.clear()
        self.w1.setRowCount( 0 )
        mycursor = self.conn.cursor()

        self.role = self.LB_roleId.text()
        self.form = self.LB_formId.text()

        sql_select_query = "select r.ROLE_Name , r.ROLE_ID , f.FORM_DESC,f.FORM_ID  ,a.ACTION_DESC ,pi.ITEM_ID " \
                           "from SYS_PRIVILEGE p   " \
                           "inner join SYS_ROLE r on p.ROLE_ID = r.ROLE_ID " \
                           "inner join SYS_FORM f on  p.FORM_ID= f.FORM_ID " \
                           "inner join SYS_PRINT_EXPORT a on p.ACTION_ID = a.ACTION_ID " \
                           " left outer join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  and p.FORM_ID=pi.FORM_ID and pi.ITEM_ID = fi.ITEM_ID  " \
                           " where  p.ROLE_ID = %s and r.ROLE_STATUS  = 1 and f.FORM_STATUS  = 1 "
        print(sql_select_query)
        x = (self.role,)


        mycursor.execute( sql_select_query, x )
        if mycursor.rowcount ==0 :
            sql_select_query = "select r.ROLE_Name , r.ROLE_ID , f.FORM_DESC,f.FORM_ID  ,a.ACTION_DESC ,pi.ITEM_ID " \
                               "from SYS_PRIVILEGE p   " \
                               "inner join SYS_ROLE r on p.ROLE_ID = r.ROLE_ID " \
                               "inner join SYS_FORM f on  p.FORM_ID= f.FORM_ID " \
                               "inner join SYS_PRINT_EXPORT a on p.ACTION_ID = a.ACTION_ID " \
                               "left outer join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  and p.FORM_ID=pi.FORM_ID and pi.ITEM_ID = fi.ITEM_ID  " \
                               " where  p.ROLE_ID = %s and r.ROLE_STATUS  = 1 and f.FORM_STATUS  = 1 "
            print('in if')
            print(sql_select_query)
            x = (self.role,)
            mycursor.execute(sql_select_query, x)
        records = mycursor.fetchall()

        records = list(dict.fromkeys(records))
        print(records)
        for row_number, row_data in enumerate( records ):
            self.w1.insertRow( row_number )

            for column_number, data in enumerate( row_data ):
                self.w1.setItem( row_number, column_number, QTableWidgetItem( str( data ) ) )
        # self.w1.setItem(0, 0, QTableWidgetItem("Name"))

        self.w1.setEditTriggers( QtWidgets.QTableWidget.NoEditTriggers )
        header_labels = ['Role Name', 'Role Id', 'Form Name', 'Form Id', 'Action Name', 'Form Item']
        self.w1.setHorizontalHeaderLabels( header_labels )
        mycursor.close()

    def FN_CREATE_PRIVILAGE(self):
        mycursor = self.conn.cursor( buffered=True )

        self.role = self.LB_roleId.text()
        # delete current role -privilage
        sql_select_query = "SELECT PRIV_ID FROM SYS_PRIVILEGE WHERE ROLE_id = %s"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        if mycursor.rowcount > 0:
            records = mycursor.fetchall()
            for row in records:
                sql_select_query = "SELECT ITEM_ID FROM SYS_PRIVILEG_ITEM WHERE PRIV_ID = '" + row[0] + "'"
                mycursor.execute(sql_select_query)
                myresult = mycursor.fetchone()
                if mycursor.rowcount > 0:
                    sql_select_query = "delete from SYS_PRIVILEG_ITEM where PRIV_ID = '" + row[0] + "'"
                    mycursor.execute( sql_select_query )
                    db1.connectionCommit( self.conn )


                sql_select_query1 = "delete from SYS_PRIVILEGE  where PRIV_ID = '" + row[0] + "'"
                mycursor.execute( sql_select_query1 )
                db1.connectionCommit( self.conn )
                # loop on table widget

        allRows = self.w1.rowCount()
        # if allRows ==0:
        # allRows=1
#
        for row in range( 0, allRows ):
            # # get max userid
            mycursor.execute( "SELECT max(cast(PRIV_ID  AS UNSIGNED)) FROM SYS_PRIVILEGE" )
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int( myresult[0] ) + 1

            roleId = self.w1.item( row, 1 )

            formId = self.w1.item( row, 3 )
            actionName = self.w1.item( row, 4 )

            sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT WHERE ACTION_DESC = %s"
            x = (actionName.text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                actionId = myresult[0]

            sql = "INSERT INTO SYS_PRIVILEGE (PRIV_ID, ROLE_ID,FORM_ID,ACTION_ID)         " \
                  "VALUES ( %s, %s, %s, %s)"
            val = (self.id, roleId.text(), formId.text(), actionId)
            mycursor.execute( sql, val )
            db1.connectionCommit( self.conn )

            formItemName = self.w1.item( row, 5 )
            sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
            x = (formItemName.text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                formItemId = myresult[0]

                sql = "INSERT INTO SYS_PRIVILEG_ITEM (PRIV_ID, FORM_ID,ITEM_ID)         " \
                  "VALUES ( %s, %s, %s)"
                val = (self.id, formId.text(), formItemId)
                mycursor.execute( sql, val )
                print(mycursor.rowcount, "record inserted.")


        db1.connectionCommit( self.conn )
        mycursor.close()

        db1.connectionClose( self.conn )

        self.close()
        QtWidgets.QMessageBox.information( self, "Success", "Privilage is created successfully" )

