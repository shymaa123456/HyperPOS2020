from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from datetime import datetime


class CL_Parameters(QtWidgets.QDialog):
    dirname = ''
    def __init__(self):
        super(CL_Parameters, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Create_Parameter.ui'
        loadUi(filename, self)

        self.setWindowTitle('Parameters')
        self.BTN_createParameter.clicked.connect(self.FN_CREATE_Parameters)
        self.CMB_Status.addItems(["Active", "Inactive"])

    def FN_CREATE_Parameters(self):
        #sql_select_Query = "select * from SYS_USER where USER_NAME = '"+self.LE_name.text()+"' and USER_STATUS = 1"
        #print(sql_select_Query)
        #mycursor = self.conn.cursor()
        #mycursor.execute(sql_select_Query)
        #print(mycursor.fetchall())
        #if mycursor.rowcount>0:
        #    QtWidgets.QMessageBox.warning(self, "Error", "Username is already exists")
        #else:
        #    self.name = self.LE_name.text().strip()
        #    self.password = self.LE_password.text().strip()
        #    self.branch = self.CMB_branch.currentText()
        #    self.fullName = self.LE_fullName.text().strip()
        #   self.hrId = self.LE_hrId.text().strip()
        #    self.userType = self.CMB_userType.currentText()
        #    self.status = self.CMB_userStatus.currentText()
        #    if self.status == 'Active':
        #        self.status = 1
        #    else:
        #        self.status = 0
        #    mycursor = self.conn.cursor()
        #    # get max userid
        #    mycursor.execute("SELECT max(cast(USER_ID  AS UNSIGNED)) FROM SYS_USER")
        #    myresult = mycursor.fetchone()

        #    if myresult[0] == None:
                self.id = "1"
        #   else:
        #        self.id = int(myresult[0]) + 1

        #   creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        #    if CL_validation.FN_isEmpty(self.name) or CL_validation.FN_isEmpty(
        #            self.password) or CL_validation.FN_isEmpty(
        #            self.fullName) or CL_validation.FN_isEmpty(self.hrId):
        #        QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")

        #    else:
        #        if CL_validation.FN_validation_password(self, self.password) == False:
        #            # if  CL_validation.FN_validation_int( self, self.hrId, "HR ID" ) == True:

        #            sql = "INSERT INTO SYS_USER (USER_ID, BRANCH_NO, USER_NAME, USER_PASSWORD, USER_FULLNAME, USER_HR_ID, USER_CREATED_ON, USER_CREATED_BY, USER_CHANGED_ON, USER_CHANGED_BY,USER_STATUS, USERTYPE_ID)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"

        #            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        #            val = (
        #                self.id, self.branch, self.name, self.password, self.fullName, self.hrId, creationDate,
        #                CL_userModule.user_name, '', '', self.status,
        #                self.userType)
        #            mycursor.execute(sql, val)
        #            # mycursor.execute(sql)

        #            mycursor.close()

        #            print(mycursor.rowcount, "record inserted.")
        #            QtWidgets.QMessageBox.information(self, "Success", "User is created successfully")
        #            db1.connectionCommit(self.conn)
        #            db1.connectionClose(self.conn)
        #            self.close()