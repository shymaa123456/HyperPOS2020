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

class CL_customer_modify(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    oldmobile=''
    oldstatus=''
    oldemail=''
    def __init__(self,pp):
        super(CL_customer_modify, self).__init__()
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
class CL_customer_create(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    def __init__(self,pp):
        super(CL_customer_create, self).__init__()
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
            self.loyalityType =self.CMB_loyalityTypecurrentData()
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
class CL_customer(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    def __init__(self):
        super(CL_customer, self).__init__()
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
        self.Qbtn_search_all.clicked.connect(self.FN_SEARCH_CUST_ALL)
        self.Qbtn_export.clicked.connect(self.FN_SAVE_CUST)
        self.Rbtn_custNo.clicked.connect(self.onClicked)
        self.Rbtn_custName.clicked.connect(self.onClicked)
        self.Rbtn_custTp.clicked.connect(self.onClicked)

        self.Rbtn_custPhone.clicked.connect(self.onClicked)
        self.chk_search_other.stateChanged.connect(self.onClickedCheckBox)
        self.chk_search_status.stateChanged.connect(self.onClickedCheckBox)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(1028)
        self.setFixedHeight(560)
        #check authorization
        for row_number, row_data in enumerate( CL_userModule.myList ):
           if  row_data[1] =='Display_Customer':
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
                   elif result[0] == 'upload':
                         self.Qbtn_upload.setEnabled(True)
                         self.Qbtn_upload.clicked.connect(self.FN_UP_CUST)
        mycursor.close()

    def FN_CR_CUST(self):
        self.window_two2 = CL_customer_create(self)

        self.window_two2.FN_LOAD_CREATE()
        self.window_two2.show()




    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadCustomers.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
        self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD)
        self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP)
        self.fileName = ''

        self.setFixedWidth(576)
        self.setFixedHeight(178)
    def FN_LOAD_UPLOAD_PT(self):

        filename = self.dirname + '/uploadCustPt.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
        self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD1)
        self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP1)
        self.fileName = ''
        self.FN_GET_BRANCHES()
        self.FN_GET_REDEEMTPS()
        self.setFixedWidth(576)
        self.setFixedHeight(178)
    def FN_GET_BRANCHES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT BRANCH_DESC_A ,`BRANCH_NO`  FROM Hyper1_Retail.BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        self.CMB_branch.addItem('أختر الفرع', "")
        for row , val in records:
            for br in CL_userModule.branch :
                if str(val) in  br:
                    self.CMB_branch.addItem(row,val)
        mycursor.close

    def FN_GET_REDEEMTPS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_redeemType.addItem('أختر النوع', "")
        sql_select_query =    "SELECT REDEEMT_DESC,REDEEMT_TYPE_ID FROM Hyper1_Retail.REDEEM_TYPE where REDEEMT_STATUS = '1' order by REDEEMT_TYPE_ID*1   asc"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row , val in records:
            self.CMB_redeemType.addItem(row,val)
        mycursor.close
        return records

    def FN_DISPLAY_TEMP(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)

             wb = xlwt.Workbook()

             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'اسم العميل')
             sheet.write(0, 1, 'مجموعه العملاء')
             sheet.write(0, 2, 'نوع العضويه')
             sheet.write(0, 3, 'رقم الهاتف')
             sheet.write(0, 4, 'الموبايل')
             sheet.write(0, 5, 'الوظيفه')
             sheet.write(0, 6, 'العنوان')
             sheet.write(0, 7, 'المدينه')
             sheet.write(0, 8, 'المجاوره')
             sheet.write(0, 9, 'المبنى')

             sheet.write(0, 10, 'الطابق')
             sheet.write(0, 11, 'الإيميل')
             sheet.write(0, 12, 'الشركه')
             sheet.write(0, 13, 'تليفون الشركه')
             sheet.write(0, 14, 'عنوان الشركه')
             sheet.write(0, 15, 'الحاله')
             sheet.write(0, 16, 'ملاحظات')
             sheet.write(0, 17, 'رقم البطاقه')

             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)
