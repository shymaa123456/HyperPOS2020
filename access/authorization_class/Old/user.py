import sys
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore

from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from access.Checkable import CheckableComboBox, Qt
from data_connection.h1pos import db1

from datetime import datetime


class CL_user(QtWidgets.QDialog):
    dirname = ''
    userid=''
    branch_list = []
    new_branch_list = []
    section_list = []
    new_section_list = []


    def __init__(self):
        super(CL_user, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/authorization_ui'
        self.conn = db1.connect()

    #Todo: method for load ui of modify user
    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifyUser.ui'
        loadUi(filename, self)
        self.CMB_branch = CheckableComboBox(self)
        self.CMB_branch.setGeometry(150, 120, 171, 25)
        self.CMB_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CMB_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.CMB_section = CheckableComboBox(self)
        self.CMB_section.setGeometry(150, 170, 171, 25)
        self.CMB_section.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CMB_section.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_BRANCHES()
        self.FN_GET_Section()
        self.FN_GET_USERTYPE()
        self.CMB_userStatus.addItems(["Active", "Inactive"])
        records = self.FN_GET_USERS()
        for row in records:
            self.CMB_userName.addItems([row[0]])
        self.FN_GET_USER()
        self.CMB_userName.currentIndexChanged.connect(self.FN_GET_USER)
        self.BTN_modifyUser.clicked.connect(self.FN_MODIFY_USER)

    #Todo: method for load ui of create User
    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createUser.ui'
        loadUi(filename, self)
        self.setWindowTitle('Users')
        self.BTN_createUser.clicked.connect(self.FN_CREATE_USER)
        self.CMB_branch = CheckableComboBox(self)
        self.CMB_branch.setGeometry(150, 85, 171, 25)
        self.CMB_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CMB_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.CMB_section = CheckableComboBox(self)
        self.CMB_section.setGeometry(150, 130, 171, 25)
        self.CMB_section.setEnabled(False)
        self.CMB_section.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CMB_section.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.FN_GET_BRANCHES()
        self.FN_GET_Section()
        self.FN_GET_USERTYPE()
        self.checkBox.toggled.connect(self.FN_EnableDepartment)
        self.CMB_userStatus.addItems(["Active", "Inactive"])

        # Set Style
        # self.voucher_num.setStyleSheet(label_num)
        # self.label_2.setStyleSheet(desc_5)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())

    #Todo: method for get user type
    def FN_GET_USERTYPE(self):
        mycursor = self.conn.cursor()
        self.CMB_userType.clear()
        sql_select_query = "SELECT USER_TYPE_DESC  FROM SYS_USER_TYPE where USER_TYPE_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_userType.addItems([row[0]])
        mycursor.close()

    #Todo: method for get all branches
    def FN_GET_BRANCHES(self):
        mycursor = self.conn.cursor()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A ,BRANCH_NO  FROM BRANCH where BRANCH_STATUS = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_branch.addItem(row,val)
        mycursor.close()

    #Todo: method for get all sections
    def FN_GET_Section(self):
        mycursor = self.conn.cursor()
        self.CMB_section.clear()
        sql_select_query = "SELECT SECTION_DESC ,SECTION_ID FROM SECTION "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row,val in records:
            self.CMB_section.addItem(row,val)
        mycursor.close()

    #Todo: method for load copy ui
    def FN_LOAD_COPY(self):
        filename = self.dirname + '/copyUser.ui'
        loadUi(filename, self)
        records = self.FN_GET_USERS()
        for row in records:
            self.CMB_userName.addItems([row[0]])
            self.CMB_userName1.addItems([row[0]])
        self.BTN_copyUser.clicked.connect(self.FN_COPY_USER)
        self.CMB_userName.currentIndexChanged.connect(self.FN_ASSIGN_ID)
        self.CMB_userName1.currentIndexChanged.connect(self.FN_ASSIGN_ID)
        self.FN_ASSIGN_ID()

    #Todo: method for get data from user combobox
    def FN_ASSIGN_ID(self):
        self.user1 = self.CMB_userName.currentText()
        self.user2 = self.CMB_userName1.currentText()
        self.LB_userID.setText(self.FN_GET_USERID_N(self.user1))
        self.LB_userID2.setText(self.FN_GET_USERID_N(self.user2))

    #Todo: method to copy user
    def FN_COPY_USER(self):
        newUser = self.LB_userID2.text()
        if self.user1 == self.user2:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter 2 different users")
        else:
            mycursor = self.conn.cursor()
            mycursor1 = self.conn.cursor()
            mycursor2 = self.conn.cursor()
            sql_select_query = "select ur.ROLE_ID ,ur.BRANCH_NO ,ur.UR_STATUS  " \
                               "from SYS_USER_ROLE  ur  inner join SYS_USER u ON u.USER_ID = ur.USER_ID  " \
                               "where  u.USER_NAME = %s "
            x = (self.user1,)
            mycursor.execute(sql_select_query, x)
            records = mycursor.fetchall()
            mycursor2 = self.conn.cursor()
            sql_select_query1 = "delete from SYS_USER_ROLE where USER_ID = '" + newUser + "'"
            mycursor2.execute(sql_select_query1)
            db1.connectionCommit(self.conn)
            mycursor1.execute("SELECT max(cast(UR_USER_ROLE_ID  AS UNSIGNED)) FROM SYS_USER_ROLE")
            myresult = mycursor1.fetchone()
            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
            id = int(myresult[0]) + 1
            for row in records:
                mycursor3 = self.conn.cursor()
                sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
                      "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"
                val = (id, newUser, row[0], row[1], CL_userModule.user_name, creationDate, '', '', row[2])
                print(str(sql))
                mycursor3.execute(sql, val)
                db1.connectionCommit(self.conn)
                print(mycursor3.rowcount, "record inserted.")
                id = id + 1
            QtWidgets.QMessageBox.information(self, "Success", "User is copied successfully")
            mycursor2.close()
            mycursor1.close()
            mycursor.close()
            self.close()

    #Todo: method for get all users and display all data
    def FN_GET_USER(self):
        user = self.CMB_userName.currentText()
        mycursor = self.conn.cursor()
        sql_select_query = "select * from SYS_USER where USER_NAME = '"+user+"'"
        print(sql_select_query)
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)
        self.LB_userID.setText(record[0])
        self.userid=record[0]
        self.LE_name.setText(record[2])
        self.LE_password.setText(record[3])
        self.LE_fullName.setText(record[4])
        self.LE_hrId.setText(record[5])
        self.CMB_userType.setCurrentText(record[11])
        if record[10] == '1':
            self.CMB_userStatus.setCurrentText('Active')
        else:
            self.CMB_userStatus.setCurrentText('Inactive')
        print(mycursor.rowcount, "record retrieved.")
        mycursor.close()
        self.FN_check_branch()
        self.FN_check_section()
        self.branch_list.clear()
        if len(self.CMB_branch.currentData()) > 0:
            for i in self.CMB_branch.currentData():
                self.branch_list.append(i)
        if len(self.CMB_section.currentData()) > 0:
            for i in self.CMB_section.currentData():
                self.section_list.append(i)

    #Todo: method for edit user
    def FN_MODIFY_USER(self):
        try:
            self.id = self.LB_userID.text()
            self.name = self.LE_name.text().strip()
            self.password = self.LE_password.text().strip()
            self.branch = self.CMB_branch.currentData()[0]
            self.fullName = self.LE_fullName.text().strip()
            self.hrId = self.LE_hrId.text().strip()
            self.userType = self.CMB_userType.currentText()
            self.status = self.CMB_userStatus.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0
            if CL_validation.FN_isEmpty(self.name) or CL_validation.FN_isEmpty(
                    self.password) or CL_validation.FN_isEmpty(self.fullName) or CL_validation.FN_isEmpty(
                self.hrId):
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")
            else:
                if CL_validation.FN_validation_password(self, self.password) == False:
                    mycursor = self.conn.cursor()
                    if len(self.CMB_branch.currentData()) > 0:
                        for i in self.CMB_branch.currentData():
                            self.new_branch_list.append(i)
                    if len(self.CMB_section.currentData()) > 0:
                        for i in self.CMB_section.currentData():
                            self.new_section_list.append(i)
                    changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "UPDATE SYS_USER   set USER_NAME= %s ,  USER_PASSWORD= %s  ,  BRANCH_NO = %s, USER_FULLNAME = %s , USER_HR_ID = %s, USER_CHANGED_ON = %s , USER_CHANGED_BY = %s, USER_STATUS = %s, USERTYPE_ID = %s where USER_id= %s "
                    val = (
                        self.name, self.password, self.branch, self.fullName, self.hrId, changeDate,
                        CL_userModule.user_name,
                        self.status, self.userType, self.id)
                    mycursor.execute(sql, val)
                    if len(self.branch_list) > len(self.new_branch_list):
                        for row in self.branch_list:
                            print(row)
                            if row in self.new_branch_list:
                                print("found")
                            else:
                                print("not found")
                                mycursor = self.conn.cursor()
                                sql5 = "update SYS_USER_BRANCH set STATUS= 0 where USER_ID='" + self.userid + "' and BRANCH_NO = '" + row + "'"
                                mycursor.execute(sql5)
                    else:
                        for row in self.new_branch_list:
                            print(row)
                            if row in self.branch_list:
                                print("found")
                            else:
                                mycursor = self.conn.cursor()
                                mycursor.execute(
                                    "SELECT * FROM SYS_USER_BRANCH where BRANCH_NO='" + row + "' and USER_ID='" + self.userid + "'")
                                record = mycursor.fetchall()
                                if mycursor.rowcount > 0:
                                    mycursor = self.conn.cursor()
                                    sql8 = "update SYS_USER_BRANCH set STATUS= 1 where USER_ID='" + self.userid + "' and BRANCH_NO = '" + row + "'"
                                    mycursor.execute(sql8)
                                    print(sql8)
                                else:
                                    mycursor = self.conn.cursor()
                                    sql6 = "INSERT INTO SYS_USER_BRANCH (USER_ID,COMPANY_ID,BRANCH_NO,STATUS) VALUES (%s,%s,%s,%s)"
                                    val6 = (self.userid, '1', row, '1')
                                    mycursor.execute(sql6, val6)
                    if len(self.section_list) > len(self.new_section_list):
                        for row in self.section_list:
                            print(row)
                            if row in self.new_section_list:
                                print("found")
                            else:
                                print("not found")
                                mycursor = self.conn.cursor()
                                sql5 = "update SYS_USER_SECTION set STATUS= 0 where USER_ID='" + self.userid + "' and SECTION_ID = '" + row + "'"
                                mycursor.execute(sql5)
                    else:
                        for row in self.new_section_list:
                            print(row)
                            if row in self.section_list:
                                print("found")
                            else:
                                mycursor = self.conn.cursor()
                                mycursor.execute(
                                    "SELECT * FROM SYS_USER_SECTION where SECTION_ID='" + row + "' and USER_ID='" + self.userid + "'")
                                record = mycursor.fetchall()
                                if mycursor.rowcount > 0:
                                    mycursor = self.conn.cursor()
                                    sql8 = "update SYS_USER_SECTION set STATUS= 1 where USER_ID='" + self.userid + "' and SECTION_ID = '" + row + "'"
                                    mycursor.execute(sql8)
                                    print(sql8)
                                else:
                                    mycursor = self.conn.cursor()
                                    sql6 = "INSERT INTO SYS_USER_SECTION (USER_ID,SECTION_ID,STATUS) VALUES (%s,%s,%s)"
                                    val6 = (self.userid, row, '1')
                                    mycursor.execute(sql6, val6)
                    mycursor.close()
                    db1.connectionCommit(self.conn)
                    print(mycursor.rowcount, "record Modified.")
                    QtWidgets.QMessageBox.information(self, "Success", "User is modified successfully")
                    db1.connectionClose(self.conn)
                    self.close()
        except:
            print(sys.exc_info())

    #Todo: method for get user data
    def FN_GET_USERS(self):
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT USER_NAME USER_ID FROM SYS_USER order by USER_ID asc")
        records = mycursor.fetchall()
        mycursor.close()
        return records

    #Todo: method for get user id
    def FN_GET_USERID_N(self, user):
        mycursor = self.conn.cursor()
        sql_select_query = "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s "
        x = (user,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        return myresult[0]

    #Todo: method for create user
    def FN_CREATE_USER(self):
        try:
            sql_select_Query = "select * from SYS_USER where USER_NAME = '" + self.LE_name.text() + "' and USER_STATUS = 1"
            print(sql_select_Query)
            mycursor = self.conn.cursor()
            mycursor.execute(sql_select_Query)
            print(mycursor.fetchall())
            if mycursor.rowcount > 0:
                QtWidgets.QMessageBox.warning(self, "Error", "Username is already exists")
            else:
                self.name = self.LE_name.text().strip()
                self.password = self.LE_password.text().strip()
                print(self.CMB_branch.currentData()[0])
                self.branch = self.CMB_branch.currentData()[0]
                self.fullName = self.LE_fullName.text().strip()
                self.hrId = self.LE_hrId.text().strip()
                self.userType = self.CMB_userType.currentText()
                self.status = self.CMB_userStatus.currentText()
                if self.status == 'Active':
                    self.status = 1
                else:
                    self.status = 0
                mycursor = self.conn.cursor()
                mycursor.execute("SELECT max(cast(USER_ID  AS UNSIGNED)) FROM SYS_USER")
                myresult = mycursor.fetchone()
                if myresult[0] == None:
                    self.id = "1"
                else:
                    self.id = int(myresult[0]) + 1
                creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                if CL_validation.FN_isEmpty(self.name) or CL_validation.FN_isEmpty(
                        self.password) or CL_validation.FN_isEmpty(
                    self.fullName) or CL_validation.FN_isEmpty(self.hrId):
                    QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")
                else:
                    if CL_validation.FN_validation_password(self, self.password) == False:
                        sql = "INSERT INTO SYS_USER (USER_ID, BRANCH_NO, USER_NAME, USER_PASSWORD, USER_FULLNAME, USER_HR_ID, USER_CREATED_ON, USER_CREATED_BY, USER_CHANGED_ON, USER_CHANGED_BY,USER_STATUS, USERTYPE_ID)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (
                            self.id, self.branch, self.name, self.password, self.fullName, self.hrId, creationDate,
                            CL_userModule.user_name, '', '', self.status,
                            self.userType)
                        mycursor.execute(sql, val)
                        for i in range(len(self.CMB_branch.currentData())):
                            sql2 = "INSERT INTO SYS_USER_BRANCH (USER_ID, COMPANY_ID, BRANCH_NO, STATUS) VALUES ( %s, %s, %s, %s)"
                            val = (
                                self.id, '1', self.CMB_branch.currentData()[i], '1')
                            mycursor.execute(sql2, val)

                        if self.checkBox.isChecked():
                            for i in range(len(self.CMB_section.currentData())):
                                sql = "INSERT INTO SYS_USER_SECTION (USER_ID, SECTION_ID, STATUS) VALUES (%s, %s, %s)"
                                val = (self.id, self.CMB_section.currentData()[i], '1')
                                mycursor.execute(sql, val)
                        mycursor.close()
                        print(mycursor.rowcount, "record inserted.")
                        QtWidgets.QMessageBox.information(self, "Success", "User is created successfully")
                        db1.connectionCommit(self.conn)
                        db1.connectionClose(self.conn)
                        self.close()
        except:
            print(sys.exc_info())

    #Todo: method for change password
    def FN_RESET_USER(self):
        mycursor = self.conn.cursor()
        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
        if CL_validation.FN_isEmpty(self.LE_password.text()) :
            QtWidgets.QMessageBox.warning(self, "Error", "Enter Password Please")
        elif CL_validation.FN_isEmpty(self.LE_password2.text()):
            QtWidgets.QMessageBox.warning(self, "Error", " RePassword Please")
        elif CL_validation.FN_validation_password(self,self.LE_password.text())==False:
            if self.LE_password.text() == self.LE_password2.text():
                sql_select_Query = "select * from SYS_USER where USER_NAME = %s and USER_PASSWORD = %s and USER_STATUS  = 1"
                x = (self.LE_username.text(), self.old_password.text())
                mycursor = self.conn.cursor()
                mycursor.execute(sql_select_Query, x)
                record = mycursor.fetchone()
                if mycursor.rowcount > 0:
                    sql = "UPDATE SYS_USER set USER_PASSWORD= %s  , USER_CHANGED_ON = %s , USER_CHANGED_BY = %s where USER_NAME= %s and USER_PASSWORD= %s "
                    val = (self.LE_password.text(), changeDate, self.LE_username.text(), self.LE_username.text(),
                           self.old_password.text())
                    print(sql)
                    mycursor.execute(sql, val)
                    mycursor.close()
                    db1.connectionCommit(self.conn)
                    print(mycursor.rowcount, "password changed")
                    QtWidgets.QMessageBox.information(self, "Success", "Password is reset successfully")
                    db1.connectionClose(self.conn)
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Incorrect Username and Password")
                    print("Please Enter Correct Username and Password")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter 2 different Passwords")

    #Todo: method for load reset password ui
    def FN_LOAD_RESET(self):
        filename = self.dirname + '/resetUserPassword.ui'
        loadUi(filename, self)
        self.BTN_resetPass.clicked.connect(self.FN_RESET_USER)

    #Todo: method for change password
    def FN_RESET_USER_MAIN(self):
        mycursor = self.conn.cursor()
        if CL_validation.FN_isEmpty(self.LE_password.text()):
            QtWidgets.QMessageBox.warning(self, "Error", "Enter Password Please")
        elif CL_validation.FN_isEmpty(self.LE_password2.text()):
            QtWidgets.QMessageBox.warning(self, "Error", " RePassword Please")
        elif CL_validation.FN_validation_password(self,self.LE_password.text())==False:
            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
            if self.LE_password.text() == self.LE_password2.text():
                sql_select_Query = "select * from SYS_USER where USER_NAME = '" + self.LE_username.currentText() + "' and USER_STATUS = 1"
                mycursor = self.conn.cursor()
                mycursor.execute(sql_select_Query)
                print(sql_select_Query)
                record = mycursor.fetchone()
                print(record)
                if mycursor.rowcount > 0:
                    sql = "UPDATE SYS_USER set USER_PASSWORD= %s  , USER_CHANGED_ON = %s , USER_CHANGED_BY = %s where USER_NAME= %s"
                    val = (self.LE_password.text(), changeDate, self.LE_username.currentText(), self.LE_username.currentText())
                    print(sql)
                    mycursor.execute(sql, val)
                    mycursor.close()
                    db1.connectionCommit(self.conn)
                    print(mycursor.rowcount, "password changed")
                    QtWidgets.QMessageBox.information(self, "Success", "Password is reset successfully")
                    db1.connectionClose(self.conn)
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Incorrect Username ")
                    print("Please Enter Correct Username and Password")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter 2 different Passwords")

    #Todo: method for load reset password ui
    def FN_LOAD_RESET_MAIN(self):
        filename = self.dirname + '/resetUserPasswordMain.ui'
        loadUi(filename, self)
        self.FN_GET_User()
        self.BTN_resetPass.clicked.connect(self.FN_RESET_USER_MAIN)

    #Todo: method for all user name
    def FN_GET_User(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT USER_NAME FROM SYS_USER")
        records = mycursor.fetchall()
        for row in records:
            self.LE_username.addItems(row)
        mycursor.close()

    #Todo: method for checked branches assigned to user
    def FN_check_branch(self):
        self.FN_unCheckedALL()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT BRANCH_NO FROM BRANCH"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_branch():
                if row[0] == row1[0]:
                    items = self.CMB_branch.findText(row[0])
                    for item in range(items +2):
                        if int(row1[1])==1:
                            self.CMB_branch.setChecked(i)
            i = i + 1
        mycursor.close()

    #Todo: method for get all branches assigned to user
    def FN_SELECT_branch(self):
        mycursor = self.conn.cursor()
        sql="SELECT BRANCH_NO , STATUS FROM SYS_USER_BRANCH where USER_ID = %s"
        c = (self.userid,)
        mycursor.execute(sql,c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    #Todo: method to refresh checkable combobox for branch
    def FN_unCheckedALL(self):
            mycursor = self.conn.cursor()
            sql_select_branch = "Select BRANCH_NO from BRANCH where BRANCH_STATUS=1"
            mycursor.execute(sql_select_branch)
            record = mycursor.fetchall()
            print(record)
            i = 0
            for row in record:
                self.CMB_branch.unChecked(i)
                i += 1

    #Todo: method to enable department
    def FN_EnableDepartment(self):
        if self.checkBox.isChecked():
            self.CMB_section.setEnabled(True)
        else:
            self.CMB_section.setEnabled(False)

    #Todo: method to get section assigned to user and checked it
    def FN_check_section(self):
        self.FN_unCheckedSection()
        mycursor = self.conn.cursor()
        sql_select_branch = "SELECT SECTION_ID FROM SECTION"
        mycursor.execute(sql_select_branch)
        record = mycursor.fetchall()
        i = 0
        for row in record:
            for row1 in self.FN_SELECT_section():
                if row[0] == row1[0]:
                    items = self.CMB_section.findText(row[0])
                    for item in range(items +2):
                        if int(row1[1])==1:
                            self.CMB_section.setChecked(i)
            i = i + 1
        mycursor.close()

    #Todo: method to get section assigned to user
    def FN_SELECT_section(self):
        mycursor = self.conn.cursor()
        sql="SELECT SECTION_ID , STATUS FROM SYS_USER_SECTION where USER_ID = %s"
        c = (self.userid,)
        mycursor.execute(sql,c)
        records = mycursor.fetchall()
        mycursor.close()
        return records

    #Todo: method to refresh checkable combobox for section
    def FN_unCheckedSection(self):
            mycursor = self.conn.cursor()
            sql_select_branch = "Select SECTION_ID from SECTION where SECTION_STATUS=1"
            mycursor.execute(sql_select_branch)
            record = mycursor.fetchall()
            print(record)
            i = 0
            for row in record:
                self.CMB_section.unChecked(i)
                i += 1