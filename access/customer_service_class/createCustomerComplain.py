from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QTextBrowser
from PyQt5.uic import loadUi

from Validation.Validation import CL_validation

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import xlrd
from datetime import datetime
import xlwt.Workbook
from access.utils.util import *


class CL_CustService_create(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    def __init__(self):
        super(CL_CustService_create, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/customer_service_ui'
        conn = db1.connect()

    def FN_LOAD_CREATE(self):
        try:
            filename = self.dirname + '/customerService_create.ui'
            loadUi(filename, self)

            records = util.FN_GET_COMPANIES()
            for row, val in records:
                self.CMB_company.addItem(row, val)
            comp = self.CMB_company.currentData()

            records = util.FN_GET_BRANCHES(comp)
            for row, val in records:
                for br in CL_userModule.branch:
                    if str(val) in br:
                        self.CMB_branch.addItem(row, val)

            records = util.FN_GET_DEPARTMENTS()
            for row, val in records:
                self.CMB_department.addItem(row, val)
            dept=self.CMB_department.currentData()

            records = util.FN_GET_SECTIONS(dept)
            for row, val in records:
                for sec in CL_userModule.section:
                    if str(val) in sec:
                        self.CMB_section.addItem(row, val)

            records = self.FN_GET_COMPLAIN_TYPE()
            for row, val in records:
                self.CMB_complainType.addItem(row, val)

            self.CMB_department.activated.connect(self.FN_GET_SECTIONS)
            self.BTN_create.clicked.connect(self.FN_CREATE_CUST)
            self.LE_custNo.textChanged.connect(self.FN_GET_CUST)
            #
            self.setFixedWidth(723)
            self.setFixedHeight(602)
        except Exception as err:
            print(err)
    def FN_GET_COMPLAIN_TYPE(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CCT_DESC ,CCT_TYPE_ID FROM Hyper1_Retail.CUSTOMER_COMPLAINT_TYPE where CCT_STATUS = 1")
        myresult = mycursor.fetchall()
        mycursor.close()
        return myresult
    def FN_GET_SECTIONS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_section.clear()
        dept = self.CMB_department.currentData()

        sql_select_query = "SELECT SECTION_DESC ,SECTION_ID  FROM Hyper1_Retail.SECTION where SECTION_STATUS   = 1 and `DEPARTMENT_ID`= '" + dept + "'"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        if mycursor.rowcount >0 :
            for row, val in records:
                for sec in CL_userModule.section:
                    if str(val) in sec:
                        self.CMB_section.addItem(row, val)


    def FN_CREATE_CUST(self):
        #get customer data
        try:

            print("here")
            self.parent.Qtable_custComplains.insertRow(0)
            no = self.LE_custNo.text().strip()
            name = self.LE_custName.text().strip()
            phone = self.LE_custPhone .text().strip()
            complainType = self.CMB_complainType.currentData()

            company = self.CMB_company.currentData()
            branch = self.CMB_branch.currentData()
            department = self.CMB_department.currentData()
            section  = self.CMB_section.currentData()
            pos =  self.LE_pos.text().strip()
            invoiceNo = self.Qdate_invoice.date().toString('yyyy-MM-dd')


            details = self.details.toPlainText().strip()
            print(details)
            conn = db1.connect()
            mycursor = conn.cursor()

            creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

            self.status = 0

            error =0
            error = self.FN_VALIDATE_FIELDS()

            if error !=1:
                sql0 = "  LOCK  TABLES    Hyper1_Retail.CUSTOMER_COMPLAINT   WRITE "
                mycursor.execute(sql0)

                sql = "INSERT INTO Hyper1_Retail.CUSTOMER_COMPLAINT(`CCT_TYPE_ID`,`POSC_CUST_ID`,`CC_CUSTOMER_NAME`,`CC_CUSTOMER_PHONE`,`COMPANY_ID`,`BRANCH_NO`,`CC_DEPARTMENT`,`CC_SECTION`,`CC_POS`,`CC_INVOICE_DATE`,CC_DETAIL,`CC_STATUS`,CC_CREATED_ON ,CC_CREATED_BY)  " \
                      "VALUES (  %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                      "%s,%s,  %s, %s,%s)"

                           # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                val = ( complainType,no , name,    phone ,company,branch,    department,section,pos,invoiceNo,details,'0' ,creationDate,CL_userModule.user_name     )
                mycursor.execute( sql, val )
                print( mycursor.rowcount, "record inserted." )
                #get max id
                mycursor.execute("SELECT max(CC_COMPLAINT_ID ) FROM Hyper1_Retail.CUSTOMER_COMPLAINT")
                myresult = mycursor.fetchone()
                id = myresult[0]
                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                db1.connectionCommit( conn )
                #db1.connectionClose( self.conn )
                QtWidgets.QMessageBox.information(self, "تم", "تم الإنشاء بنجاح")

                self.close()
                #update parent
                self.FN_REFRESH_GRID(id)
                #self.parent.Qtable_customer.insertRow(2)
                print(id)
                print("in create cust" ,name)
                mycursor.close()
        except Exception as err:
            print(err)


    def FN_VALIDATE_FIELDS(self):
        no = self.LE_custNo.text().strip()
        name = self.LE_custName.text().strip()
        phone = self.LE_custPhone.text().strip()

        error = 0
        if name == '' or phone == '' :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
            error = 1
        else:
            ret = CL_validation.FN_validation_int(phone)
            if ret == False:
                QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل غير صحيح")
                error = 1

            ret = CL_validation.FN_validation_mobile(phone)
            if ret == 3:
                QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل يجب أن يكون 11 رقم")
                error = 1
            elif ret == 2:
                QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل يجب أن يبدأ ب 01")
                error = 1

            # ret = util.FN_VALIDATE_CUST(no)
            # if ret == False:
            #     QtWidgets.QMessageBox.warning(self, "خطأ", "رقم العميل غير صحيح")
            #     error = 1
        return error

    def FN_GET_CUST (self):
        conn = db1.connect()
        mycursor = conn.cursor()
        no = self.LE_custNo.text().strip()
        self.LE_custPhone.setText('')
        self.LE_custName.setText('')

        sql = "SELECT POSC_NAME,POSC_MOBILE FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(no) + "'"
        print(sql)
        mycursor.execute(sql)
        myresult = mycursor.fetchone()

        if mycursor.rowcount >0:
            self.LE_custPhone.setText(myresult[1])
            self.LE_custName.setText(myresult[0])
        mycursor.close()
