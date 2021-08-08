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

class CL_CustService_modify(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    oldmobile=''
    oldstatus=''
    oldemail=''
    def __init__(self):
        super(CL_CustService_modify, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/customer_service_ui'
        conn = db1.connect()

    def FN_LOAD_MODIFY(self):
        try:
            #print("id is ", id)
            filename = self.dirname + '/customerService_modify.ui'
            loadUi(filename, self)
            #get company id
            conn = db1.connect()
            #mycursor = conn.cursor()

            #mycursor.close()
            records = util.FN_GET_COMPANIES()
            for row, val in records:
                self.CMB_company.addItem(row, val)


            records = util.FN_GET_DEPARTMENTS()
            for row, val in records:
                self.CMB_department.addItem(row, val)

            self.CMB_status.addItem( "Created", '0')
            self.CMB_status.addItem( "Finished" ,'1')

            self.CMB_status.addItem("Inprogress" , '2' )

            records = self.FN_GET_COMPLAIN_TYPE()
            for row, val in records:
                self.CMB_complainType.addItem(row, val)

            self.CMB_department.activated.connect(self.FN_GET_SECTIONS)
            #self.LE_custNo.textChanged.connect(self.FN_GET_CUST)
            #self.Rbtn_custNo.clicked.connect(self.onClicked)
            #self.Rbtn_complainNo.clicked.connect(self.onClicked)

            self.btn_modify.clicked.connect(self.FN_MODIFY_CUST)
            self.Qbtn_search.clicked.connect(self.FN_SEARCH_CUST_SERVICE)
            #self.setFixedWidth(723)
            #self.setFixedHeight(633)

        except Exception as err:
            print(err)
    def onClicked(self):
        if self.Rbtn_custNo.isChecked():
            self.LE_custNo.setEnabled(True)
            self.Rbtn_complainNo.setEnabled(False)
            self.Rbtn_complainNo.setText('')
        elif self.Rbtn_custName.isChecked():

            self.LE_custNo.setEnabled(False)
            self.Rbtn_complainNo.setEnabled(True)
            self.LE_custNo.setText('')
    def FN_SEARCH_CUST_SERVICE(self):
        try:
            whereClause = "  "

            if self.Rbtn_custNo.isChecked():
                id = self.LE_custNo.text()
                whereClause =  "  POSC_CUST_ID = '" + id + "'  "

            if self.Rbtn_complainNo.isChecked():
                name = self.LE_complainNo.text()
                whereClause = " CC_COMPLAINT_ID = '" + name + "'  "

            if self.Rbtn_custNo.isChecked() == False and self.Rbtn_complainNo.isChecked() == False:
                QtWidgets.QMessageBox.warning(self, "خطأ", "أختر أي من محدادات  البحث")
            else:
                conn = db1.connect()
                mycursor = conn.cursor()
                print(whereClause)
                sql_select_query = "select  CC_COMPLAINT_ID from Hyper1_Retail.CUSTOMER_COMPLAINT where " + whereClause

                mycursor.execute(sql_select_query)
                records = mycursor.fetchone()

                self.FN_GET_CUST(str(records[0]))

                mycursor.close()
            # self.Qbtn_search.setEnabled(True)
        except Exception as err:
            print(err)
    def FN_GET_STATUS_ID(self):
        status = self.CMB_status.currentData()
        id = ""
        if status == "Active":
            id='1'
        elif status == "Inactive":
            id = '0'
        elif status == "Inprogress":
            id = '2'

    def FN_MODIFY_CUST(self):
        #get customer data
        try:
            id = self.LE_complainNo.text().strip()
            complainType = self.CMB_complainType.currentData()
            # city = self.CMB_city.currentData()
            # branch = self.CMB_branch.currentData()
            # dept = self.CMB_city.currentData()
            # sec = self.CMB_branch.currentData()
            status = self.CMB_status.currentData()
            responsible = self.LE_responsible.text().strip()
            details = self.details.toPlainText().strip()
            #details
            conn = db1.connect()
            mycursor = conn.cursor()

            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))


            sql = "update  Hyper1_Retail.CUSTOMER_COMPLAINT  set CCT_TYPE_ID = %s  ,CC_STATUS =%s " \
                  ",CC_RESPONSIBLE = %s  ,CC_CHANGED_ON = %s , CC_CHANGED_BY = %s,CC_DETAIL = %s  where CC_COMPLAINT_ID = %s"
            print(sql)
            val = (complainType,status,responsible,changeDate, CL_userModule.user_name,details,id)
            mycursor.execute(sql, val)
            mycursor.close()

            print(mycursor.rowcount, "record updated.")
            QtWidgets.QMessageBox.information(self, "تم", "تم التعديل")
            db1.connectionCommit(conn)

            self.close()
            self.FN_REFRESH_GRID(id)
            if self.oldStatus != status:
                util.FN_INSERT_IN_LOG("CUSTOMER_COMPLAINT","status",status,self.oldStatus,id)
            if self.oldResponsible != responsible:
                util.FN_INSERT_IN_LOG("CUSTOMER_COMPLAINT","responsible",responsible,self.oldResponsible,id)
            if str(self.oldComplainType) != str(complainType):
                util.FN_INSERT_IN_LOG("CUSTOMER_COMPLAINT","complainType",complainType,self.oldComplainType,id)
        except Exception as err:
            print(err)

    def FN_GET_CUST(self,id):
        try:

            conn = db1.connect()
            mycursor = conn.cursor()
            sql_select_query ="select    `CCT_TYPE_ID`,`POSC_CUST_ID`,`CC_CUSTOMER_NAME`,`CC_CUSTOMER_PHONE`,`COMPANY_ID`,`BRANCH_NO`,`CC_DEPARTMENT`,`CC_SECTION`,`CC_POS`,`CC_INVOICE_DATE`,`CC_RESPONSIBLE`,`CC_STATUS` ,CC_DETAIL " \
                               "from Hyper1_Retail.CUSTOMER_COMPLAINT where CC_COMPLAINT_ID = '"+id+"'"
            print(sql_select_query)
            mycursor.execute( sql_select_query )
            record = mycursor.fetchone()
            self.LE_complainNo.setText(id)
            self.LE_custNo.setText(record[1])
            #self.LE_custName.setText(record[2])
            #self.LE_custPhone.setText( record[3] )
            self.LE_pos.setText(record[8])
            self.LE_responsible.setText(record[10])
            self.details.setText(record[12])
            xto = record[9].split("-")

            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_invoice.setDate(d)

            records = util.FN_GET_BRANCHES(record[4])
            for row, val in records:
                for br in CL_userModule.branch:
                    if str(val) in br:
                        self.CMB_branch.addItem(row, val)

            records = util.FN_GET_SECTIONS(record[6])
            for row, val in records:
                for sec in CL_userModule.section:
                    if str(val) in sec:
                        self.CMB_section.addItem(row, val)

            self.CMB_status.setCurrentText(util.FN_GET_COMPAIN_STATUS_DESC(record[11]))
            self.CMB_complainType.setCurrentText(util.FN_GET_COMPLAIN_TYPE_DESC(str(record[0])))
            self.CMB_company.setCurrentText(util.FN_GET_COMP_DESC( record[4]))
            self.CMB_branch.setCurrentText(util.FN_GET_BRANCH_DESC(record[5]))
            self.CMB_department.setCurrentText(util.FN_GET_DEPT_DESC( record[6]))
            self.CMB_section.setCurrentText(util.FN_GET_SEC_DESC( record[7]))

            self.oldStatus = record[11]
            self.oldComplainType = record[0]
            self.oldResponsible = record[10]
            mycursor.close()
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
