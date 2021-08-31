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
from access.reports_class.ReportPDF import body, Text

class CL_customer_report(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    field_names = ['رقم العميل', 'اسم العميل', 'مجموعه العملاء', 'رقم الهاتف' , 'الموبيل' ,
                                    'الوطيفه' , 'العنوان' , 'المدينه' , 'المجاوره' ,
                                    'المبنى' , 'الطابق'  ,'الإيميل' , 'حاله العميل']
    def __init__(self):
        super(CL_customer_report, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/reports_ui'
        conn = db1.connect()


    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/customer_display.ui'
        loadUi(filename, self)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        conn = db1.connect()
        mycursor = conn.cursor()
        self.Qbtn_search.clicked.connect(self.FN_SEARCH_CUST)
        self.Qbtn_search_all.clicked.connect(self.FN_SEARCH_CUST_ALL)
        self.Qbtn_export.clicked.connect(self.FN_SAVE_CUST)
        self.Qbtn_print.clicked.connect(self.printpreviewDialog)

        self.Rbtn_custNo.clicked.connect(self.onClicked)
        self.Rbtn_custName.clicked.connect(self.onClicked)
        self.Rbtn_custTp.clicked.connect(self.onClicked)

        self.Rbtn_custPhone.clicked.connect(self.onClicked)
        self.chk_search_other.stateChanged.connect(self.onClickedCheckBox)
        self.chk_search_status.stateChanged.connect(self.onClickedCheckBox)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        mycursor.close()


    # def FN_VALIDATE_CUST(self,id ):
    #
    #         conn = db1.connect()
    #         mycursor11 = conn.cursor()
    #         sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
    #         #print(sql)
    #         mycursor11.execute(sql)
    #         myresult = mycursor11.fetchone()
    #
    #         if mycursor11.rowcount > 0:
    #             mycursor11.close()
    #             return True
    #         else:
    #             mycursor11.close()
    #             return False
    # # return customer tye id
    def printpreviewDialog(self):
        try:
            # Todo: method for export reports pdf file

            title = Text()
            title.setName("customers")
            title.setFooter(
                " س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
            title.setFont('Scheherazade-Regular.ttf')
            title.setFontsize(10)
            #title.setcodeText("15235")
            title.setwaterText("hyperone company")
            #title.settelText("1266533")
            title.setbrachText("Entrance 1,EL Sheikh Zayed City")
            #title.setCursor("Testing")
            title.setQuery(self.sql_select_query)
            title.setCursor(self.field_names)
            body()
            QtWidgets.QMessageBox.information(self, "Success", "Report is printed successfully")
            import os
            os.system('my_file.pdf')

        except Exception as err:
             print(err)
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
                    if teext !=  None:
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
        orderClause = " order by POSC_CUST_ID*1 asc "
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

            self.sql_select_query = "select POSC_CUST_ID 'رقم العميل',POSC_NAME 'اسم العميل',LOYCT_TYPE_ID  'مجموعه العملاء',POSC_PHONE  'رقم الهاتف', POSC_MOBILE 'الموبيل',POSC_JOB  'الوطيفه' ,    POSC_ADDRESS 'العنوان',POSC_CITY 'المدينه' " \
                                    ",POSC_DISTICT 'المجاوره',POSC_BUILDING  'المبنى',POSC_FLOOR 'الطابق',POSC_EMAIL 'الإيميل',POSC_STATUS 'حاله العميل'    from Hyper1_Retail.POS_CUSTOMER where " + whereClause + orderClause

            mycursor.execute(self.sql_select_query)
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
        try:
            for i in reversed(range(self.Qtable_customer.rowCount())):
                self.Qtable_customer.removeRow(i)
            conn = db1.connect()
            mycursor = conn.cursor()

            orderClause = " order by POSC_CUST_ID*1 asc"
            self.sql_select_query = "select POSC_CUST_ID 'رقم العميل',POSC_NAME 'اسم العميل',LOYCT_TYPE_ID  'مجموعه العملاء',POSC_PHONE  'رقم الهاتف', POSC_MOBILE 'الموبيل',POSC_JOB  'الوطيفه' ,    POSC_ADDRESS 'العنوان',POSC_CITY 'المدينه' " \
                                    ",POSC_DISTICT 'المجاوره',POSC_BUILDING  'المبنى',POSC_FLOOR 'الطابق',POSC_EMAIL 'الإيميل',POSC_STATUS 'حاله العميل' from Hyper1_Retail.POS_CUSTOMER  " + orderClause
            # print(sql_select_query)
            mycursor.execute(self.sql_select_query)
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
        except Exception as err:
            print(err)
        #self.Qbtn_search.setEnabled(True)

