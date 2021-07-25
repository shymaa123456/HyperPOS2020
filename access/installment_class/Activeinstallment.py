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
    def __init__(self,parentInit):
        super(CL_installment_Activation, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/installment_ui'
        self.conn = db1.connect()
        self.parent = parentInit


    def FN_LOAD_Activation(self):
        filename = self.dirname + '/Activate_InstallmentProgram.ui'
        loadUi(filename, self)

        # Search for installment program
        self.Qbtn_searchInstallment.clicked.connect(self.FN_SearchForInstallmentProgram)

        #save installment program
        self.BTN_updateInstallmentProgram.clicked.connect(self.FN_UpdateInstallemtProgram)

    #Get data for installment program
    def FN_SearchForInstallmentProgram(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()

        # insert to INSTALLMENT_PROGRAM
        sql2 = "SELECT INST_DESC,INST_STATUS FROM INSTALLMENT_PROGRAM WHERE INST_PROGRAM_ID='"+self.QL_installmentNo.text()+"'"

        mycursor.execute(sql2)
        records = mycursor.fetchall()
        if len(records) >0 :

            for INST_DESC, INST_STATUS in records:
                print("INST_DESC", INST_DESC)
                print("INST_STATUS", INST_STATUS)
                self.LE_installmentTypeDesc.setText (INST_DESC)

                if INST_STATUS == str(0):
                    self.QRBTN_inactive.setChecked(True)
                elif INST_STATUS ==str(1):
                    self.QRBTN_active.setChecked(True)

        else:
            print("Program doesn't exist")
            QtWidgets.QMessageBox.information(self, "INFO", " Program doesn't exist")


        mycursor.close()


    #save Installment program
    def FN_UpdateInstallemtProgram(self):
        error = 0
        Validation_For_installmentProgramm=0

        error = self.FN_ValidateInstallemt()
        print(error)
        if error !=0:

            try:
                self.conn = db1.connect()
                self.conn.autocommit = False
                mycursor = self.conn.cursor()
                self.conn.start_transaction()

                # # lock table for new record:
                sql0 = "  LOCK  TABLES   Hyper1_Retail.INSTALLMENT_PROGRAM   WRITE "
                mycursor.execute(sql0)

                #Check if this program create before or not
                #Validation_For_installmentProgramm = 1
                #Validation_For_installmentProgramm = self.FN_ValidateInstallemtProgram(mycursor)
                #print("Validation_For_installmentProgramm",Validation_For_installmentProgramm)
                #self.FN_ValidateInstallemtProgram(mycursor )

                #get values for insert in INSTALLMENT_PROGRAM table

                ModifingDateTime = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

                # insert to INSTALLMENT_PROGRAM
                if self.QRBTN_active.isChecked():
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=1 , INST_CHANGED_ON = '"+ ModifingDateTime +"' , INST_CHANGED_BY = "+ CL_userModule.user_name +" , INST_ACTIVATED_BY = "+ CL_userModule.user_name +" where INST_PROGRAM_ID='"+self.QL_installmentNo.text()+"'"
                elif self.QRBTN_inactive.isChecked():
                    sql2 = "update Hyper1_Retail.INSTALLMENT_PROGRAM set INST_STATUS=0 , INST_CHANGED_ON = '"+ ModifingDateTime +"' , INST_CHANGED_BY = "+ CL_userModule.user_name +" , INST_DEACTIVATED_BY = "+ CL_userModule.user_name +" where INST_PROGRAM_ID='"+self.QL_installmentNo.text()+"'"

                print("sql2",sql2)
                mycursor.execute(sql2)

                # # unlock table :
                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                self.conn.commit()

            except mysql.connector.Error as error:
                print("Failed to update record to database rollback: {}".format(error))
                # reverting changes because of exception
                self.conn.rollback()
            finally:
                # closing database connection.
                if self.conn.is_connected():
                    mycursor.close()
                    self.conn.close()
                    print("connection is closed")

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
