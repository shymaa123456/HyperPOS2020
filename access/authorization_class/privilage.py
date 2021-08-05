from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox
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
        css_path = Path(__file__).parent.parent.parent

        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())

    #Todo: method to load ui of create privilage
    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createPrivilage.ui'
        loadUi( filename, self )
        self.BTN_createPrivilage.clicked.connect( self.FN_CREATE_PRIVILAGE )
        self.FN_GET_ROLES()
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
        self.CMB_roleName.activated.connect( self.FN_GET_ROLEID )
        self.CMB_formName.activated[str].connect( self.FN_GET_FORMID )
        self.CMB_actionName.activated.connect( self.FN_GET_ACTIONID )
        self.BTN_add.clicked.connect( self.FN_ADD_PRIVILAGE )
        self.BTN_delete.clicked.connect( self.FN_DELETE_PRIVILAGE )

    #Todo: method to delete privilage
    def FN_DELETE_PRIVILAGE(self):
        rows = []
        for idx in self.w1.selectionModel().selectedRows():
            rows.append( idx.row() )
        for row in rows:
            self.w1.removeRow( row )

    #Todo: method to create privilage
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

    #Todo: method to get check TABLE_WIDGET availabilty
    def FN_CHECK_TABLE_WIDGET_AVAILABILITY(self, var11, var2, var3, var4):
        try:
            conn = db1.connect()
            mycursor = conn.cursor()
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
        except Exception as err:
            print(err)

    #Todo: method to get check privilage availabilty
    def FN_CHECK_DB_AVAILABILITY(self, var11, var2, var3, var4):
        conn = db1.connect()
        mycursor = conn.cursor()
        sqlStat = "Select  *      " \
                  "from SYS_PRIVILEGE p inner join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  " \
                  "and p.FORM_ID = pi.FORM_ID                 " \
                  "where  p.ROLE_ID = " + var11 + " and p.FORM_ID = " + var2 + " and p.ACTION_ID = " + var3 + " and pi.ITEM_ID=" + var4 + ""
        mycursor.execute( sqlStat )
        records = mycursor.fetchall()
        if mycursor.rowcount > 0:
            return True
        else:
            return False

    #Todo: method to get action name
    def FN_GET_ACTIONS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT ACTION_DESC FROM SYS_PRINT_EXPORT order by ACTION_ID asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_actionName.addItems( [row[0]] )
        mycursor.close()

    #Todo: method to get role name
    def FN_GET_ROLES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT ROLE_NAME FROM SYS_ROLE where ROLE_STATUS =1  order by ROLE_ID asc " )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems( [row[0]] )
        mycursor.close()

    #Todo: method to get form item name
    def FN_GET_FORMItems(self):
        self.form = self.LB_formId.text()
        self.CMB_formItemName.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT ITEM_DESC FROM SYS_FORM_ITEM where ITEM_STATUS  = 1 and FORM_ID = '" + self.form + "'"
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        print(records )
        for row1 in records:
            self.CMB_formItemName.addItems( [row1[0]] )
        mycursor.close()

    #Todo: method to get form item id
    def FN_GET_FORMITEMID(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.item = self.CMB_formItemName.currentText()
        formId = self.LB_formId.text()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM  WHERE ITEM_DESC = %s and FORM_ID = %s and ITEM_STATUS  = 1 "
        x = (self.item,formId)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formItemID.setText( myresult[0] )
        mycursor.close()

    #Todo: method to get role id
    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_Name = %s and ROLE_STATUS  = 1 "
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_roleId.setText( myresult[0] )
        mycursor.close()
        self.FN_DISPLAY_PRIVILAGE()

    #Todo: method to get role name
    def FN_GET_ROLENAME(self):
        self.role = self.LB_roleId.text()
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT ROLE_DESC FROM SYS_ROLE WHERE ROLE_ID = %s and ROLE_STATUS  = 1"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.CMB_roleName.setText( myresult[0] )
        mycursor.close()

    #Todo: method to get form id
    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s "
        x = (self.form,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formId.setText( myresult[0] )
        mycursor.close()
        self.CMB_formItemName.activated[str].connect(self.FN_GET_FORMITEMID)
        self.FN_GET_FORMItems()
        self.FN_GET_FORMITEMID()

    #Todo: method to get action id
    def FN_GET_ACTIONID(self):
        self.action = self.CMB_actionName.currentText()
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT WHERE ACTION_DESC = %s"
        x = (self.action,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_actionId.setText( myresult[0] )
        mycursor.close()

    #Todo: method to display privilage
    def FN_DISPLAY_PRIVILAGE(self):
        self.w1.clear()
        self.w1.setRowCount( 0 )
        conn = db1.connect()
        mycursor = conn.cursor()
        self.role = self.LB_roleId.text()
        self.form = self.LB_formId.text()
        sql_select_query = "select r.ROLE_Name , r.ROLE_ID , f.FORM_DESC,f.FORM_ID  ,a.ACTION_DESC ,pi.ITEM_ID from SYS_PRIVILEGE p   inner join SYS_ROLE r on p.ROLE_ID = r.ROLE_ID inner join SYS_FORM f on  p.FORM_ID= f.FORM_ID inner join SYS_PRINT_EXPORT a on p.ACTION_ID = a.ACTION_ID  left outer join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  and p.FORM_ID=pi.FORM_ID    where  p.ROLE_ID = %s and r.ROLE_STATUS  = 1 and f.FORM_STATUS  = 1"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        records = mycursor.fetchall()
        records = list(dict.fromkeys(records))
        for row_number, row_data in enumerate( records ):
            self.w1.insertRow( row_number )
            for column_number, data in enumerate( row_data ):
                self.w1.setItem( row_number, column_number, QTableWidgetItem( str( data ) ) )
            val= self.w1.item(row_number,5).text()
            if val == 'None':
                print ('hh')
            else:
                sql_select_query = "select  i.ITEM_DESC from SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                x = (val,)
                mycursor.execute(sql_select_query, x)
                result = mycursor.fetchone()
                self.w1.setItem(row_number, 5, QTableWidgetItem(str(result[0])))
        self.w1.setEditTriggers( QtWidgets.QTableWidget.NoEditTriggers )
        header_labels = ['Role Name', 'Role Id', 'Form Name', 'Form Id', 'Action Name', 'Form Item']
        self.w1.setHorizontalHeaderLabels( header_labels )
        mycursor.close()

    #Todo: method to create privilage
    def FN_CREATE_PRIVILAGE(self):
        conn = db1.connect()
        mycursor = conn.cursor( buffered=True )
        self.role = self.LB_roleId.text()
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
                    db1.connectionCommit( conn )
                sql_select_query1 = "delete from SYS_PRIVILEGE  where PRIV_ID = '" + row[0] + "'"
                mycursor.execute( sql_select_query1 )
                db1.connectionCommit( conn )
        allRows = self.w1.rowCount()
        for row in range( 0, allRows ):
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
            db1.connectionCommit( conn )
            formItemName = self.w1.item( row, 5 )
            sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s and form_ID =%s"
            x = (formItemName.text(),formId.text())
            mycursor.execute( sql_select_query, x )
            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                formItemId = myresult[0]
                sql = "INSERT INTO SYS_PRIVILEG_ITEM (PRIV_ID, FORM_ID,ITEM_ID)         " \
                  "VALUES ( %s, %s, %s)"
                val = (self.id, formId.text(), formItemId)
                mycursor.execute( sql, val )
                print(mycursor.rowcount, "record inserted.")
        db1.connectionCommit( conn )
        mycursor.close()
        db1.connectionClose( conn )
        self.close()
        QtWidgets.QMessageBox.information( self, "Success", "Privilage is created successfully" )

