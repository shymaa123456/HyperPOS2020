import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
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
class CL_role(QtWidgets.QDialog):
    dirname = ''
    def __init__(self):
        super(CL_role, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        self.conn = db1.connect()
    def FN_ASSIGN(self):
        filename = self.dirname + '/assignUserToRole.ui'
        loadUi( filename, self )

        self.BTN_assignRole.clicked.connect(self.FN_ASSIGN_ROLE)
        self.CMB_userRoleStatus.addItems(["0", "1"])
        self.FN_GET_USERS()
        self.FN_GET_ROLES()
        self.FN_GET_USERID()
        self.FN_GET_ROLEID()
        self.CMB_userName.currentIndexChanged.connect(self.FN_GET_USERID)
        self.CMB_roleName.currentIndexChanged.connect(self.FN_GET_ROLEID)
    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyRole.ui'
        loadUi( filename, self )
        #loadUi('../Presentation/modifyRole.ui', self)
        self.FN_GET_ROLES()
        self.FN_GET_ROLEID()
        self.FN_GET_ROLE()
        self.CMB_roleName.currentIndexChanged.connect( self.FN_GET_ROLE )
        self.BTN_modifyRole.clicked.connect(self.FN_MODIFY_ROLE)
        self.CMB_roleStatus.addItems(["0", "1"])
    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createRole.ui'
        loadUi( filename, self )

        self.BTN_createRole.clicked.connect(self.FN_CREATE_ROLE)
        self.CMB_roleStatus.addItems(["0", "1"])
    def FN_GET_USERID(self):
        self.user = self.CMB_userName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query= "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s"
        x = (self.user,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        self.LB_userID.setText(myresult [0])

    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_NAME = %s"
        x = (self.role,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_roleID.setText(myresult[0])
        mycursor.close()

    def FN_GET_USERS(self):

        mycursor = self.conn.cursor()

        mycursor.execute("SELECT USER_NAME FROM SYS_USER order by USER_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_userName.addItems([row[0]])


        mycursor.close()

    def FN_GET_ROLES(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT ROLE_NAME FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems([row[0]])


        mycursor.close()
    def FN_ASSIGN_ROLE(self):


        self.status = self.CMB_userRoleStatus.currentText()
        self.user = self.LB_userID.text()
        self.role = self.LB_roleID.text()

        mycursor = self.conn.cursor()
        mycursor.execute("SELECT max(UR_USER_ROLE_ID) FROM SYS_USER_ROLE")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))


        sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
              "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"

        val = (self.id, self.user, self.role, '','', creationDate,'', '',  self.status)
        mycursor.execute(sql, val)

        mycursor.close()
        db1.connectionCommit( self.conn )
        print(mycursor.rowcount, "record inserted.")
        db1.connectionClose(self.conn)
        self.close()






    def FN_GET_ROLE(self):
        self.FN_GET_ROLEID()
        self.id = self.LB_roleID.text()

        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_ROLE where ROLE_ID = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        print(record)
        self.LE_name.setText(record[1])
        self.LE_DESC.setText(record[2])

        self.CMB_roleStatus.setCurrentText(record[7])


        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_ROLE(self):
        self.id = self.LB_roleID.text()
        self.name = self.LE_name.text()
        self.desc = self.LE_DESC.text()
        self.status = self.CMB_roleStatus.currentText()

        mycursor = self.conn.cursor()

        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        sql = "UPDATE SYS_ROLE   set ROLE_NAME= %s ,  ROLE_DESC= %s  ,  ROLE_CHANGED_ON = %s , ROLE_CHANGED_BY = %s, ROLE_STATUS = %s where ROLE_id= %s "

        val = (self.name  , self.desc,  changeDate, '', self.status, self.id)
        print(val)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)

        mycursor.close()
        db1.connectionCommit( self.conn )
        print(mycursor.rowcount, "record Modified.")
        db1.connectionClose(self)
        self.close()

    def FN_CREATE_ROLE(self):
        self.name = self.LE_name.text()
        self.desc= self.LE_DESC.text()

        self.status = self.CMB_roleStatus.currentText()

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(role_ID) FROM SYS_ROLE")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))



        sql = "INSERT INTO SYS_ROLE (ROLE_ID, ROLE_NAME,ROLE_DESC,ROLE_CREATED_ON,   ROLE_STATUS)         " \
              "VALUES ('"+ str(self.id )+"','"+ self.name+"','"+self.desc+"', '"+ creationDate +"','" + self.status+"')"

        print(sql)
        #val = ('"+self.id+"','"+ self.name"','"+self.desc "', '"+ creationDate +"',' ', ' ',' ','" + self.status+"')
        mycursor.execute(sql)

        mycursor.close()
        db1.connectionCommit( self.conn )
        print(mycursor.rowcount, "record inserted.")
        db1.connectionClose(self.conn)
        self.close()
