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
    def __init__(self,pp):
        super(CL_CustService_modify, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/customer_service_ui'
        conn = db1.connect()
        self.parent = pp
    def FN_LOAD_MODIFY(self,id):
        try:
            print("id is ", id)
            filename = self.dirname + '/customerService_modify.ui'
            loadUi(filename, self)
            #get company id
            conn = db1.connect()
            mycursor = conn.cursor()
            mycursor.execute("SELECT COMPANY_ID ,CC_DEPARTMENT FROM Hyper1_Retail.CUSTOMER_COMPLAINT where CC_COMPLAINT_ID = '" + id + "'")
            myresult = mycursor.fetchone()
            mycursor.close()
            records = util.FN_GET_COMPANIES()
            for row, val in records:
                self.CMB_company.addItem(row, val)

            records = util.FN_GET_BRANCHES(myresult[0])
            for row, val in records:
                for br in CL_userModule.branch:
                    if str(val) in br:
                       self.CMB_branch.addItem(row, val)

            records = util.FN_GET_DEPARTMENTS()
            for row, val in records:
                self.CMB_department.addItem(row, val)

            records = util.FN_GET_SECTIONS(myresult[1])
            for row, val in records:
                for sec in CL_userModule.section:
                    if str(val) in sec:
                        self.CMB_section.addItem(row, val)
            self.CMB_status.addItem( "Created", '0')
            self.CMB_status.addItem( "Finished" ,'1')

            self.CMB_status.addItem("Inprogress" , '2' )

            records = self.FN_GET_COMPLAIN_TYPE()
            for row, val in records:
                self.CMB_complainType.addItem(row, val)

            self.FN_GET_CUST(id)

            self.CMB_department.activated.connect(self.FN_GET_SECTIONS)
            self.LE_custNo.textChanged.connect(self.FN_GET_CUST)
            self.btn_modify.clicked.connect(self.FN_MODIFY_CUST)

            self.setFixedWidth(723)
            self.setFixedHeight(633)

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
            self.LE_custName.setText(record[2])
            self.LE_custPhone.setText( record[3] )
            self.LE_pos.setText(record[8])
            self.LE_responsible.setText(record[10])
            self.details.setText(record[12])
            xto = record[9].split("-")

            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_invoice.setDate(d)

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
    def FN_REFRESH_GRID(self,id):
        for i in reversed(range(self.parent.Qtable_custComplains.rowCount())):
            self.parent .Qtable_custComplains.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "select    `CC_COMPLAINT_ID`,`CCT_TYPE_ID`,`POSC_CUST_ID`,`CC_CUSTOMER_NAME`,`CC_CUSTOMER_PHONE`,`COMPANY_ID`,`BRANCH_NO`,`CC_DEPARTMENT`,`CC_SECTION`,`CC_POS`,`CC_INVOICE_DATE`,`CC_RESPONSIBLE`,`CC_STATUS`" \
                               "from Hyper1_Retail.CUSTOMER_COMPLAINT where `CC_COMPLAINT_ID` = %s "
        val = (id,)
        mycursor.execute(sql_select_query,val)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.parent.Qtable_custComplains.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 1:
                    data = util.FN_GET_COMPLAIN_TYPE_DESC(str(data))
                elif column_number == 5:
                    data = util.FN_GET_COMP_DESC(str(data))
                elif column_number == 6:
                    data = util.FN_GET_BRANCH_DESC(str(data))
                elif column_number == 7:
                    data = util.FN_GET_DEPT_DESC(str(data))
                elif column_number == 8:
                    data = util.FN_GET_SEC_DESC(str(data))

                elif column_number == 12:
                    data = util.FN_GET_COMPAIN_STATUS_DESC(str(data))
                self.parent .Qtable_custComplains.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.parent .Qtable_custComplains.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        mycursor.close()

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


class CL_CustService_create(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    def __init__(self,pp):
        super(CL_CustService_create, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/customer_service_ui'
        conn = db1.connect()
        self.parent = pp
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

    def FN_REFRESH_GRID(self,id):
        for i in reversed(range(self.parent.Qtable_custComplains.rowCount())):
            self.parent .Qtable_custComplains.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "select    `CC_COMPLAINT_ID`,`CCT_TYPE_ID`,`POSC_CUST_ID`,`CC_CUSTOMER_NAME`,`CC_CUSTOMER_PHONE`,`COMPANY_ID`,`BRANCH_NO`,`CC_DEPARTMENT`,`CC_SECTION`,`CC_POS`,`CC_INVOICE_DATE`,`CC_RESPONSIBLE`,`CC_STATUS`" \
                               "from Hyper1_Retail.CUSTOMER_COMPLAINT where `CC_COMPLAINT_ID` = %s "
        val = (id,)
        mycursor.execute(sql_select_query,val)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.parent.Qtable_custComplains.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 1:
                    data = util.FN_GET_COMPLAIN_TYPE_DESC(str(data))
                elif column_number == 5:
                    data = util.FN_GET_COMP_DESC(str(data))
                elif column_number == 6:
                    data = util.FN_GET_BRANCH_DESC(str(data))
                elif column_number == 7:
                    data = util.FN_GET_DEPT_DESC(str(data))
                elif column_number == 8:
                    data = util.FN_GET_SEC_DESC(str(data))

                elif column_number == 12:
                    data = util.FN_GET_COMPAIN_STATUS_DESC(str(data))
                self.parent .Qtable_custComplains.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.parent .Qtable_custComplains.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        mycursor.close()
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

class CL_CustService(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    def __init__(self):
        super(CL_CustService, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/customer_service_ui'
        conn = db1.connect()


    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/customerٍService_display.ui'
        loadUi(filename, self)
        conn = db1.connect()
        mycursor = conn.cursor()
        self.Qbtn_search.clicked.connect(self.FN_SEARCH_CUST)

        self.Rbtn_custNo.clicked.connect(self.onClicked)
        self.Rbtn_custName.clicked.connect(self.onClicked)
        self.Rbtn_custPhone.clicked.connect(self.onClicked)
        self.Rbtn_complainNo.clicked.connect(self.onClicked)

        self.chk_search_other.stateChanged.connect(self.onClickedCheckBox)
        self.chk_search_status.stateChanged.connect(self.onClickedCheckBox1)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(1028)
        self.setFixedHeight(560)
        #check authorization
        for row_number, row_data in enumerate( CL_userModule.myList ):
           if  row_data[1] =='Customer_Service':
               if row_data[4] =='None':
                print('hh')
               else:
                   sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                   x = (row_data[4],)
                   mycursor.execute(sql_select_query, x)
                   result = mycursor.fetchone()
                   if result[0] == 'create' :
                        self.Qbtn_create.setEnabled(True)
                        self.Qbtn_create.clicked.connect(self.FN_CR_CUST)
                   elif result[0] == 'modify':
                         self.Qbtn_modify.setEnabled(True)
                         self.Qbtn_modify.clicked.connect(self.FN_MD_CUST)

        mycursor.close()

    def FN_CR_CUST(self):
        self.window_two2 = CL_CustService_create(self)

        self.window_two2.FN_LOAD_CREATE()
        self.window_two2.show()


    def FN_MD_CUST(self):

        self.window_two = CL_CustService_modify(self)
        try:
            if len(self.Qtable_custComplains.selectedIndexes()) > 0:
                rowNo=self.Qtable_custComplains.selectedItems()[0].row()
                id =self.Qtable_custComplains.item(rowNo, 0).text()
                self.window_two.FN_LOAD_MODIFY(id)
                self.window_two.show()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

        except Exception as err:
            print(err)

    def onClickedCheckBox1(self):
        if self.chk_search_status.isChecked():

            # self.LE_custNo.setEnabled(False)
            self.Rbtn_stsAll.setChecked(True)
            self.Rbtn_stsCreated.setEnabled(True)
            self.Rbtn_stsFinished.setEnabled(True)
            self.Rbtn_stsInprogress.setEnabled(True)
            self.Rbtn_stsAll.setEnabled(True)
        else:
            self.Rbtn_stsAll.setChecked(False)
            self.Rbtn_stsCreated.setEnabled(False)
            self.Rbtn_stsFinished.setEnabled(False)
            self.Rbtn_stsInprogress.setEnabled(False)
            self.Rbtn_stsAll.setEnabled(False)

    def onClickedCheckBox(self):
        if self.chk_search_other.isChecked():
            self.Rbtn_custNo.setChecked(True)
            self.Rbtn_complainNo.setEnabled(True)
            self.Rbtn_complainNo.setChecked(True)
            self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custName.setEnabled(True)
            self.Rbtn_custPhone.setEnabled(True)

            self.LE_complainNo.setEnabled(True)
            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(True)
            self.LE_custPhone.setEnabled(True)

        else:
            self.Rbtn_complainNo.setChecked(False)
            self.Rbtn_custNo.setChecked(False)
            self.Rbtn_custName.setChecked(False)
            self.Rbtn_custPhone.setChecked(False)

            self.Rbtn_complainNo.setEnabled(False)
            self.Rbtn_custNo.setEnabled(False)
            self.Rbtn_custPhone.setEnabled(False)
            self.Rbtn_custName.setEnabled(False)

            self.LE_custNo.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custName.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setText('')
            self.LE_custName.setText('')
            self.LE_complainNo.setText('')




    def onClicked(self):

        if self.Rbtn_complainNo.isChecked():

            self.LE_complainNo.setEnabled(True)
            self.LE_custNo.setEnabled(False)
            self.LE_custName.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setEnabled(False)
        elif self.Rbtn_custNo.isChecked():

            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(False)
            self.LE_custName.setText('')
            self.LE_custPhone.setEnabled(False)
            self.LE_custPhone.setText('')
            self.LE_complainNo.setEnabled(False)
            self.LE_complainNo.setText('')
        elif self.Rbtn_custPhone.isChecked():

            self.LE_custNo.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custName.setEnabled(False)
            self.LE_custName.setText('')
            self.LE_custPhone.setEnabled(True)
            self.LE_complainNo.setEnabled(False)
            self.LE_complainNo.setText('')

        elif self.Rbtn_custName.isChecked():

            self.LE_custNo.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custName.setEnabled(True)
            self.LE_custPhone.setEnabled(False)
            self.LE_complainNo.setEnabled(False)
            self.LE_complainNo.setText('')
            self.LE_custPhone.setText('')

   #search for a customer
    def FN_SEARCH_CUST(self):
        for i in reversed(range(self.Qtable_custComplains.rowCount())):
            self.Qtable_custComplains.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        whereClause = " "
        orderClause = " order by CC_COMPLAINT_ID asc"
        if self.chk_search_other.isChecked():
            if self.Rbtn_custNo.isChecked():
                id = self.LE_custNo.text()
                whereClause = whereClause + "  POSC_CUST_ID = '" + id + "'  "

            elif  self.Rbtn_custName.isChecked():
                name = self.LE_custName.text()
                whereClause = whereClause +" CC_CUSTOMER_NAME like '%" + name + "%'  "

            elif self.Rbtn_custPhone.isChecked():
                phone = self.LE_custPhone.text()
                whereClause = whereClause + " (CC_CUSTOMER_PHONE = '" + phone + "' )  "
            elif self.Rbtn_complainNo.isChecked():
                complainNo = self.LE_complainNo.text()
                whereClause = whereClause + " (CC_COMPLAINT_ID = '" + complainNo + "' )  "

        if self.chk_search_status.isChecked():
            if len (whereClause) > 1:

                whereClause = whereClause + " and "
            if self.Rbtn_stsCreated.isChecked():
                whereClause = whereClause + ' CC_STATUS = 0'
            elif self.Rbtn_stsFinished.isChecked():
                whereClause = whereClause + '  CC_STATUS = 1'
            elif self.Rbtn_stsInprogress.isChecked():
                whereClause = whereClause + '  CC_STATUS = 2'
            elif self.Rbtn_stsAll.isChecked():
                whereClause = whereClause + '  CC_STATUS in ( 0,1,2)'
        if self.chk_search_status.isChecked() == False and self.chk_search_other.isChecked() == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "أختر أي من محدادات  البحث")
        else:

            sql_select_query = "select    `CC_COMPLAINT_ID`,`CCT_TYPE_ID`,`POSC_CUST_ID`,`CC_CUSTOMER_NAME`,`CC_CUSTOMER_PHONE`,`COMPANY_ID`,`BRANCH_NO`,`CC_DEPARTMENT`,`CC_SECTION`,`CC_POS`,`CC_INVOICE_DATE`,`CC_RESPONSIBLE`,`CC_STATUS`" \
                               "from Hyper1_Retail.CUSTOMER_COMPLAINT where " + whereClause + orderClause
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_custComplains.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    if column_number == 1:
                        data = util.FN_GET_COMPLAIN_TYPE_DESC(str(data))
                    elif   column_number == 5:
                        data = util.FN_GET_COMP_DESC(str(data))
                    elif column_number == 6:
                        data = util.FN_GET_BRANCH_DESC(str(data))
                    elif column_number == 7:
                        data = util.FN_GET_DEPT_DESC(str(data))
                    elif column_number == 8:
                        data = util.FN_GET_SEC_DESC(str(data))

                    elif column_number == 12:
                        data = util.FN_GET_COMPAIN_STATUS_DESC(str(data))
                    self.Qtable_custComplains.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.Qtable_custComplains.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            mycursor.close()

