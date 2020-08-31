import sys

import PyQt5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector
import os
import sys
from pathlib import Path

from data_connection.h1pos import db1


class CL_privilage(QtWidgets.QDialog):
    dirname=''
    def __init__(self):
        super(CL_privilage, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        #


    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createPrivilage.ui'
        loadUi( filename, self )

        self.BTN_createPrivilage.clicked.connect(self.FN_CREATE_PRIVILAGE)
        self.FN_GET_ROLES()
        self.FN_GET_FORMS()
        self.FN_GET_ACTIONS()
        self.FN_GET_ROLEID()
        self.FN_GET_FORMID()
        self.FN_GET_ACTIONID()
        self.FN_GET_FORMItems()
        self.FN_GET_FORMITEMID()
        self.FN_DISPLAY_PRIVILAGE()
        self.CMB_roleName.currentIndexChanged.connect(self.FN_GET_ROLEID)
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.CMB_actionName.currentIndexChanged.connect(self.FN_GET_ACTIONID)
        self.CMB_formItemName.currentIndexChanged.connect(self.FN_GET_FORMITEMID)
        self.BTN_add.clicked.connect(self.FN_ADD_PRIVILAGE)
        self.BTN_delete.clicked.connect(self.FN_DELETE_PRIVILAGE)
    def FN_DELETE_PRIVILAGE (self):
        rows = []
        for idx in self.w1.selectionModel().selectedRows():
            rows.append( idx.row() )
        #print(rows)
        for row in rows:
            self.w1.removeRow( row )

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
            print("in else")
            if self.FN_CHECK_TABLE_WIDGET_AVAILABILITY(self.role, self.form, self.actionId, self.formItem) == True :
                QtWidgets.QMessageBox.warning( self, "Error", "You already entered this Priviliage in the grid" )
            else:

                rowPosition = self.w1.rowCount()
                self.w1.setRowCount( rowPosition )
                self.w1.insertRow( self.w1.rowCount())

                self.w1.setItem( rowPosition, 0, QTableWidgetItem( str(self.roleName) ) )
                self.w1.setItem( rowPosition, 1, QTableWidgetItem( str( self.role ) ) )
                self.w1.setItem( rowPosition, 2, QTableWidgetItem( str( self.formName ) ) )
                self.w1.setItem( rowPosition, 3, QTableWidgetItem( str( self.form ) ) )
                self.w1.setItem( rowPosition, 4, QTableWidgetItem( str( self.actionName ) ) )
                self.w1.setItem( rowPosition, 5, QTableWidgetItem( str( self.formItemName ) ) )
    def FN_CHECK_TABLE_WIDGET_AVAILABILITY(self,var11, var2, var3, var4):

        mycursor = db1.connect( self )
        allRows = self.w1.rowCount()

        for row in range( 0, allRows ):

            sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT_LOOKUP WHERE ACTION_DESC = %s"
            x = (self.w1.item( row, 4 ).text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                actionId = myresult[0]

            formItemName = self.w1.item( row, 5 )
            sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
            x = (formItemName.text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                formItemId = myresult[0]

            if var11 == self.w1.item( row, 1 ).text() and var2 ==self.w1.item( row, 3 ).text()and var3 == actionId and var4 == formItemId:
               return True

        # if chk:
        #     return True



    def FN_CHECK_DB_AVAILABILITY(self,var11, var2, var3, var4):
        #print(var11, var2, var3, var4)
        mycursor = db1.connect(self)
        sqlStat= "Select  *      " \
                 "from SYS_PRIVILEGE p inner join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  " \
                 "and p.FORM_ID = pi.FORM_ID                 " \
                 "where  p.ROLE_ID = "+var11+" and p.FORM_ID = "+var2+" and p.ACTION_ID = "+var3+" and pi.ITEM_ID="+var4+""
        #print(sqlStat)
        mycursor.execute( sqlStat )

        records = mycursor.fetchall()

        if mycursor.rowcount > 0:
            return True
        else:
            return False

    def FN_GET_ACTIONS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ACTION_DESC FROM SYS_PRINT_EXPORT_LOOKUP order by ACTION_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_actionName.addItems([row[0]])


        connection.close()
        mycursor.close()
    def FN_GET_ROLES(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ROLE_NAME FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems([row[0]])


        connection.close()
        mycursor.close()

    def FN_GET_FORMS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT FORM_DESC FROM SYS_FORM order by FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formName.addItems([row[0]])


        connection.close()
        mycursor.close()

    def FN_GET_FORMItems(self):
        self.CMB_formItemName.clear()
        connection = mysql.connector.connect( host='localhost', database='PosDB'

                                              , user='root', password='password', port='3306' )
        self.form = self.LB_formId.text()
        mycursor = connection.cursor()
        sql_select_query = "SELECT ITEM_DESC FROM SYS_FORM_ITEM where  FORM_ID = %s"
        x = (self.form,)
        mycursor.execute( sql_select_query, x )
        records = mycursor.fetchall()

        for row in records:
            self.CMB_formItemName.addItems( [row[0]] )
        connection.close()
        mycursor.close()

    def FN_GET_FORMITEMID(self):
        self.item= self.CMB_formItemName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
        x = (self.item,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formItemID.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_Name = %s"
        x = (self.role,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_roleId.setText(myresult[0])
        connection.close()
        mycursor.close()
        self.FN_DISPLAY_PRIVILAGE()
    def FN_GET_ROLENAME(self):
        self.role = self.LB_roleId.text()
        connection = mysql.connector.connect( host='localhost', database='PosDB'
                                              , user='root', password='password', port='3306' )
        mycursor = connection.cursor()
        sql_select_query = "SELECT ROLE_DESC FROM SYS_ROLE WHERE ROLE_ID = %s"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.CMB_roleName.setText( myresult[0] )
        connection.close()
        mycursor.close()

    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formId.setText(myresult[0])

        connection.close()
        mycursor.close()
        self.FN_GET_FORMItems()
    def FN_GET_ACTIONID(self):
        self.action = self.CMB_actionName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT_LOOKUP WHERE ACTION_DESC = %s"
        x = (self.action,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_actionId.setText(myresult[0])

        connection.close()
        mycursor.close()
    # def FN_GET_PRIV(self):
    #
    #     self.id = self.LE_id.text()
    #     self.FN_GET_ROLES()
    #     self.FN_GET_FORMS()
    #     self.FN_GET_ACTIONS()
    #     # self.FN_GET_ROLEID()
    #     # self.FN_GET_FORMID()
    #     # self.FN_GET_ACTIONID()
    #     connection = mysql.connector.connect(host='localhost', database='PosDB'
    #                                          , user='root', password='password', port='3306')
    #     mycursor = connection.cursor()
    #     sql_select_query = "select * from SYS_PRIVILEGE where PRIV_ID = %s"
    #     x = (self.id,)
    #     mycursor.execute(sql_select_query, x)
    #     record = mycursor.fetchone()
    #
    #     self.LB_roleId.setText(record[1])
    #     self.LB_formId.setText(record[2])
    #     self.LB_actionId.setText(record[3])
    #    # self.FN_GET_ROLENAME()
    #     #self.CMB_roleName.setCurrentIndex(self,1)
    #     connection.close()
    #     mycursor.close()
    #
    #     print(mycursor.rowcount, "record retrieved.")

    # def FN_LOAD_MODFIY(self):
    #     filename = self.dirname + '/modifyPrivilage.ui'
    #     loadUi( filename, self )
    #     self.LE_id.textChanged.connect( self.FN_GET_PRIV )
    #     self.BTN_modifyPrivilage.clicked.connect( self.FN_MODIFY_PRIV )
    #     self.CMB_roleName.currentIndexChanged.connect( self.FN_GET_ROLEID )
    #     self.CMB_formName.currentIndexChanged.connect( self.FN_GET_FORMID )
    #     self.CMB_actionName.currentIndexChanged.connect( self.FN_GET_ACTIONID )
    # def FN_MODIFY_PRIV(self):
    #     self.id = self.LE_id.text()
    #     self.role = self.LB_roleId.text()
    #     self.form = self.LB_formId.text()
    #     self.action = self.LB_actionId.text()
    #
    #     #         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
    #     connection = mysql.connector.connect(host='localhost', database='PosDB'
    #                                          , user='root', password='password', port='3306')
    #
    #     mycursor = connection.cursor()
    #
    #
    #     sql = "UPDATE SYS_PRIVILEGE  set ROLE_ID= %s ,  FORM_ID= %s  ,  ACTION_ID= %s  where PRIV_ID= %s "
    #
    #     val = (self.role , self.form,   self.action, self.id)
    #
    #     mycursor.execute(sql, val)
    #     # mycursor.execute(sql)
    #     connection.commit()
    #
    #     connection.close()
    #     mycursor.close()
    #
    #     print(mycursor.rowcount, "record Modified.")
    #
    #     self.close()
    def FN_DISPLAY_PRIVILAGE(self):
        self.w1.clear()
        self.w1.setRowCount(0)
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        self.role = self.LB_roleId.text()
        self.form = self.LB_formId.text()

        sql_select_query = "select r.ROLE_Name , r.ROLE_ID , f.FORM_DESC,f.FORM_ID  ,a.ACTION_DESC ,fi.ITEM_DESC " \
                           "from SYS_PRIVILEGE p inner join SYS_FORM_ITEM fi on p.FORM_ID = fi.FORM_ID  " \
                           "inner join SYS_ROLE r on p.ROLE_ID = r.ROLE_ID " \
                           "inner join SYS_FORM f on  p.FORM_ID= f.FORM_ID " \
                           "inner join SYS_PRINT_EXPORT_LOOKUP a on p.ACTION_ID = a.ACTION_ID " \
                           "inner join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  and p.FORM_ID=pi.FORM_ID and pi.ITEM_ID = fi.ITEM_ID  "  \
                           " where  p.ROLE_ID = %s"
        x = (self.role,)

        #print(sql_select_query)
        mycursor.execute(sql_select_query,x)

        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.w1.insertRow(row_number)

            for column_number, data in enumerate(row_data):

                self.w1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        # self.w1.setItem(0, 0, QTableWidgetItem("Name"))
        connection.close()

        self.w1.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header_labels = ['Role Name', 'Role Id', 'Form Name', 'Form Id', 'Action Name','Form Item']
        self.w1.setHorizontalHeaderLabels( header_labels )

    def FN_CREATE_PRIVILAGE(self):
        connection = mysql.connector.connect( host='localhost', database='PosDB'
                                              , user='root', password='password', port='3306' )
        mycursor = connection.cursor()

        self.role = self.LB_roleId.text()
        #delete current role -privilage
        sql_select_query = "SELECT PRIV_ID FROM SYS_PRIVILEGE WHERE ROLE_id = %s"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        records = mycursor.fetchall()
        for row in records:
            sql_select_query = "delete from SYS_PRIVILEG_ITEM where PRIV_ID = '"+row[0]+"'"
            mycursor.execute( sql_select_query)
            sql_select_query1 = "delete from SYS_PRIVILEGE  where PRIV_ID = '" + row[0] + "'"
            mycursor.execute( sql_select_query1 )
            # loop on table widget

        allRows = self.w1.rowCount()
        for row in range( 0, allRows ):
        # # get max userid
            mycursor.execute("SELECT max(PRIV_ID) FROM SYS_PRIVILEGE")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1

            roleId = self.w1.item( row, 1 )

            formId = self.w1.item( row, 3 )
            actionName=self.w1.item( row, 4 )

            sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT_LOOKUP WHERE ACTION_DESC = %s"
            x = (actionName.text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                actionId=myresult[0]

            formItemName= self.w1.item( row, 5)
            sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
            x = (formItemName.text(),)
            mycursor.execute( sql_select_query, x )

            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                formItemId = myresult[0]

            sql = "INSERT INTO SYS_PRIVILEGE (PRIV_ID, ROLE_ID,FORM_ID,ACTION_ID)         " \
                  "VALUES ( %s, %s, %s, %s)"
            val = (self.id,roleId.text() , formId.text(),  actionId)
            mycursor.execute(sql, val)

            sql = "INSERT INTO SYS_PRIVILEG_ITEM (PRIV_ID, FORM_ID,ITEM_ID)         " \
                  "VALUES ( %s, %s, %s)"
            val = (self.id, formId.text(), formItemId)
            mycursor.execute( sql, val )
            print( mycursor.rowcount, "record inserted." )


        connection.commit()
        connection.close()
        mycursor.close()



        self.close()
