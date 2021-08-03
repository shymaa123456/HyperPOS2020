from PyQt5.uic import loadUi
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
from PyQt5.uic import loadUi

from access.authorization_class.user_module import CL_userModule
from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from datetime import datetime


class CL_role(QtWidgets.QDialog):
    dirname = ''

    def __init__(self):
        super(CL_role, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        css_path = Path(__file__).parent.parent.parent

        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        self.conn = db1.connect()

    #Todo: method to load ui of copy role
    def FN_LOAD_COPY(self):
        filename = self.dirname + '/copyRole.ui'
        loadUi(filename, self)
        records = self.FN_GET_ROLES_N()
        for row in records:
            self.CMB_roleName.addItems([row[0]])
            self.CMB_roleName1.addItems([row[0]])
        self.BTN_copyRole.clicked.connect(self.FN_COPY_ROLE)
        self.CMB_roleName.currentIndexChanged.connect(self.FN_ASSIGN_ID)
        self.CMB_roleName1.currentIndexChanged.connect(self.FN_ASSIGN_ID)
        self.FN_ASSIGN_ID()

    #Todo: method to set text by id
    def FN_ASSIGN_ID(self):
        self.role1 = self.CMB_roleName.currentText()
        self.role2 = self.CMB_roleName1.currentText()
        self.LB_roleID.setText(self.FN_GET_ROLEID_N(self.role1))
        self.LB_roleID2.setText(self.FN_GET_ROLEID_N(self.role2))

    #Todo: method to copy role action
    def FN_COPY_ROLE(self):
        newRole = self.LB_roleID2.text()
        if self.role1 == self.role2:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter 2 different users")
        else:
            mycursor = self.conn.cursor()
            mycursor1 = self.conn.cursor()
            mycursor2 = self.conn.cursor()
            sql_select_query = "select ur.FORM_ID ,ur.ACTION_ID  " \
                               "from SYS_PRIVILEGE ur  inner join SYS_ROLE u ON u.ROLE_ID = ur.ROLE_ID  " \
                               "where  u.ROLE_NAME = %s "
            x = (self.role1,)
            mycursor.execute(sql_select_query, x)
            records = mycursor.fetchall()
            mycursor2 = self.conn.cursor()
            sql_select_query1 = "delete from SYS_PRIVILEGE  where ROLE_ID = '" + newRole + "'"
            mycursor2.execute(sql_select_query1)
            db1.connectionCommit(self.conn)
            mycursor1.execute("SELECT max(cast(PRIV_ID  AS UNSIGNED)) FROM SYS_PRIVILEGE")
            myresult = mycursor1.fetchone()
            id = int(myresult[0]) + 1
            for row in records:
                mycursor3 = self.conn.cursor()
                sql = "INSERT INTO SYS_PRIVILEGE VALUES ( %s, %s, %s, %s)"
                val = (id, newRole, row[0], row[1])
                mycursor3.execute(sql, val)
                db1.connectionCommit(self.conn)
                print(mycursor3.rowcount, "record inserted.")
                id = id + 1
            mycursor2.close()
            mycursor1.close()
            mycursor.close()
            self.close()

    #Todo: method to get all role name and id
    def FN_GET_ROLES_N(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT ROLE_NAME ROLE_ID FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        mycursor.close()
        return records

    #Todo: method to get role id
    def FN_GET_ROLEID_N(self, role):
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_NAME = %s "
        x = (role,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        return myresult[0]

    #Todo: method to load ui of assignUserToRole
    def FN_ASSIGN(self):
        self.CMB_roleName = CheckableComboBox(self)
        self.CMB_roleName.setGeometry(100, 85, 179, 18)
        self.CMB_roleName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CMB_roleName.setStyleSheet("background-color: rgb(198, 207, 199)")
        filename = self.dirname + '/assignUserToRole.ui'
        loadUi(filename, self)
        self.BTN_assignRole.clicked.connect(self.FN_ASSIGN_ROLE)
        self.CMB_userRoleStatus.addItems(["Active", "Inactive"])
        self.FN_GET_USERS()
        self.FN_GET_USERID()
        self.FN_GET_ROLES()
        self.CMB_userName.currentIndexChanged.connect(self.FN_GET_USERID)

    #Todo: method to load ui of modify role
    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyRole.ui'
        loadUi(filename, self)
        self.CMB_roleStatus.addItems(["Active", "Inactive"])
        self.FN_GET_ROLES1()
        self.FN_GET_ROLEID()
        self.FN_GET_ROLE()
        self.CMB_roleName.currentIndexChanged.connect(self.FN_GET_ROLE)
        self.BTN_modifyRole.clicked.connect(self.FN_MODIFY_ROLE)

    #Todo: method to load ui of create role
    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createRole.ui'
        loadUi(filename, self)
        self.BTN_createRole.clicked.connect(self.FN_CREATE_ROLE)
        self.CMB_roleStatus.addItems(["Active", "Inactive"])

    #Todo: method to get user id
    def FN_GET_USERID(self):
        self.user = self.CMB_userName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s"
        x = (self.user,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        self.LB_userID.setText(myresult[0])
        self.FN_GET_ROLES()

    #Todo: method to get role id
    def FN_GET_ROLEID1(self, roleNm):
        if roleNm is not None:
            self.role = roleNm
        else:
            self.role = self.CMB_roleName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_NAME = %s"
        x = (self.role,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        self.LB_roleID.setText(myresult[0])
        mycursor.close()
        return myresult[0]

    #Todo: method to get role id
    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_NAME = %s"
        x = (self.role,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        self.LB_roleID.setText(myresult[0])
        mycursor.close()
        return myresult[0]

    #Todo: method to get all users name
    def FN_GET_USERS(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT USER_NAME FROM SYS_USER where USER_STATUS = 1 order by USER_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_userName.addItems([row[0]])
        mycursor.close()

    #Todo: method to get role assigned to user and checked it
    def FN_GET_ROLES(self):
        self.CMB_roleName.clear()
        if self.LB_userID is not None:
            selectedRoles = self.FN_SELECT_USER_ROLES()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT ROLE_NAME FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        j = 0
        for row in records:
            self.CMB_roleName.addItems(row)
            for row1 in selectedRoles:
                if row[0] == row1[0]:
                    items = self.CMB_roleName.findText(row[0])
                    for item in range(items+1):
                        self.CMB_roleName.setChecked(j)
            j = j + 1
        mycursor.close()

    #Todo: method to get all role name
    def FN_GET_ROLES1(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT ROLE_NAME FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems(row)
        mycursor.close()

    #Todo: method to get all role assigned to user
    def FN_SELECT_USER_ROLES(self):
        self.user = self.LB_userID.text()
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT ROLE_NAME FROM SYS_USER_ROLE INNER JOIN SYS_ROLE   on SYS_ROLE.ROLE_ID= SYS_USER_ROLE.ROLE_ID where SYS_USER_ROLE.USER_ID= %s "
        x = (self.user,)
        mycursor.execute(sql_select_query, x)
        records = mycursor.fetchall()
        return records

    #Todo: method to assign role to user
    def FN_ASSIGN_ROLE(self):
        self.status = self.CMB_userRoleStatus.currentText()
        self.user = self.LB_userID.text()
        self.role = self.LB_roleID.text()
        self.status = self.CMB_userRoleStatus.currentText()
        if self.status == 'Active':
            self.status = 1
        else:
            self.status = 0
        mycursor = self.conn.cursor(buffered=True)
        sql_select_query = "delete from SYS_USER_ROLE where SYS_USER_ROLE.USER_ID=  '" + self.user + "'"
        mycursor.execute(sql_select_query)
        db1.connectionCommit(self.conn)
        items = self.CMB_roleName.currentData()
        x = []
        for i in range(len(items)):
            roleId = self.FN_GET_ROLEID1(str(items[i]))
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT max(cast(UR_USER_ROLE_ID  AS UNSIGNED)) FROM SYS_USER_ROLE")
            myresult = mycursor.fetchone()
            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1
            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
            sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
                  "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"
            val = (self.id, self.user, roleId, '1', CL_userModule.user_name, creationDate, '', '', self.status)
            mycursor.execute(sql, val)
            mycursor.close()
            db1.connectionCommit(self.conn)
            print(mycursor.rowcount, "record inserted.")
        db1.connectionClose(self.conn)
        self.close()
        QtWidgets.QMessageBox.information(self, "Success", "Role is assigned successfully")

    def FN_GET_ROLE(self):
        self.FN_GET_ROLEID()
        self.name = self.CMB_roleName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_ROLE where ROLE_NAME = %s "
        x = (self.name,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        self.LE_name.setText(record[1])
        self.LE_DESC.setText(record[2])
        if record[7] == '1':
            self.CMB_roleStatus.setCurrentText('Active')
        else:
            self.CMB_roleStatus.setCurrentText('Inactive')
        mycursor.close()
        print(mycursor.rowcount, "record retrieved.")

    #Todo: method to modify role
    def FN_MODIFY_ROLE(self):
        self.old_name = self.CMB_roleName.currentText()
        self.name = self.LE_name.text().strip()
        self.desc = self.LE_DESC.text().strip()
        self.status = self.CMB_roleStatus.currentText()
        if self.status == 'Active':
            self.status = '1'
        else:
            self.status = '0'
        if self.name == '' or self.desc == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please all required field")
        else:
            mycursor = self.conn.cursor()
            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
            sql = "UPDATE SYS_ROLE   set ROLE_NAME= %s ,  ROLE_DESC= %s  ,  ROLE_CHANGED_ON = %s , ROLE_CHANGED_BY = %s, ROLE_STATUS = %s where ROLE_NAME= %s "
            val = (self.name, self.desc, changeDate, CL_userModule.user_name, self.status, self.old_name)
            mycursor.execute(sql, val)
            mycursor.close()
            db1.connectionCommit(self.conn)
            print(mycursor.rowcount, "record Modified.")
            db1.connectionClose(self)
            self.close()
            QtWidgets.QMessageBox.information(self, "Success", "Role is modified successfully")

    #Todo: method to get create role
    def FN_CREATE_ROLE(self):
        self.name = self.LE_name.text().strip()
        self.desc = self.LE_DESC.text().strip()
        self.status = self.CMB_roleStatus.currentText()
        if self.status == 'Active':
            self.status = '1'
        else:
            self.status = '0'
        if self.name == '' or self.desc == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please all required field")
        else:
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT max(cast(role_ID  AS UNSIGNED)) FROM SYS_ROLE")
            myresult = mycursor.fetchone()
            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int(myresult[0]) + 1
            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
            sql = "INSERT INTO SYS_ROLE (ROLE_ID, ROLE_NAME,ROLE_DESC,ROLE_CREATED_BY,ROLE_CREATED_ON,   ROLE_STATUS)         " \
                  "VALUES ('" + str(
                self.id) + "','" + self.name + "','" + self.desc + "',  '" + CL_userModule.user_name + "',  '" + creationDate + "','" + self.status + "')"
            print(sql)
            mycursor.execute(sql)
            mycursor.close()
            db1.connectionCommit(self.conn)
            print(mycursor.rowcount, "record inserted.")
            db1.connectionClose(self.conn)
            self.close()
            QtWidgets.QMessageBox.information(self, "Success", "Role is created successfully")
