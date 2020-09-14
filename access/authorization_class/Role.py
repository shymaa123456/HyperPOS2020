from PyQt5.uic import loadUi
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from data_connection.h1pos import db1
from datetime import  datetime


class CL_role( QtWidgets.QDialog ):
    dirname = ''

    def __init__(self):
        super( CL_role, self ).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        self.conn = db1.connect()

    def FN_LOAD_COPY(self):
        filename = self.dirname + '/copyRole.ui'
        loadUi( filename, self )

        records = self.FN_GET_ROLES_N()
        for row in records :
            self.CMB_roleName.addItems( [row[0]] )
            self.CMB_roleName1.addItems( [row[0]] )

        self.BTN_copyRole.clicked.connect( self.FN_COPY_ROLE )
        self.CMB_roleName.currentIndexChanged.connect( self.FN_ASSIGN_ID )
        self.CMB_roleName1.currentIndexChanged.connect( self.FN_ASSIGN_ID )
        self.FN_ASSIGN_ID()

    def FN_ASSIGN_ID(self):
        self.role1 = self.CMB_roleName.currentText()
        self.role2 = self.CMB_roleName1.currentText()
        self.LB_roleID.setText( self.FN_GET_ROLEID_N(self.role1) )
        self.LB_roleID2.setText( self.FN_GET_ROLEID_N(self.role2 ) )

    def FN_COPY_ROLE(self):
        newRole = self.LB_roleID2.text()

        if self.role1 == self.role2:
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter 2 different users" )
        else:
            mycursor = self.conn.cursor()
            mycursor1 = self.conn.cursor()
            mycursor2 = self.conn.cursor()

            sql_select_query = "select ur.FORM_ID ,ur.ACTION_ID  " \
                               "from SYS_PRIVILEGE ur  inner join SYS_ROLE u ON u.ROLE_ID = ur.ROLE_ID  " \
                               "where  u.ROLE_NAME = %s "
            x = (self.role1,)
            mycursor.execute( sql_select_query, x )
            records = mycursor.fetchall()
            # delete current assignment if found
            mycursor2 = self.conn.cursor()
            sql_select_query1 = "delete from SYS_PRIVILEGE  where ROLE_ID = '" + newRole + "'"
            mycursor2.execute( sql_select_query1 )
            db1.connectionCommit( self.conn )

            mycursor1.execute( "SELECT max(cast(PRIV_ID  AS UNSIGNED)) FROM SYS_PRIVILEGE" )
            myresult = mycursor1.fetchone()

            id = int( myresult[0] ) + 1
            for row in records:
                mycursor3 = self.conn.cursor()
                # sql = " INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS) VALUES ( "+id+", "+newUser+", "+row[0]+", '"+row[1]+"','"+CL_userModule.user_name+"', '"+creationDate+"',' ',' ' ,'"+row[2]+"')"
                sql = "INSERT INTO SYS_PRIVILEGE VALUES ( %s, %s, %s, %s)"

                val = (id, newRole, row[0], row[1])
                print( str( sql ) )
                # val = (id,newUser,  row[0], row[1], CL_userModule.user_name, creationDate, '', '', row[2],)
                mycursor3.execute( sql, val )

                db1.connectionCommit( self.conn )
                print( mycursor3.rowcount, "record inserted." )
                id = id + 1

            mycursor2.close()
            mycursor1.close()
            mycursor.close()
            self.close()

    def FN_GET_ROLES_N(self):

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT ROLE_NAME ROLE_ID FROM SYS_ROLE order by ROLE_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_GET_ROLEID_N(self, role):

        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_NAME = %s "
        x = (role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        return myresult[0]




    def FN_ASSIGN(self):
        filename = self.dirname + '/assignUserToRole.ui'
        loadUi( filename, self )

        self.BTN_assignRole.clicked.connect( self.FN_ASSIGN_ROLE )
        self.CMB_userRoleStatus.addItems( ["0", "1"] )
        self.FN_GET_USERS()
        self.FN_GET_ROLES()
        self.FN_GET_USERID()
        self.FN_GET_ROLEID()
        self.CMB_userName.currentIndexChanged.connect( self.FN_GET_USERID )
        self.CMB_roleName.currentIndexChanged.connect( self.FN_GET_ROLEID )

    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyRole.ui'
        loadUi( filename, self )
        # loadUi('../Presentation/modifyRole.ui', self)
        self.FN_GET_ROLES()
        self.FN_GET_ROLEID()
        self.FN_GET_ROLE()
        self.CMB_roleName.currentIndexChanged.connect( self.FN_GET_ROLE )
        self.BTN_modifyRole.clicked.connect( self.FN_MODIFY_ROLE )
        self.CMB_roleStatus.addItems( ["0", "1"] )

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createRole.ui'
        loadUi( filename, self )

        self.BTN_createRole.clicked.connect( self.FN_CREATE_ROLE )
        self.CMB_roleStatus.addItems( ["0", "1"] )

    def FN_GET_USERID(self):
        self.user = self.CMB_userName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s"
        x = (self.user,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        self.LB_userID.setText( myresult[0] )

    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_NAME = %s"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )

        myresult = mycursor.fetchone()
        self.LB_roleID.setText( myresult[0] )
        mycursor.close()

    def FN_GET_USERS(self):

        mycursor = self.conn.cursor()

        mycursor.execute( "SELECT USER_NAME FROM SYS_USER where USER_STATUS = 0 order by USER_ID asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_userName.addItems( [row[0]] )

        mycursor.close()

    def FN_GET_ROLES(self):
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT ROLE_NAME FROM SYS_ROLE order by ROLE_ID asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems( [row[0]] )

        mycursor.close()

    def FN_ASSIGN_ROLE(self):

        self.status = self.CMB_userRoleStatus.currentText()
        self.user = self.LB_userID.text()
        self.role = self.LB_roleID.text()

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT max(cast(UR_USER_ROLE_ID  AS UNSIGNED)) FROM SYS_USER_ROLE" )
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int( myresult[0] ) + 1

        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

        sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
              "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"

        val = (self.id, self.user, self.role, '1', '', creationDate, '', '', self.status)
        mycursor.execute( sql, val )

        mycursor.close()
        db1.connectionCommit( self.conn )
        print( mycursor.rowcount, "record inserted." )
        db1.connectionClose( self.conn )
        self.close()

    def FN_GET_ROLE(self):
        self.FN_GET_ROLEID()
        self.id = self.LB_roleID.text()

        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_ROLE where ROLE_ID = %s "
        x = (self.id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()
        print( record )
        self.LE_name.setText( record[1] )
        self.LE_DESC.setText( record[2] )

        self.CMB_roleStatus.setCurrentText( record[7] )

        mycursor.close()

        print( mycursor.rowcount, "record retrieved." )

    def FN_MODIFY_ROLE(self):
        self.id = self.LB_roleID.text()
        self.name = self.LE_name.text().strip()
        self.desc = self.LE_DESC.text().strip()
        self.status = self.CMB_roleStatus.currentText()

        if self.name == '' or self.desc == '':
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )
        else:
            mycursor = self.conn.cursor()

            changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

            sql = "UPDATE SYS_ROLE   set ROLE_NAME= %s ,  ROLE_DESC= %s  ,  ROLE_CHANGED_ON = %s , ROLE_CHANGED_BY = %s, ROLE_STATUS = %s where ROLE_id= %s "

            val = (self.name, self.desc, changeDate, '', self.status, self.id)
            print( val )
            mycursor.execute( sql, val )
            # mycursor.execute(sql)

            mycursor.close()
            db1.connectionCommit( self.conn )
            print( mycursor.rowcount, "record Modified." )
            db1.connectionClose( self )
            self.close()

    def FN_CREATE_ROLE(self):
        self.name = self.LE_name.text().strip()
        self.desc = self.LE_DESC.text().strip()

        self.status = self.CMB_roleStatus.currentText()
        if self.name == '' or self.desc =='' :
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )
        else:
            mycursor = self.conn.cursor()
            # get max userid
            mycursor.execute( "SELECT max(cast(role_ID  AS UNSIGNED)) FROM SYS_ROLE" )
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int( myresult[0] ) + 1

            creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )


            sql = "INSERT INTO SYS_ROLE (ROLE_ID, ROLE_NAME,ROLE_DESC,ROLE_CREATED_ON,   ROLE_STATUS)         " \
                  "VALUES ('" + str(
                self.id ) + "','" + self.name + "','" + self.desc + "', '" + creationDate + "','" + self.status + "')"

            print( sql )
            # val = ('"+self.id+"','"+ self.name"','"+self.desc "', '"+ creationDate +"',' ', ' ',' ','" + self.status+"')
            mycursor.execute( sql )

            mycursor.close()
            db1.connectionCommit( self.conn )
            print( mycursor.rowcount, "record inserted." )
            db1.connectionClose( self.conn )
            self.close()