# get customer type desc
    def FN_DISPLAY_TEMP1(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)

             wb = xlwt.Workbook()

             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'رقم العميل')
             sheet.write(0, 1, 'عدد النقاط')
             sheet.write(0, 2, 'السبب')
             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)

    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName( self, "QFileDialog.getOpenFileName()", "",
                                                   " Files (*.xlsx)", options=options )
        self.LE_fileName.setText(self.fileName)
        #print(self.fileName)
    def FN_SAVE_UPLOAD(self):

        if self.fileName !='':
            self.LE_fileName.setText(self.fileName)
            wb = xlrd.open_workbook( self.fileName )
            sheet = wb.sheet_by_index( 0 )
            conn = db1.connect()
            mycursor = conn.cursor()
            errorMsg =''
            createdCust =0
            nonCreatedCust=0
            #print (sheet.nrows)
            error_message = ''
            for i in range( sheet.nrows ):
                error = 0
                try:

                    self.name = sheet.cell_value( i, 0 )
                    error_message = error_message + " \n username " + self.name
                    self.custGroup = int(sheet.cell_value( i, 1 ))
                    self.loyalityType = int(sheet.cell_value( i, 2 ))
                    self.phone = int(sheet.cell_value( i, 3))
                    self.mobile = sheet.cell_value( i, 4)
                    self.job = sheet.cell_value( i, 5)
                    self.address = sheet.cell_value( i, 6)
                    self.city = int(sheet.cell_value( i, 7 ))
                    self.district = int(sheet.cell_value( i, 8 ))
                    self.building = int(sheet.cell_value( i, 9 ))
                    self.floor = int(sheet.cell_value( i, 10 ))
                    self.email = sheet.cell_value( i, 11 )
                    self.company = sheet.cell_value( i, 12 )
                    self.workPhone = int(sheet.cell_value( i, 13 ))
                    self.workAddress = sheet.cell_value( i, 14 )
                    self.status = int (sheet.cell_value( i, 15 ) )
                    self.notes = sheet.cell_value( i, 16 )
                    nationalID = sheet.cell_value(i, 17)
                    #QtWidgets.QMessageBox.warning(self, "خطأ", "Please select the row you want to modify ")
                    if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.city == '' or self.district == '' or self.building == '' \
                            or self.email == '' or nationalID =='':

                        error = 1
                        error_message= error_message + " user has an empty fields"

                    ret = CL_validation.FN_validation_mobile(str(self.mobile))
                    if ret == 3:

                        error_message = error_message + "رقم الموبايل يجب أن يكون 11 رقم"

                        error = 1
                    elif ret == 2:
                        error_message = error_message + " رقم الموبايل يجب أن يبدأ ب 01"

                        error = 1

                    ret = CL_validation.FN_validation_int(str(self.phone))
                    if ret == False:
                        error_message = error_message + " , صحيح غير الهاتف رقم "

                        error = 1
                    ret = CL_validation.FN_validation_int(nationalID)
                    if ret == False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "رقم البطاقه غير صحيح")
                        error = 1
                    ret = CL_validation.FN_valedation_mail(self.email)
                    if ret == False:
                        error_message = error_message +  "  إيميل غير صحسح"
                        error = 1

                    if error != 1:
                        sql0 = "  LOCK  TABLES    Hyper1_Retail.POS_CUSTOMER   WRITE "
                        mycursor.execute(sql0)

                        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
                        sql = "INSERT INTO Hyper1_Retail.POS_CUSTOMER( LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                              " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                              "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                              "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS,`POSC_NATIONAL_ID`) " \
                              "         VALUES (%s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                              "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s,%s)"

                        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                        val = ( self.loyalityType, self.custGroup, self.name, str(self.phone), self.mobile,
                               self.job, self.address, str(self.city), str(self.district), str(self.building), self.floor, self.email,
                               CL_userModule.user_name, creationDate, ' ', self.company, self.workPhone, self.workAddress,
                               self.notes, self.status,nationalID
                               )
                        #print(val)
                        mycursor.execute( sql, val )
                        createdCust=createdCust+1
                        sql00 = "  UNLOCK   tables    "
                        mycursor.execute(sql00)

                        db1.connectionCommit( conn )
                    else:
                        nonCreatedCust = nonCreatedCust + 1
                    #     self.msgBox1.setText(error_message)
                    #     self.msgBox1.show()

                except Exception as err:
                     print(err)
            mycursor.close()
            self.msgBox = QMessageBox()

            # Set the various texts
            self.msgBox.setWindowTitle( "Information" )
            self.msgBox.setStandardButtons( QMessageBox.Ok)
            self.msgBox.setText(error_message+ "\n No of created Cust '"+str(createdCust) +"'  No of non created Cust '"+str(nonCreatedCust)+"'")
            self.msgBox.show()
            self.close()
        #Extracting number of rows
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار الملف")
    def FN_VALIDATE_CUST(self,id ):

            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()

            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False

    def FN_SAVE_UPLOAD1(self):
        if len (self.CMB_branch.currentData())<=0 or len (self.CMB_redeemType.currentData()) <= 0:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يجب إختيار الفرع و نوع الإسترجاع ")
        elif self.fileName !='':
            self.LE_fileName.setText(self.fileName)
            wb = xlrd.open_workbook( self.fileName )
            sheet = wb.sheet_by_index( 0 )
            conn = db1.connect()
            mycursor = conn.cursor()
            error = 0
            error1 = 0
            for i in range(sheet.nrows):
                try:
                    cust = sheet.cell_value(i, 0)
                    pts = sheet.cell_value(i, 1)

                    cust = int(cust)
                    ret = self.FN_VALIDATE_CUST(cust)
                    if cust == '' or pts == '':
                        error = 1
                        break
                    if ret == False:
                        error1 = 1
                        break
                except Exception as err:
                     print(err)

            if error == 0 and error1 ==0 :
                # lock tables
                sql0 = "  LOCK  TABLES    Hyper1_Retail.POS_CUSTOMER_POINT   WRITE , " \
                       "    Hyper1_Retail.LOYALITY_POINTS_TRANSACTION_LOG   WRITE  "

                mycursor.execute(sql0)
                for i in range( sheet.nrows ):

                    try:
                        cust = sheet.cell_value( i, 0 )
                        pts = sheet.cell_value(i, 1)

                        reason     = sheet.cell_value(i, 2)
                        #branch = sheet.cell_value(i, 3)
                        cust = int(cust)
                        pts = int(pts)
                        sql = "select POSC_POINTS_AFTER from Hyper1_Retail.POS_CUSTOMER_POINT where POSC_CUSTOMER_ID = '"+str(cust)+"'"
                        mycursor.execute(sql)
                        result = mycursor.fetchone()
                        before_points = int(result[0])
                        after_points = before_points+pts
                        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

                        sql= "INSERT INTO `Hyper1_Retail`.`LOYALITY_POINTS_TRANSACTION_LOG` " \
                             "(`POSC_CUST_ID`,`REDEEM_TYPE_ID`,`COMPANY_ID`,`BRANCH_NO`,`TRANS_CREATED_BY`," \
                             "`TRANS_CREATED_ON`,`POSC_POINTS_BEFORE`,`VALUE_OF_POINTS`,`TRANS_POINTS_QTY`,`TRANS_POINTS_VALUE`,`TRANS_REASON`,`POSC_POINTS_AFTER`,`TRANS_STATUS`)" \
                             "                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                        val=(cust,self.CMB_redeemType.currentData(),'1',self.CMB_branch.currentData(),CL_userModule.user_name,creationDate,before_points,1,pts,1,reason,after_points,'2')
                        mycursor.execute(sql, val)
                        db1.connectionCommit(conn)
                        mycursor.execute("SELECT max(cast(`MEMBERSHIP_POINTS_TRANS`  AS UNSIGNED)) FROM LOYALITY_POINTS_TRANSACTION_LOG")
                        myresult = mycursor.fetchone()
                        MEMBERSHIP_POINTS_TRANS = myresult[0]
                        sql = "update Hyper1_Retail.POS_CUSTOMER_POINT set POSC_POINTS_BEFORE =%s ,POSC_POINTS_AFTER=%s , POINTS_CHANGED_ON =%s , TRANS_SIGN = '0'" \
                              ",MEMBERSHIP_POINTS_TRANS = %s , TRANS_POINTS = %s where POSC_CUSTOMER_ID = %s"
                        val = (before_points, after_points, creationDate,MEMBERSHIP_POINTS_TRANS, pts,str(cust))
                        mycursor.execute(sql, val)
                        db1.connectionCommit(conn)
                    except Exception as err:
                         print(err)

                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                db1.connectionCommit(conn)
                QtWidgets.QMessageBox.information(self, "تم", "تم رفع نقاط العملاء")
            elif error == 1:
                QtWidgets.QMessageBox.warning(self, "خطأ", "الملف يحتوي على بعض الخانات الفارغه")
            elif error1 == 1:
                QtWidgets.QMessageBox.warning(self, "خطأ", "الملف يحتوي على عملاء غير متواجدين")

            mycursor.close()
#            self.close()
        #Extracting number of rows
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار الملف")

    def FN_MD_CUST(self):

        self.window_two = CL_customer_modify(self)
        #get first selected row
        try:
            if len(self.Qtable_customer.selectedIndexes()) > 0:
                rowNo=self.Qtable_customer.selectedItems()[0].row()
                #if rowNo >0 :
                id =self.Qtable_customer.item(rowNo, 0).text()
                self.window_two.FN_LOAD_MODIFY(id)
                self.window_two.show()
            else:
                 QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

        except Exception as err:
            print(err)
            #QtWidgets.QMessageBox.warning(self, "خطأ", "Please select the row you want to modify ")

    def FN_UP_CUST(self, funct):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_UPLOAD()
        self.window_two.show()


    # return customer tye id
    def FN_GET_CUSTTP_ID(self,desc):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+desc+"'" )
        records = mycursor.fetchone()
        mycursor.close()
        return records[0]

    def onClickedCheckBox(self):
        if self.chk_search_other.isChecked():
            # self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custNo.setChecked(True)
            #self.Rbtn_custName.setChecked(True)
            self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custName.setEnabled(True)
            self.Rbtn_custTp.setEnabled(True)
            self.Rbtn_custPhone.setEnabled(True)
            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(True)
            self.LE_custPhone.setEnabled(True)
            self.CMB_loyalityType.setEnabled(True)
        else:
            self.Rbtn_custNo.setChecked(False)
            self.Rbtn_custName.setChecked(False)
            self.Rbtn_custTp.setChecked(False)
            self.Rbtn_custPhone.setChecked(False)

            self.Rbtn_custNo.setEnabled(False)
            self.Rbtn_custTp.setEnabled(False)
            self.Rbtn_custPhone.setEnabled(False)
            self.LE_custNo.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setText('')
            self.CMB_loyalityType.setEnabled(False)

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
            records = util.FN_GET_CUSTTP()
            for row in records:
                self.CMB_loyalityType.addItems([row[0]])

            self.CMB_loyalityType.setEnabled(True)
            self.LE_custNo.setEnabled(False)
            self.LE_custName.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setEnabled(False)
        elif self.Rbtn_custNo.isChecked():
            self.CMB_loyalityType.setEnabled(False)
            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custPhone.setText('')
        elif self.Rbtn_custPhone.isChecked():
            self.CMB_loyalityType.setEnabled(False)
            self.LE_custNo.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custName.setEnabled(False)
            self.LE_custPhone.setEnabled(True)
        elif self.Rbtn_custName.isChecked():
            self.CMB_loyalityType.setEnabled(False)
            self.LE_custNo.setEnabled(False)
            self.LE_custName.setEnabled(True)
            self.LE_custPhone.setEnabled(False)
            self.LE_custPhone.setText('')
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

        error = 0
        if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.building == '' \
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
            QtWidgets.QMessageBox.warning(self, "خطأ"," رقم الموبايل يجب أن يبدأ ب  01")
            error = 1

        ret = self.FN_CHECK_REPEATED_MOBILE(self.mobile)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "موبايل مكرر ")
            error = 1

        ret = CL_validation.FN_validation_int(self.workPhone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "خطأ", "رقم هاتف غير صحيح")
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




