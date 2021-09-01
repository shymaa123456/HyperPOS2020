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

class CL_customerFunds(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    field_names = ['رقم العميل', 'اسم العميل', 'مجموعه العملاء', 'رقم الهاتف' , 'الموبيل' ,
                                    'الوطيفه' , 'العنوان' , 'المدينه' , 'المجاوره' ,
                                    'المبنى' , 'الطابق'  ,'الإيميل' , 'حاله العميل']
    def __init__(self):
        super(CL_customerFunds, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/reports_ui'
        conn = db1.connect()

    def FN_LOAD_DISPlAY(self):
        try:
            filename = self.dirname + '/customer_funds.ui'
            loadUi(filename, self)
            conn = db1.connect()
            mycursor = conn.cursor()
            self.Qbtn_search.clicked.connect(self.FN_SEARCH)

            self.Qline_cust.textChanged.connect(self.FN_CLEAR_FEILDS)
            self.Qbtn_search_details.clicked.connect(self.FN_SEARCH_DETAILS)
            self.Qbtn_print.clicked.connect(self.printpreviewDialog)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

        except Exception as err:
            print(err)

    def FN_CHECK_CUSTOMER(self, id):
        try:
            conn = db1.connect()
            mycursor = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = " + id
            mycursor.execute(sql)
            print("in check customer ")
            myresult = mycursor.fetchone()
            if mycursor.rowcount > 0:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False
        except Exception as err:
                print(err)

    def FN_SEARCH_DETAILS(self):
        print('details')
    def FN_SEARCH(self):
        try:
            print('in search')

            customer = self.Qline_cust.text().strip()
            if customer != '':
                ret = self.FN_CHECK_CUSTOMER(customer)
                if ret == True:
                    ##get customer points
                    conn = db1.connect()
                    mycursor = conn.cursor()
                    sql = "SELECT cp.POSC_POINTS_AFTER , c.POSC_NAME  FROM Hyper1_Retail.POS_CUSTOMER_POINT  cp " \
                          " inner join Hyper1_Retail.POS_CUSTOMER  c " \
                          " on cp.POSC_CUSTOMER_ID = c.POSC_CUST_ID " \
                          " where c.POSC_CUST_ID = " + customer
                    mycursor.execute(sql)
                    myresult = mycursor.fetchone()
                    self.Qline_points.setText(str(myresult[0]))
                    self.Qline_name.setText(str(myresult[1]))
                else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "رقم العميل غير صحيح")
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال رقم العميل")
        except Exception as err:
            print(err)
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


    def FN_CLEAR_FEILDS (self):
        self.Qline_points.setText("")
        self.Qline_name.setText('')
        self.Qline_point_value.setText("")