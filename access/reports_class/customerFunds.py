from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QDate
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
    field_names = ['رقم العمليه','نوع الإسترجاع','الشركه','الفرع','ماكينه الكاشير','رقم الفاتوره','تاريخ الفاتوره','نقاط العميل قبل','النقاط المكتسبه','تقاط العميل بعد','الحاله']
    def __init__(self):
        super(CL_customerFunds, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/reports_ui'
        conn = db1.connect()

    def FN_LOAD_DISPLAY(self):
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
            valid_from = str(datetime.today().strftime('%Y-%m-%d'))

            xto = valid_from.split("-")
            print(xto)
            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_from.setDate(d)

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
        try:
            self.FN_SEARCH()
            customer = self.Qline_cust.text().strip()
            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            if customer != '':
                ret = self.FN_CHECK_CUSTOMER(customer)
                if ret == True:
                    for i in reversed(range(self.Qtable_customer.rowCount())):
                        self.Qtable_customer.removeRow(i)
                    conn = db1.connect()
                    mycursor = conn.cursor()

                    self.sql = "SELECT MEMBERSHIP_POINTS_TRANS  'رقم العمليه',REDEEM_TYPE_ID 'نوع الإسترجاع',COMPANY_ID 'الشركه' ,BRANCH_NO  'الفرع',POS_NO 'ماكينه الكاشير',INVOICE_NO 'رقم الفاتوره' ,INVOICE_DATE 'تاريخ الفاتوره',  POSC_POINTS_BEFORE 'نقاط العميل قبل', TRANS_POINTS_QTY 'النقاط المكتسبه',POSC_POINTS_AFTER 'تقاط العميل بعد',TRANS_STATUS 'الحاله' FROM Hyper1_Retail.LOYALITY_POINTS_TRANSACTION_LOG  cp " \
                          " inner join Hyper1_Retail.POS_CUSTOMER  c " \
                          " on cp.POSC_CUST_ID = c.POSC_CUST_ID " \
                          " where c.POSC_CUST_ID = " + customer + " and TRANS_CREATED_ON >= '" + date_from + "' and TRANS_CREATED_ON <= '" + date_to + "' order by MEMBERSHIP_POINTS_TRANS*1 asc"
                    print(self.sql)
                    mycursor.execute(self.sql)
                    myresult = mycursor.fetchall()


                    for row_number, row_data in enumerate(myresult):
                        self.Qtable_customer.insertRow(row_number)

                        for column_number, data in enumerate(row_data):
                            if column_number == 1:
                                data = util.FN_GET_REDEEMTYPE_DESC(str(data))
                            elif column_number == 2:
                                data = util.FN_GET_COMP_DESC(str(data))
                            elif column_number == 3:
                                data = util.FN_GET_BRANCH_DESC(str(data))
                            elif column_number == 10:
                                data = self.FN_GET_TRANS_STATUS(str(data))
                            self.Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

                    mycursor.close()
                else:
                     QtWidgets.QMessageBox.warning(self, "خطأ", "رقم العميل غير صحيح")
            else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال رقم العميل")
        except Exception as err:
                print(err)

    def FN_GET_TRANS_STATUS(self,status):
        if status == '2':
            return "Completed"
        elif status== '0':
            return "Reversed"
        elif status == '1':
            return "Cancelled"
    def FN_SEARCH(self):
        try:
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
                    value = self.FN_GET_POINTS_VALUE(str(myresult[0]))
                    self.Qline_point_value.setText(str(value))
                else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "رقم العميل غير صحيح")
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال رقم العميل")
        except Exception as err:
            print(err)

    def FN_GET_POINTS_VALUE(self,points):
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT POINTS_QTY,POINTS_VALUE FROM Hyper1_Retail.LOYALITY_POINT where POINTS_VALID_FROM <= %s and POINTS_VALID_TO >= %s"
        currentDate =str(datetime.today().strftime('%Y-%m-%d'))
        x = (currentDate,currentDate,)
        mycursor.execute(sql_select_query,x)
        result = mycursor.fetchone()
        value = float(points) * int(result[1])  / int(result[0])
        #value = float(value)
        return value
    def printpreviewDialog(self):
        try:
            # Todo: method for export reports pdf file
            customer = self.Qline_cust.text().strip()
            points = self.Qline_points.text().strip()
            name = self.Qline_name.text().strip()
            pointValue = self.Qline_point_value.text().strip()
            title = Text()

            title.setFooter(
                " س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
            title.setFont('Scheherazade-Regular.ttf')
            title.setFontsize(10)
            title.setName("customer funds")
            #title.setcodeText("15235")
            title.setwaterText("hyperone company")
            #title.settelText("1266533")
            title.setbrachText("Entrance 1,EL Sheikh Zayed City")
            #title.setCursor("Testing")
            title.setQuery(self.sql)
            title.setCursor(self.field_names)
            data = [['customer no:' , ' ',customer ,'                                   ', 'customer name:' , ' ',name],

                    ['customer points:', ' ', points ,'                                   ', 'point value:', ' ', pointValue  ]
                    ]
            title.setData(data)
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