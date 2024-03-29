from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
import mysql.connector
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule
from datetime import datetime

class CL_installment_Activation(QtWidgets.QDialog):
    dirname = ''
    parent = ''
    oldstatus=""
    InstallmentNo=""
    #conn=''
    # mycursor=''
    def __init__(self,parentInit):
        super(CL_installment_Activation, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/installment_ui'

        self.parent = parentInit
        print("int CL_installment_Activation ",self.parent.mycursor)
        self.conn = self.parent.conn #.rollback()
        self.mycursor = self.parent.mycursor

        # self.mycursor = self.parent.mycursor
        # self.mycursor.rollback()
        # self.conn = self.parent.conn
        # self.mycursor = self.parent.mycursor  #self.conn.cursor()
        # sql2 = "SELECT INST_DESC,INST_STATUS FROM INSTALLMENT_PROGRAM WHERE INST_PROGRAM_ID='38'"
        # self.parent.mycursor.execute(sql2)
        #self.conn.start_transaction()

    def FN_LOAD_Activation(self):
        filename = self.dirname + '/Activate_InstallmentProgram.ui'
        loadUi(filename, self)

        # Search for installment program
        self.Qbtn_searchInstallment.clicked.connect(self.FN_SearchForInstallmentProgram)

        #save installment program
        self.BTN_updateInstallmentProgram.clicked.connect(self.FN_UpdateInstallemtProgram)

    #Get data for installment program
    def FN_SearchForInstallmentProgram(self):
        self.InstallmentNo=self.QL_installmentNo.text()
        #self.conn = db1.connect()
        #mycursor = self.conn.cursor()

        # insert to INSTALLMENT_PROGRAM
        sql2 = "SELECT INST_DESC,INST_STATUS FROM INSTALLMENT_PROGRAM WHERE INST_PROGRAM_ID='"+self.InstallmentNo+"';"
        print("FN_SearchForInstallmentProgram",sql2)
        self.parent.mycursor.execute(sql2)
        records = self.mycursor.fetchall()
        if len(records) >0 :

            for INST_DESC, INST_STATUS in records:
                print("INST_DESC", INST_DESC)
                print("INST_STATUS", INST_STATUS)
                self.LE_installmentTypeDesc.setText (INST_DESC)

                if INST_STATUS == str(0):
                    self.QRBTN_inactive.setChecked(True)
                    self.oldstatus=str(0)
                elif INST_STATUS ==str(1):
                    self.QRBTN_active.setChecked(True)
                    self.oldstatus=str(1)

        else:
            print("Program doesn't exist")
            QtWidgets.QMessageBox.information(self, "INFO", " Program doesn't exist")


        #mycursor.close()

    #save Installment program
    def FN_UpdateInstallemtProgram(self):
        error = 0
        Validation_For_installmentProgramm=0
        self.BTN_updateInstallmentProgram.setEnabled(False)
        error = self.FN_ValidateInstallemt()
        print(error)
        if error !=0:

            try:
                """
                # get values for insert in INSTALLMENT_PROGRAM table
                ModifingDateTime = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                creationDate = str(datetime.today().strftime('%Y-%m-%d'))

                sql0 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=2 , INST_CHANGED_ON = '" + ModifingDateTime +\
                       "' , INST_CHANGED_BY = " + CL_userModule.user_name + " , INST_ACTIVATED_BY = " + CL_userModule.user_name + \
                       " where INST_PROGRAM_ID='" + self.InstallmentNo + "'"
                print("sql0", sql0)
                self.mycursor.execute(sql0)
                """

                #self.conn = db1.connect()
                self.parent.conn.autocommit = False
                #mycursor = self.conn.cursor()
                #self.conn.start_transaction()

                # # lock table for new record:
                sql0 = "  LOCK  TABLES   Hyper1_Retail.INSTALLMENT_PROGRAM   WRITE , Hyper1_Retail.SYS_CHANGE_LOG  WRITE"
                self.parent.mycursor.execute(sql0)

                #get values for insert in INSTALLMENT_PROGRAM table
                ModifingDateTime = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                creationDate = str(datetime.today().strftime('%Y-%m-%d'))

                # insert to INSTALLMENT_PROGRAM
                if self.QRBTN_active.isChecked():
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=1 , INST_CHANGED_ON = '"+ ModifingDateTime +"' , INST_CHANGED_BY = "+ CL_userModule.user_name +" , INST_ACTIVATED_BY = "+ CL_userModule.user_name +" where INST_PROGRAM_ID='"+self.InstallmentNo+"'"
                    val8 = (self.InstallmentNo, 'INSTALLMENT_PROGRAM', 'INST_STATUS', self.oldstatus,
                            str(1),
                            creationDate,
                            CL_userModule.user_name)
                elif self.QRBTN_inactive.isChecked():
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=0 , INST_CHANGED_ON = '"+ ModifingDateTime +"' , INST_CHANGED_BY = "+ CL_userModule.user_name +" , INST_DEACTIVATED_BY = "+ CL_userModule.user_name +" where INST_PROGRAM_ID='"+self.InstallmentNo+"'"
                    val8 = (self.InstallmentNo, 'INSTALLMENT_PROGRAM', 'INST_STATUS', self.oldstatus,
                        str(0),
                        creationDate,
                        CL_userModule.user_name)

                print("sql2",sql2)
                self.parent.mycursor.execute(sql2)

                #Insert in log table
                sql8 = "INSERT INTO SYS_CHANGE_LOG (ROW_KEY_ID,TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY) VALUES (%s,%s,%s,%s,%s,%s,%s)"

                self.parent.mycursor.execute(sql8, val8)

                # # unlock table :
                sql00 = "  UNLOCK   tables    "
                self.parent.mycursor.execute(sql00)
                self.parent.conn.commit()

            except mysql.connector.Error as error:
                print("Failed to update record to database rollback: {}".format(error))

                # reverting changes because of exception
                self.parent.conn.rollback()
            finally:
                # closing database connection.
                if self.parent.conn.is_connected():
                    #mycursor.close()
                    #self.conn.close()
                    sql00 = "  UNLOCK   tables    "
                    self.parent.mycursor.execute(sql00)

                    self.BTN_updateInstallmentProgram.setEnabled(True)

                    print("connected")

    def FN_ValidateInstallemt(self):
        error=0
        if len(self.LE_installmentTypeDesc.text()) == 0:
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى البحث اولا")
            error = 0

        elif not self.QRBTN_active.isChecked() and not self.QRBTN_inactive.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", " يرجى البحث اولا")
            error = 0
        else:
            error = 1

        return error
