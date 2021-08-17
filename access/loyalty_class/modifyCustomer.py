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
    def __init__(self):
        super(CL_customer_modify, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()

    def FN_LOAD_MODIFY(self):
        try:

            filename = self.dirname + '/modifyCustomer.ui'
            loadUi(filename, self)
            records = util.FN_GET_CUSTTP()
            for row, val in records:
                self.CMB_loyalityType.addItem(row, val)

            records = util.FN_GET_CUSTGP()

            for row, val in records:
                self.CMB_custGroup.addItem(row, val)
            self.CMB_status.addItems(["Active", "Inactive"])
            #self.FN_GET_CUST(id)
            self.Qbtn_search.clicked.connect(self.FN_SEARCH_CUST)
            self.Rbtn_custNo.clicked.connect(self.onClicked)
            self.Rbtn_custName.clicked.connect(self.onClicked)

            self.CMB_city.currentIndexChanged.connect(self.FN_GET_DISTRICT)
            self.BTN_modifyCustomer.clicked.connect(self.FN_MODIFY_CUST)

            #self.setFixedWidth(1056)
            #self.setFixedHeight(540)

        except Exception as err:
            print(err)
    def onClicked(self):
        if self.Rbtn_custNo.isChecked():
            self.LE_custNo.setEnabled(True)
            self.LE_custName.setEnabled(False)
            self.LE_custName.setText('')
        elif self.Rbtn_custName.isChecked():

            self.LE_custNo.setEnabled(False)
            self.LE_custName.setEnabled(True)
            self.LE_custNo.setText('')

        # search for a customer
    def FN_SEARCH_CUST(self):

            whereClause = " POSC_NAME not like '%cust%' "

            if self.Rbtn_custNo.isChecked():
                id = self.LE_custNo.text()
                whereClause = whereClause + " and POSC_CUST_ID = '" + id + "'  "

            if self.Rbtn_custName.isChecked():
                name = self.LE_custName.text()
                whereClause = whereClause + " and POSC_NAME = '" + name + "'  "

            if self.Rbtn_custNo.isChecked() == False and self.Rbtn_custName.isChecked() == False:
                QtWidgets.QMessageBox.warning(self, "خطأ", "أختر أي من محدادات  البحث")
            else:
                if self.LE_custNo.text() == '' and self.LE_custName.text() == '':
                    QtWidgets.QMessageBox.warning(self, "خطأ", "أختر أي من محدادات  البحث")
                else:
                    conn = db1.connect()
                    mycursor = conn.cursor()
                    sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER where " + whereClause

                    mycursor.execute(sql_select_query)
                    records = mycursor.fetchone()
                    self.FN_GET_CUST(records[0])

                    mycursor.close()
            # self.Qbtn_search.setEnabled(True)

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
                #self.FN_REFRESH_GRID(self.id)
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
            self.LB_custID.setText(str(id))
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


