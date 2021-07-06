from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
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
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()
        self.parent = pp
    def FN_LOAD_MODIFY(self,id):
        try:
            print("id is ", id)
            filename = self.dirname + '/modifyCustomer.ui'
            loadUi(filename, self)
            records = util.FN_GET_CUSTTP()
            for row,val in records:
                self.CMB_loyalityType.addItem(row,val)

            records = util.FN_GET_CUSTGP()

            for row, val in records:
                self.CMB_custGroup.addItem(row, val)

            self.CMB_status.addItems(["Active", "Inactive"])
            self.FN_GET_CUST(id)


            self.CMB_city.currentIndexChanged.connect(self.FN_GET_DISTRICT)
            self.BTN_modifyCustomer.clicked.connect(self.FN_MODIFY_CUST)

            self.setFixedWidth(1056)
            self.setFixedHeight(540)

        except Exception as err:
            print(err)

    def FN_GET_DISTRICT(self):
        self.CMB_district.clear()
        if self.CMB_city.currentData() != None:
            conn = db1.connect()
            mycursor = conn.cursor()
            sql = "SELECT DISTRICT_NAME ,DISTRICT_ID FROM Hyper1_Retail.DISTRICT where CITY_ID = %s and DISTRICT_STATUS = 1  order by DISTRICT_ID asc"
            val = (self.CMB_city.currentData(),)
            mycursor.execute(sql, val)
            records = mycursor.fetchall()

            for row, val in records:
                self.CMB_district.addItem(row, val)
            mycursor.close()
    def FN_MODIFY_CUST(self):
        #get customer data
        try:
            self.id = self.LB_custID.text().strip()

            self.name = self.LE_name.text().strip()
            self.custGroup = self.CMB_custGroup.currentData()
            self.loyalityType = self.CMB_loyalityType.currentData()
            self.phone = self.lE_phone.text().strip()
            self.mobile = self.lE_mobile.text().strip()
            self.job = self.LE_job.text().strip()
            self.address = self.LE_address.text().strip()
            self.city = self.CMB_city.currentData()
            self.district = self.CMB_district.currentData()
            self.building = self.LE_building.text().strip()
            self.floor = self.LE_floor.text().strip()
            self.email = self.LE_email.text().strip()
            self.company = self.LE_company.text().strip()
            self.workPhone = self.LE_workPhone.text().strip()
            self.workAddress = self.LE_workAddress.text().strip()
            self.status = self.CMB_status.currentText()
            self.notes = self.LE_notes.toPlainText().strip()
            self.nationalID = self.LE_nationalID.text().strip()
            conn = db1.connect()
            mycursor = conn.cursor()

            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

            self.status = self.CMB_status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0
            error = 0
            error = self.FN_VALIDATE_FIELDS()

            if error != 1:
                sql = "update  Hyper1_Retail.POS_CUSTOMER  set  LOYCT_TYPE_ID=%s, CG_GROUP_ID=%s,  POSC_NAME = %s , POSC_PHONE=%s," \
                      " POSC_MOBILE=%s, POSC_JOB=%s, POSC_ADDRESS=%s, POSC_CITY=%s, POSC_DISTICT=%s, POSC_BUILDING=%s,POSC_FLOOR=%s, POSC_EMAIL=%s, " \
                      "POSC_CHANGED_BY =%s, POSC_CHANGED_ON =%s, POSC_COMPANY=%s, " \
                      "POSC_WORK_PHONE=%s, POSC_WORK_ADDRESS=%s, POSC_NOTES=%s, POSC_STATUS=%s ,`POSC_NATIONAL_ID` = %s where POSC_CUST_ID = %s"

                # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                val = (self.loyalityType, self.custGroup, self.name, self.phone, self.mobile,
                       self.job, self.address, self.city, self.district, self.building, self.floor, self.email,
                       CL_userModule.user_name, changeDate, self.company, self.workPhone, self.workAddress,
                       self.notes, self.status, self.nationalID,self.id)
                mycursor.execute(sql, val)
                # mycursor.execute(sql)

                mycursor.close()

                print(mycursor.rowcount, "record updated.")
                QtWidgets.QMessageBox.information(self, "Success", "تم التعديل")

                db1.connectionCommit(conn)
                # db1.connectionClose( self.conn )
                # self.FN_INSERT_IN_LOG(tableName,)
                self.close()
                self.FN_REFRESH_GRID(self.id)
                if self.mobile != self.oldmobile:
                    util.FN_INSERT_IN_LOG("POS_CUSTOMER","mobile",self.mobile,self.oldmobile,self.id)
                if self.email != self.oldemail:
                    util.FN_INSERT_IN_LOG("POS_CUSTOMER","email",self.email,self.oldemail,self.id)
                if str(self.status) != str(self.oldstatus):
                    util.FN_INSERT_IN_LOG("POS_CUSTOMER","status",self.status,self.oldstatus,self.id)
        except Exception as err:
            print(err)



    def FN_GET_CUST(self,id):
        try:
        #self.FN_GET_CustID()
        #self.id = self.LB_custID.text()
            self.LB_custID.setText(id)
            conn = db1.connect()
            mycursor = conn.cursor()
            sql_select_query = "select POSC_NAME,`POSC_PHONE`,`POSC_MOBILE`,`POSC_JOB`,`POSC_ADDRESS`,`POSC_BUILDING`,`POSC_FLOOR`,`POSC_EMAIL`,`POSC_COMPANY`,`POSC_WORK_PHONE`,`POSC_WORK_ADDRESS` ,`POSC_NOTES`,`POSC_NATIONAL_ID` " \
                               ",`POSC_CITY`,`POSC_DISTICT`,`LOYCT_TYPE_ID`,`CG_GROUP_ID`,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = %s "
            x = (id,)
            mycursor.execute( sql_select_query, x )
            record = mycursor.fetchone()
            #print( record )
            self.LE_name.setText(record[0])
            self.lE_phone.setText( record[1] )
            self.lE_mobile.setText( record[2] )
            self.LE_job.setText( record[3] )
            self.LE_address.setText( record[4] )

            self.LE_building.setValue( int(record[5] ))
            self.LE_floor.setValue(int( record[6] ))
            self.LE_email.setText( record[7] )
            self.LE_company.setText( record[8] )
            self.LE_workPhone.setText( record[9] )
            self.LE_workAddress.setText( record[10] )
            self.LE_notes.setText( record[11] )
            self.LE_nationalID.setText( record[12] )
            self.CMB_status.setCurrentText(util.FN_GET_STATUS_DESC(record[17]))
            self.CMB_custGroup.setCurrentText(util.FN_GET_CUSTTG_DESC(record[16] ))
            self.CMB_loyalityType.setCurrentText( util.FN_GET_CUSTTP_DESC(record[15] ))

            records = util.FN_GET_CITIES()
            for row, val in records:
                self.CMB_city.addItem(row, val)

            self.CMB_city.setCurrentText( util.FN_GET_CITY_DESC(record[13]))

            records = util.FN_GET_DISTRICT(record[13])
            for row, val in records:
                self.CMB_district.addItem(row, val)
            self.CMB_district.setCurrentText( util.FN_GET_DISTRICT_DESC(record[14]))

            self.oldmobile = record[2]
            self.oldstatus = record[17]
            self.oldemail = record[7]
            mycursor.close()


        except Exception as err:
            print(err)

    def FN_REFRESH_GRID(self,id):
        for i in reversed(range(self.parent.Qtable_customer.rowCount())):
            self.parent .Qtable_customer.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = %s"
        #print(sql_select_query)
        val = (str(id),)
        mycursor.execute(sql_select_query,val)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.parent.Qtable_customer.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 12:
                    data = util.FN_GET_STATUS_DESC(str(data))
                elif column_number == 2:
                    data = util.FN_GET_CUSTTP_DESC(str(data))
                elif column_number == 7:
                    data = util.FN_GET_CITY_DESC(str(data))

                elif column_number == 8:
                    data = util.FN_GET_DISTRICT_DESC(str(data))
                self.parent .Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.parent .Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        mycursor.close()
    def FN_VALIDATE_FIELDS(self):
        id = self.LB_custID.text().strip()
        self.name = self.LE_name.text().strip()

        self.phone = self.lE_phone.text().strip()
        self.mobile = self.lE_mobile.text().strip()


        self.building = self.LE_building.text().strip()
        self.floor = self.LE_floor.text().strip()
        self.email = self.LE_email.text().strip()
        self.company = self.LE_company.text().strip()
        self.workPhone = self.LE_workPhone.text().strip()
        self.workAddress = self.LE_workAddress.text().strip()
        nationalID = self.LE_nationalID.text().strip()
        error = 0
        if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.building == '' \
                or self.floor == '' or self.email == '' or nationalID == '':
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
            error = 1
            return error
        ret = CL_validation.FN_validation_int(self.phone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم التليفون غير صحيح")
            error = 1

        ret = CL_validation.FN_validation_mobile(self.mobile)
        if ret == 3:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل يجب أن يكون 11 رقم")
            error = 1
        elif ret == 2:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل يجب أن يبدأ ب 01")
            error = 1

        ret = self.FN_CHECK_REPEATED_MOBILE(self.mobile,id)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "موبايل مكرر ")
            error = 1

        ret = CL_validation.FN_validation_int(self.workPhone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم هاتف غير صحيح")
            error = 1
        ret = self.FN_CHECK_REPEATED_NATIONALID(nationalID,id)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم بطاقه مكرر ")
            error = 1
        ret = CL_validation.FN_validation_int(nationalID)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم البطاقه غير صحيح")
            error = 1
        ret = CL_validation.FN_validation_nationalID(nationalID)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم اليطاقه يجب أن يكون 14 رقم")
            error = 1
        ret = CL_validation.FN_valedation_mail(self.email)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "إيميل غير صحسح")
            error = 1
        return error
    def FN_CHECK_REPEATED_MOBILE(self,mobile,id):
       try:
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max id
            mycursor.execute("SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_MOBILE ='"+mobile+"' and POSC_CUST_ID  != '"+id+"'")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False

       except Exception as err:
             print(err)
    def FN_CHECK_REPEATED_NATIONALID(self,nationalID,id):
       try:
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max id
            mycursor.execute("SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_NATIONAL_ID ='"+nationalID+"' and POSC_CUST_ID  != '"+id+"'")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False

       except Exception as err:
             print(err)
