from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime
class CL_CreateBank(QtWidgets.QDialog):
    dirname = ''
    def __init__(self):
        super(CL_CreateBank, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/installment_ui'
        self.conn = db1.connect()


    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createbank.ui'
        loadUi( filename, self )

        self.setWindowTitle('أنشاء بنك')
        self.BTN_createBank.clicked.connect(self.FN_VALIDATE_BANK)

        self.CMB_bankStatus.addItems(["0","1"])

    def FN_VALIDATE_BANK(self):
        if len(self.LE_bankDesc.text()) > 0 and len(self.LE_bankAddress.text()) > 0 and len(self.LE_accountNumber.text()) > 0:
            print("Login!")
            self.bankDesc = self.LE_bankDesc.text()
            self.bankAddress = self.LE_bankAddress.text()
            self.accountNumber = self.LE_accountNumber.text()
            self.LE_bankDesc.clear()
            self.LE_bankAddress.clear()
            self.LE_accountNumber.clear()
            self.FN_CREATE_Bank(self.bankDesc, self.bankAddress , self.accountNumber)

        else:

            QtWidgets.QMessageBox.warning(self, "Error", "Please enter your Username and Password")
            # print("Please enter your Username and Password")

    def FN_CREATE_Bank(self ,bankDesc , bankAddress , accountNumber ):
        self.bankDes = self.bankDesc.strip()
        self.bankAddress = self.bankAddress.strip()
        self.accountNumber = self.accountNumber.currentText()

        self.status = self.CMB_bankStatus.currentText()

        mycursor = self.conn.cursor()
        # get max userid
        mycursor.execute("SELECT max(cast(BANK_ID  AS UNSIGNED)) FROM BANK")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if self.name == '' or self.password == '' or self.fullName == '' or self.hrId == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please all required field")

        else:

            sql = "INSERT INTO BANK (BANK_ID, BANK_DES, BANK_CREATED_ON, BANK_CREATED_BY, BANK_CHANGED_ON , BANK_CHANGED_BY, BANK_ACCOUNT_NO, BANK_ADDRESS, BANK_STATUS)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"

            # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
            val = (
                self.id, self.bankDes, creationDate, CL_userModule.user_name, '', '', self.accountNumber,
                self.bankAddress, self.status)
            mycursor.execute(sql, val)
            # mycursor.execute(sql)
            print(CL_userModule.user_name)
            mycursor.close()

            print(mycursor.rowcount, "record inserted.")
            db1.connectionCommit(self.conn)
            db1.connectionClose(self.conn)
            self.close()

    def FN_LOAD_MODIFY(self):
        filename = self.dirname + '/modifybank.ui'
        loadUi(filename, self)
        records = self.FN_GET_BanksDES()
        for row in records:
            self.CMB_bankdes.addItems([row[0]])

        self.FN_GET_BANK()
        self.CMB_bankdes.currentIndexChanged.connect(self.FN_GET_BANK)

        self.user1 = self.CMB_userName.currentText()

        self.BTN_modifyUser.clicked.connect(self.FN_MODIFY_BANK(self.user1))

        self.CMB_userStatus.addItems(["0", "1"])



    def FN_GET_BANK(self):
        bankdesc = self.CMB_bankdes.currentText()

        mycursor = self.conn.cursor()
        sql_select_query = "select * from BANK where BANK_DES = %s"
        x = (bankdesc,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        self.LE_bankDesc.setText(record[1])
        self.LE_bankAddress.setText(record[2])
        self.LE_accountNumber.setText(record[3])

        self.CMB_bankStatus.setCurrentText(record[4])


        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_BANK(self):
        #self.id = self.LB_userID.text()
        self.bankDesc = self.LE_bankDesc.text().strip()
        self.bankAddress = self.LE_bankAddress.text().strip()
        self.accountNumber = self.LE_accountNumber.text().strip()
        self.Bankstatus = self.CMB_bankStatus.currentText()
        if self.bankDesc == '' or self.bankAddress =='' or self.accountNumber == '' :
            QtWidgets.QMessageBox.warning( self, "Error", "Please all required field" )
        else:
            mycursor = self.conn.cursor()

            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            sql = "UPDATE BANK   set BANK_DESC= %s , BANK_CHANGED_ON = %s , BANK_CHANGED_BY = %s,BANK_ACCOUNT_NO = %s, BANK_ADDRESS = %s, USER_STATUS = %s where BANK_DESC= %s "
            val = (self.bankDesc  ,changeDate , CL_userModule.user_name , self.accountNumber, self.bankAddress,  self.Bankstatus , self.bankDesc )
            print(val)
            mycursor.execute(sql, val)

            mycursor.close()
            db1.connectionCommit( self.conn )
            print(mycursor.rowcount, "record Modified.")
            db1.connectionClose( self.conn )
            self.close()

    def FN_GET_BanksDES(self):

        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT BANK_DES FROM BANK order by BANK_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        return  records
    # def FN_GET_USERID(self):
    #     self.user = self.CMB_userName.currentText()
    #     mycursor = self.conn.cursor()
    #     sql_select_query= "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s "
    #     x = (self.user,)
    #     mycursor.execute(sql_select_query, x)
    #     myresult = mycursor.fetchone()
    #     self.LB_userID.setText(myresult [0])

    def FN_GET_USERID_N(self,user):

        mycursor = self.conn.cursor()
        sql_select_query= "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s "
        x = (user,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        return myresult[0]



    def FN_RESET_USER(self):
        mycursor = self.conn.cursor()

        changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
        if self.LE_password.text()  == self.LE_password2.text() :

            sql = "UPDATE SYS_USER   set   USER_PASSWORD= %s  , USER_CHANGED_ON = %s , USER_CHENGED_BY = %s where USER_NAME= %s "
            val = ( self.LE_password.text(), changeDate, CL_userModule.user_name,CL_userModule.user_name)
            #print( val )
            mycursor.execute( sql, val )
            mycursor.close()
            db1.connectionCommit( self.conn )
            print( mycursor.rowcount, "password changed" )
            db1.connectionClose( self.conn )
            self.close()
        else:
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter 2 different Passwords" )


    def FN_LOAD_RESET(self):
        filename = self.dirname + '/resetUserPassword.ui'
        loadUi( filename, self )
        self.BTN_resetPass.clicked.connect(self.FN_RESET_USER)


    def FN_LOAD_COPY(self):
        filename = self.dirname + '/copyUser.ui'
        loadUi( filename, self )

        records = self.FN_GET_BanksDES()
        for row in records:
            self.CMB_userName.addItems( [row[0]] )
            self.CMB_userName1.addItems( [row[0]] )

        self.BTN_copyUser.clicked.connect(self.FN_COPY_USER)
        self.CMB_userName.currentIndexChanged.connect( self.FN_ASSIGN_ID )
        self.CMB_userName1.currentIndexChanged.connect(self.FN_ASSIGN_ID)
        self.FN_ASSIGN_ID()

    def FN_ASSIGN_ID (self):
        self.user1 = self.CMB_userName.currentText()
        self.user2 = self.CMB_userName1.currentText()
        self.LB_userID.setText( self.FN_GET_USERID_N( self.user1 ) )
        self.LB_userID2.setText( self.FN_GET_USERID_N( self.user2 ) )
    def FN_COPY_USER(self):
        newUser=  self.LB_userID2.text()

        if self.user1 == self.user2 :
            QtWidgets.QMessageBox.warning( self, "Error", "Please enter 2 different users" )
        else:
            mycursor = self.conn.cursor()
            mycursor1 = self.conn.cursor()
            mycursor2 = self.conn.cursor()

            sql_select_query = "select ur.ROLE_ID ,ur.BRANCH_NO ,ur.UR_STATUS  " \
                               "from SYS_USER_ROLE  ur  inner join SYS_USER u ON u.USER_ID = ur.USER_ID  " \
                               "where  u.USER_NAME = %s "
            x = (self.user1,)
            mycursor.execute( sql_select_query, x )
            records = mycursor.fetchall()
            #delete current assignment if found
            mycursor2 = self.conn.cursor()
            sql_select_query1 = "delete from SYS_USER_ROLE where USER_ID = '" + newUser + "'"
            mycursor2.execute( sql_select_query1 )
            db1.connectionCommit( self.conn )

            mycursor1.execute( "SELECT max(cast(UR_USER_ROLE_ID  AS UNSIGNED)) FROM SYS_USER_ROLE" )
            myresult = mycursor1.fetchone()

            creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
            id = int( myresult[0] ) + 1
            for row in records:

                mycursor3 = self.conn.cursor()
                # sql = " INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS) VALUES ( "+id+", "+newUser+", "+row[0]+", '"+row[1]+"','"+CL_userModule.user_name+"', '"+creationDate+"',' ',' ' ,'"+row[2]+"')"
                sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
                      "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"

                val = (id, newUser, row[0], row[1], '', creationDate, '', '', row[2])
                print( str( sql ) )
                # val = (id,newUser,  row[0], row[1], CL_userModule.user_name, creationDate, '', '', row[2],)
                mycursor3.execute( sql, val )

                db1.connectionCommit( self.conn )
                print( mycursor3.rowcount, "record inserted." )
                id = id + 1

                # sql_select_query = "select * from SYS_USER_ROLE where USER_ID ='"+newUser+"' and ROLE_ID = '"+row[0]+"'"
                # print(sql_select_query)
                #
                # mycursor2.execute( sql_select_query)
                # print("mycursor2.rowcount is "+ str(mycursor2.rowcount))
                # if mycursor2.rowcount > 0:
                #     print("h")
                # else:
                #     mycursor3 = self.conn.cursor()
                #     #sql = " INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS) VALUES ( "+id+", "+newUser+", "+row[0]+", '"+row[1]+"','"+CL_userModule.user_name+"', '"+creationDate+"',' ',' ' ,'"+row[2]+"')"
                #     sql = "INSERT INTO SYS_USER_ROLE (UR_USER_ROLE_ID, USER_ID, ROLE_ID, BRANCH_NO, UR_CREATED_BY, UR_CREATED_ON, UR_CHANGED_BY, UR_CHANGED_ON, UR_STATUS)      " \
                #           "VALUES ( %s, %s, %s, %s,%s, %s,%s,%s,%s)"
                #
                #     val = (id, newUser,row[0], row[1], '', creationDate, '', '', row[2])
                #     print(str(sql))
                #     #val = (id,newUser,  row[0], row[1], CL_userModule.user_name, creationDate, '', '', row[2],)
                #     mycursor3.execute( sql, val)
                #
                #
                #     db1.connectionCommit( self.conn )
                #     print( mycursor3.rowcount, "record inserted." )
                #     id = id + 1
            mycursor2.close()
            mycursor1.close()
            mycursor.close()
            self.close()
