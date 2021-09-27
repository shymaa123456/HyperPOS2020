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
from access.Checkable import CheckableComboBox
class CL_redeemTypeValue(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    whereClause1= ''
    field_names = ['رقم العمليه', 'رقم العميل','اسم العميل','نوع الإسترجاع','الشركه','الفرع','ماكينه الكاشير','رقم الفاتوره','تاريخ الفاتوره','نقاط العميل قبل','النقاط المكتسبه','تقاط العميل بعد','الحاله']
    def __init__(self):
        super(CL_redeemTypeValue, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/reports_ui'

    def FN_LOAD_DISPLAY(self):
        try:
            filename = self.dirname + '/redeemTypeValue.ui'
            loadUi(filename, self)

            self.Qbtn_search.clicked.connect(self.FN_SEARCH)

            #self.Qline_cust.textChanged.connect(self.FN_CLEAR_FEILDS)
            self.Qbtn_search_details.clicked.connect(self.FN_SEARCH_DETAILS)
            self.Qbtn_print.clicked.connect(self.printpreviewDialog)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())
            valid_from = str(datetime.today().strftime('%Y-%m-%d'))

            xto = valid_from.split("-")

            d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
            self.Qdate_from.setDate(d)

            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(490, 42, 179, 18)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_branch = CheckableComboBox(self)
            self.Qcombo_branch.setGeometry(490, 95, 179, 18)
            self.Qcombo_branch.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.FN_GET_COMPANIES()
            self.Qcombo_company.model().dataChanged.connect(self.FN_GET_Branch)

            self.FN_GET_Branch()
            self.FN_GET_REDEEMTPS()
        except Exception as err:
            print(err)
    def FN_GET_REDEEMTPS(self):
        self.conn = db1.connect()
        try:


            mycursor = self.conn.cursor()
            mycursor.execute("SELECT REDEEMT_DESC ,REDEEMT_TYPE_ID FROM Hyper1_Retail.REDEEM_TYPE  ")
            records = mycursor.fetchall()
            for row, val in records:
                self.CMB_redeemType.addItem(row, val)
        except Exception as err:
            print(err)

    def FN_GET_Branch(self):
        self.Qcombo_branch.clear()
        i = 0
        try:
            # Todo: method for fills the Branch combobox
            self.conn = db1.connect()
            mycursor = self.conn.cursor()

            val3 = ""
            for a in range(len(self.Qcombo_company.currentData())):
                if a < len(self.Qcombo_company.currentData()) - 1:
                    val3 = val3 + "'" + self.Qcombo_company.currentData()[a] + "',"
                else:
                    val3 = val3 + "'" + self.Qcombo_company.currentData()[a] + "'"


            sqlite3 = "SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH WHERE COMPANY_ID in (" + val3 + ")"



            mycursor.execute(sqlite3)

            records = mycursor.fetchall()
            for row, val in records:
                for bra in CL_userModule.branch:
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1
            mycursor.close()
            self.Qcombo_branch.setCurrentIndex(-1)
        except Exception as err:
            print(err)

    def FN_GET_COMPANIES(self):
        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
            records = mycursor.fetchall()
            print(records)
            for row, val in records:
                self.Qcombo_company.addItem(row, val)
            mycursor.close()

        except Exception as err:
            print(err)

    def FN_SEARCH_DETAILS(self):
        try:
                    self.FN_SEARCH()
                    for i in reversed(range(self.Qtable_customer.rowCount())):
                        self.Qtable_customer.removeRow(i)
                    conn = db1.connect()
                    mycursor = conn.cursor()

                    self.sql = "SELECT MEMBERSHIP_POINTS_TRANS  'رقم العمليه',cp.POSC_CUST_ID 'رقم العميل', c.POSC_NAME 'اسم العميل',REDEEM_TYPE_ID 'نوع الإسترجاع',COMPANY_ID 'الشركه' ,BRANCH_NO  'الفرع',POS_NO 'ماكينه الكاشير',INVOICE_NO 'رقم الفاتوره' ,INVOICE_DATE 'تاريخ الفاتوره',  POSC_POINTS_BEFORE 'نقاط العميل قبل', TRANS_POINTS_QTY 'النقاط المكتسبه',POSC_POINTS_AFTER 'تقاط العميل بعد',TRANS_STATUS 'الحاله' FROM Hyper1_Retail.LOYALITY_POINTS_TRANSACTION_LOG  cp " \
                          " left outer join Hyper1_Retail.POS_CUSTOMER  c " \
                          " on cp.POSC_CUST_ID = c.POSC_CUST_ID  where " + self.whereClause1

                    mycursor.execute(self.sql)
                    print(self.sql)
                    myresult = mycursor.fetchall()


                    for row_number, row_data in enumerate(myresult):
                        self.Qtable_customer.insertRow(row_number)

                        for column_number, data in enumerate(row_data):
                            if column_number == 3:
                                data = util.FN_GET_REDEEMTYPE_DESC(str(data))
                            elif column_number == 4:
                                data = util.FN_GET_COMP_DESC(str(data))
                            elif column_number == 5:
                                data = util.FN_GET_BRANCH_DESC(str(data))
                            elif column_number == 12:
                                data = self.FN_GET_TRANS_STATUS(str(data))
                            self.Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

                    mycursor.close()

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
            self.FN_CLEAR_FEILDS()
            branchs = self.Qcombo_branch.currentData()
            companies = self.Qcombo_company.currentData()
            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            redeem_type = self.CMB_redeemType.currentData()
            conn = db1.connect()
            mycursor = conn.cursor()
            whereClause = ""
            whereClause = whereClause + " `TRANS_CREATED_ON` >= '" + date_from + "' and `TRANS_CREATED_ON` <= '" + date_to + "' "
            whereClause = whereClause + " and REDEEM_TYPE_ID = '" +redeem_type+"'"

            company_list = companies
            if len(company_list) > 0:
                if len(company_list) == 1:
                    whereClause = whereClause + " and `COMPANY_ID` = '" + company_list[0] + "'"
                else:
                    company_list_tuple = tuple(company_list)
                    whereClause = whereClause + " and `COMPANY_ID` in {}".format(company_list_tuple)
                    # get branchs
            branch_list = branchs

            if len(branch_list) > 0:
                if len(branch_list) == 1:
                    whereClause = whereClause + " and BRANCH_NO ='" + branch_list[0] + "'"
                else:
                    branch_list_tuple = tuple(branch_list)
                    whereClause = whereClause + " and BRANCH_NO in {} ".format(branch_list_tuple)
            sql_select_query = "SELECT sum( TRANS_POINTS_QTY) ,sum(`TRANS_POINTS_VALUE`)  FROM Hyper1_Retail.LOYALITY_POINTS_TRANSACTION_LOG    where " + whereClause + " group by  REDEEM_TYPE_ID"
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()

            if len(records) >0:
                self.Qline_points.setText(str (records[0][0]))
                self.Qline_point_value.setText(str (records[0][1]))
            mycursor.close()
            self.whereClause1 = whereClause
        except Exception as err:
            print(err)

    def printpreviewDialog(self):
        try:
            # Todo: method for export reports pdf file

            points = self.Qline_points.text().strip()
            pointValue = self.Qline_point_value.text().strip()
            redeem_type = self.CMB_redeemType.currentText()
            title = Text()

            title.setFooter(
                " س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
            title.setFont('Scheherazade-Regular.ttf')
            title.setFontsize(10)
            title.setName("Redeem Type values")
            #title.setcodeText("15235")
            title.setwaterText("hyperone company")
            #title.settelText("1266533")
            title.setbrachText("Entrance 1,EL Sheikh Zayed City")
            #title.setCursor("Testing")
            title.setQuery(self.sql)
            title.setCursor(self.field_names)
            data = [['Redeem Type:' , ' ',redeem_type ],
                    ['No of points ' , ' ',points ,'                                   ', 'Point value:' , ' ',pointValue],]
            title.setData(data)
            body()
            QtWidgets.QMessageBox.information(self, "Success", "Report is printed successfully")
            import os
            os.system('my_file.pdf')

        except Exception as err:
             print(err)


    def FN_CLEAR_FEILDS (self):
        self.Qline_points.setText("")
        self.Qline_point_value.setText("")