class CL_CustService_create(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    def __init__(self,pp):
        super(CL_CustService_create, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()
        self.parent = pp
    def FN_LOAD_CREATE(self):
        try:
            filename = self.dirname + '/createCustomer.ui'
            loadUi(filename, self)

            records = util.FN_GET_CUSTGP()
            for row, val in records:
                self.CMB_custGroup.addItem(row, val)

            self.CMB_loyalityType.clear()
            records = util.FN_GET_CUSTTP()
            for row,val in records:
                self.CMB_loyalityType.addItem(row,val)

            records = util.FN_GET_CITIES()
            for row ,val in records:
                self.CMB_city.addItem(row,val)

            city=self.CMB_city.currentData()

            records = util.FN_GET_DISTRICT(city)
            for row ,val in records:
                self.CMB_district.addItem(row,val)

            self.CMB_city.currentIndexChanged.connect(self.FN_GET_DISTRICT)
            self.CMB_status.addItems(["Active", "Inactive"])


            self.BTN_createCustomer.clicked.connect(self.FN_CREATE_CUST)
            #
            self.setFixedWidth(1015)
            self.setFixedHeight(540)
        except Exception as err:
            print(err)

    def FN_GET_DISTRICT(self):
        self.CMB_district.clear()
        if self.CMB_city.currentData() != None:
            conn = db1.connect()
            mycursor = conn.cursor()
            sql = "SELECT DISTRICT_NAME ,DISTRICT_ID FROM Hyper1_Retail.DISTRICT where CITY_ID = %s and DISTRICT_STATUS = 1  order by DISTRICT_ID asc"
            val = (self.CMB_city.currentData(),)
            mycursor.execute(sql, val)
            records = mycursor.fetchall()

            for row, val in records:
                self.CMB_district.addItem(row, val)
            mycursor.close()

    def FN_CREATE_CUST(self):
        #get customer data
        try:

            print("here")
            self.parent.Qtable_customer.insertRow(0)
            self.name = self.LE_name.text().strip()
            self.custGroup = self.CMB_custGroup.currentData()
            self.loyalityType =self.CMB_loyalityType.currentData()
            self.phone = self.lE_phone .text().strip()
            self.mobile = self.lE_mobile.text().strip()
            self.job = self.LE_job.text().strip()
            self.address = self.LE_address.text().strip()
            self.city = self.CMB_city.currentData()
            self.district = self.CMB_district.currentData()
            self.building = self.LE_building.text().strip()
            self.floor = self.LE_floor.text().strip()
            self.email = self.LE_email.text().strip()
            self.company = self.LE_company.text().strip()
            self.workPhone =  self.LE_workPhone.text().strip()
            self.workAddress = self.LE_workAddress.text().strip()
            self.status = self.CMB_status.currentText()
            self.notes = self.LE_notes.toPlainText().strip()
            self.nationalID = self.LE_nationalID.text().strip()

            conn = db1.connect()
            mycursor = conn.cursor()

            creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

            self.status = self.CMB_status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0

            error =0
            error = self.FN_VALIDATE_FIELDS()

            if error !=1:
                sql0 = "  LOCK  TABLES    Hyper1_Retail.POS_CUSTOMER   WRITE "
                mycursor.execute(sql0)

                sql = "INSERT INTO Hyper1_Retail.POS_CUSTOMER( LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                      " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                      "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                      "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS,`POSC_NATIONAL_ID`) " \
                      "         VALUES (  %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                      "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s,%s)"

                           # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                val = (self.loyalityType,self.custGroup,self.name,self.phone,self.mobile,
                       self.job, self.address, self.city, self.district, self.building, self.floor ,self.email,
                       CL_userModule.user_name, creationDate, ' ',self.company, self.workPhone, self.workAddress,
                       self.notes, self.status,self.nationalID
                )
                mycursor.execute( sql, val )
                print( mycursor.rowcount, "record inserted." )
                #get max id
                mycursor.execute("SELECT max(POSC_CUST_ID ) FROM Hyper1_Retail.POS_CUSTOMER")
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
                print("in create cust" ,self.name)
                mycursor.close()
        except Exception as err:
            print(err)

    def FN_REFRESH_GRID(self,id):
        for i in reversed(range(self.parent.Qtable_customer.rowCount())):
            self.parent .Qtable_customer.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = %s"
        #print(sql_select_query)
        val = (id,)
        mycursor.execute(sql_select_query,val)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.parent.Qtable_customer.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 12:
                    data = util.FN_GET_STATUS_DESC(str(data))
                elif column_number == 2:
                    data = util.FN_GET_CUSTTP_DESC(str(data))
                elif column_number == 7:
                    data = util.FN_GET_CITY_DESC(str(data))

                elif column_number == 8:
                    data = util.FN_GET_DISTRICT_DESC(str(data))
                self.parent .Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.parent .Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        mycursor.close()
    def FN_VALIDATE_FIELDS(self):

        self.name = self.LE_name.text().strip()
        self.phone = self.lE_phone.text().strip()
        self.mobile = self.lE_mobile.text().strip()
        self.building = self.LE_building.text().strip()
        self.floor = self.LE_floor.text().strip()
        self.email = self.LE_email.text().strip()
        self.company = self.LE_company.text().strip()
        self.workPhone = self.LE_workPhone.text().strip()
        self.workAddress = self.LE_workAddress.text().strip()
        nationalID = self.LE_nationalID.text().strip()
        error = 0
        if self.name == '' or self.mobile == '' or self.job == ''  or self.building == '' \
                or self.floor == '' or self.email == '':
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
            error = 1
            return error
        ret = CL_validation.FN_validation_int(self.phone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم التليفون غير صحيح")
            error = 1

        ret = CL_validation.FN_validation_mobile(self.mobile)
        if ret == 3:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل يجب أن يكون 11 رقم")
            error = 1
        elif ret == 2:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم الموبايل يجب أن يبدأ ب 01")
            error = 1

        ret = self.FN_CHECK_REPEATED_MOBILE(self.mobile)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "موبايل مكرر ")
            error = 1
        ret = self.FN_CHECK_REPEATED_NATIONALID(nationalID)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم بطاقه مكرر ")
            error = 1
        ret = CL_validation.FN_validation_int(self.workPhone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم هاتف غير صحيح")
            error = 1
        ret = CL_validation.FN_validation_int(nationalID)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم البطاقه غير صحيح")
            error = 1
        ret = CL_validation.FN_validation_nationalID(nationalID)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم اليطاقه يجب أن يكون 14 رقم")
            error = 1
        ret = CL_validation.FN_valedation_mail(self.email)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ",  "إيميل غير صحسح")
            error = 1
        return error
    def FN_CHECK_REPEATED_MOBILE(self,mobile):
       try:
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max id
            mycursor.execute("SELECT POSC_MOBILE FROM Hyper1_Retail.POS_CUSTOMER where POSC_MOBILE ='"+mobile+"'")
            myresult = mycursor.fetchone()
            mycursor.close()
            if myresult[0] == None:
                return True
            else:
                return False

       except Exception as err:
             print(err)

    def FN_CHECK_REPEATED_NATIONALID(self, nationalID):
        try:
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max id
            mycursor.execute(
                "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_NATIONAL_ID ='" + nationalID + "'")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False

        except Exception as err:
            print(err)
class CL_CustService(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    def __init__(self):
        super(CL_CustService, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()


    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/customer_display.ui'
        loadUi(filename, self)
        conn = db1.connect()
        mycursor = conn.cursor()
        self.Qbtn_search.clicked.connect(self.FN_SEARCH_CUST)

        self.Rbtn_custNo.clicked.connect(self.onClicked)
        self.Rbtn_custName.clicked.connect(self.onClicked)
        self.Rbtn_custPhone.clicked.connect(self.onClicked)
        self.chk_search_other.stateChanged.connect(self.onClickedCheckBox)
        self.chk_search_status.stateChanged.connect(self.onClickedCheckBox)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(723)
        self.setFixedHeight(638)
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

    def FN_VALIDATE_CUST(self,id ):

            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            mycursor11.close()
            if mycursor11.rowcount > 0:
                return True
            else:
                return False



    def FN_MD_CUST(self):

        self.window_two = CL_CustService_modify(self)
        #get first selected row
        try:
            rowNo=self.Qtable_customer.selectedItems()[0].row()
            #if rowNo >0 :
            id =self.Qtable_customer.item(rowNo, 0).text()
            self.window_two.FN_LOAD_MODIFY(id)
            self.window_two.show()
        except Exception as err:
            print(err)
            #QtWidgets.QMessageBox.warning(self, "خطأ", "Please select the row you want to modify ")

    def onClickedCheckBox(self):
        if self.chk_search_other.isChecked():
            # self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custNo.setChecked(True)
            #self.Rbtn_custName.setChecked(True)
            self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custName.setEnabled(True)

            self.Rbtn_custPhone.setEnabled(True)
            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(True)
            self.LE_custPhone.setEnabled(True)

        else:
            self.Rbtn_custNo.setChecked(False)
            self.Rbtn_custName.setChecked(False)

            self.Rbtn_custPhone.setChecked(False)

            self.Rbtn_custNo.setEnabled(False)
            self.Rbtn_custTp.setEnabled(False)
            self.Rbtn_custPhone.setEnabled(False)
            self.LE_custNo.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setText('')


        if self.chk_search_status.isChecked():

            # self.LE_custNo.setEnabled(False)
            self.Rbtn_stsAll.setChecked(True)
            self.Rbtn_stsActive.setEnabled(True)
            self.Rbtn_stsInactive.setEnabled(True)
            self.Rbtn_stsAll.setEnabled(True)
        else:
            self.Rbtn_stsAll.setChecked(False)
            self.Rbtn_stsActive.setEnabled(False)
            self.Rbtn_stsInactive.setEnabled(False)
            self.Rbtn_stsAll.setEnabled(False)

    def onClicked(self):

        if self.Rbtn_custTp.isChecked():

            self.LE_custNo.setEnabled(False)
            self.LE_custName.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setEnabled(False)
        elif self.Rbtn_custNo.isChecked():

            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custPhone.setText('')
        elif self.Rbtn_custPhone.isChecked():

            self.LE_custNo.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custName.setEnabled(False)
            self.LE_custPhone.setEnabled(True)
        elif self.Rbtn_custName.isChecked():

            self.LE_custNo.setEnabled(False)
            self.LE_custName.setEnabled(True)
            self.LE_custPhone.setEnabled(False)
            self.LE_custPhone.setText('')
   #search for a customer
    def FN_SEARCH_CUST(self):
        for i in reversed(range(self.Qtable_customer.rowCount())):
            self.Qtable_customer.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        whereClause = " POSC_NAME not like '%cust%' "
        orderClause = " order by POSC_CUST_ID*1 asc"
        if self.chk_search_other.isChecked():
            if self.Rbtn_custNo.isChecked():
                id = self.LE_custNo.text()
                whereClause = whereClause + " and POSC_CUST_ID = '" + id + "'  "

            if  self.Rbtn_custName.isChecked():
                name = self.LE_custName.text()
                whereClause = whereClause +" and POSC_NAME like '%" + name + "%'  "

            elif self.Rbtn_custPhone.isChecked():
                phone = self.LE_custPhone.text()
                whereClause = whereClause + " and (POSC_PHONE = '" + phone + "' or POSC_MOBILE = '"+phone+"')  "

        if self.chk_search_status.isChecked():
            if self.Rbtn_stsActive.isChecked():
                whereClause = whereClause + 'and POSC_STATUS = 1'
            elif self.Rbtn_stsInactive.isChecked():
                whereClause = whereClause + ' and POSC_STATUS = 0'
            elif self.Rbtn_stsAll.isChecked():
                whereClause = whereClause + ' and POSC_STATUS in ( 0,1)'
        if self.chk_search_status.isChecked() == False and self.chk_search_other.isChecked() == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "أختر أي من محدادات  البحث")
        else:

            sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER where " + whereClause + orderClause

            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_customer.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    if column_number == 12:
                        data = util.FN_GET_STATUS_DESC(str(data))

                    elif column_number == 2:
                        data = util.FN_GET_CUSTTP_DESC(str(data))
                    elif column_number == 7:
                        data = util.FN_GET_CITY_DESC(str(data))

                    elif column_number == 8:
                        data = util.FN_GET_DISTRICT_DESC(str(data))
                    self.Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            mycursor.close()
        #self.Qbtn_search.setEnabled(True)

    def FN_SEARCH_CUST_ALL(self):
        #print('in search' +var)
        # self.Qtable_customer.clearcontents()
        #self.Qbtn_search.setEnabled(False)
        for i in reversed(range(self.Qtable_customer.rowCount())):
            self.Qtable_customer.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()

        orderClause = " order by POSC_CUST_ID*1 asc"
        sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER  " + orderClause
        # print(sql_select_query)
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_customer.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                if column_number == 12:
                    data = util.FN_GET_STATUS_DESC(str(data))

                elif column_number == 2:
                    data = util.FN_GET_CUSTTP_DESC(str(data))
                elif column_number == 7:
                    data = util.FN_GET_CITY_DESC(str(data))

                elif column_number == 8:
                    data = util.FN_GET_DISTRICT_DESC(str(data))
                self.Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        mycursor.close()
        #self.Qbtn_search.setEnabled(True)