# export to a file

    def FN_SAVE_CUST(self):
        try:
            filename = QFileDialog.getSaveFileName(self, "Save File", '', "(*.xls)")
            print(filename)

            wb = xlwt.Workbook()

            # add_sheet is used to create sheet.
            sheet = wb.add_sheet('Sheet 1')
            sheet.write(0, 0, 'رقم العميل')
            sheet.write(0, 1, 'اسم العميل')
            sheet.write(0, 2, 'نوع العضويه')
            sheet.write(0, 3, 'رقم الهاتف')
            sheet.write(0, 4, 'الموبايل')
            sheet.write(0, 5, 'الوظيفه')
            sheet.write(0, 6, 'العنوان')
            sheet.write(0, 7, 'المدينه')
            sheet.write(0, 8, 'المجاوره')
            sheet.write(0, 9, 'المبنى')

            sheet.write(0, 10, 'الطابق')
            sheet.write(0, 11, 'الإيميل')
            sheet.write(0, 12, 'حاله العميل')

            rowNo= self.Qtable_customer.rowCount()+1

            for currentColumn in range(self.Qtable_customer.columnCount()):
                for currentRow in range(self.Qtable_customer.rowCount()):
                    teext = str(self.Qtable_customer.item(currentRow, currentColumn).text())
                    sheet.write(currentRow+1, currentColumn, teext)
            # # wb.save('test11.xls')
            wb.save(str(filename[0]))
            # wb.close()
            import webbrowser
            webbrowser.open(filename[0])
        except Exception as err:
            print(err)

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

            elif self.Rbtn_custTp.isChecked():
                type = self.CMB_loyalityType.currentText()
                whereClause = whereClause + " and LOYCT_TYPE_ID ='" + self.FN_GET_CUSTTP_ID(type) + "'  "

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

