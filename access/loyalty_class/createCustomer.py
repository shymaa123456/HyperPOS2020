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


class CL_customer_create(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    def __init__(self):
        super(CL_customer_create, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()

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
            # self.setFixedWidth(1015)
            # self.setFixedHeight(540)

            # Set Style
            # self.voucher_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

            # Set Style
            # self.voucher_num.setStyleSheet(label_num)
            # self.label_2.setStyleSheet(desc_5)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
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
            #self.parent.Qtable_customer.insertRow(0)
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
                #self.FN_REFRESH_GRID(id)
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


