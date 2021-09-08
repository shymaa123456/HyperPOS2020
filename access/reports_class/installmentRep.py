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

class CL_installmentReport(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''

    field_names = ['رقم العمليه','نوع الإسترجاع','الشركه','الفرع','ماكينه الكاشير','رقم الفاتوره','تاريخ الفاتوره','نقاط العميل قبل','النقاط المكتسبه','تقاط العميل بعد','الحاله']
    def __init__(self):
        super(CL_installmentReport, self).__init__()
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


            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())


        except Exception as err:
            print(err)


    def FN_SEARCH(self):
        try:
           print('in search')
        except Exception as err:
            print(err)

