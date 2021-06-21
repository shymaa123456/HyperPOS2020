#!/usr/bin/env python3
# -*     - coding: utf-8 -*-
"""
Created on Mon Jun 29 19:52:06 2020

@author: hossam
"""

#####
import os

import pandas as pd
from PyQt5.QtGui import QStandardItemModel
from PyQt5.uic import loadUi

from access.authorization_class.user_module import CL_userModule
from access.promotion_class.Promotion_Add import CheckableComboBox
from access.reports_class.ReportPDF import body, Text
from pathlib import Path

from PyQt5 import QtCore, QtGui, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from data_connection.h1pos import db1
import sys



class CL_report1(QtWidgets.QDialog):
    model = QStandardItemModel()

    switch_window = QtCore.pyqtSignal()
    cond = 1
    query = ""
    company_list = []
    branch_list = []
    conn = db1.connect()

    prom_status = ""
    prom_CG = ""
    sponsor_prom = ""
    multi = ""
    copNum = ""
    list_num = []
    field_names = []

    def FN_close(self):
        #Todo: method for close window

        self.close()



    def FN_loadData(self, PROM_ID):
        #Todo: method for searching about promotions in data base

        self.company_list.clear()
        self.branch_list.clear()

        if len(self.Qcombo_company.currentData()) > 0:
            for i in self.Qcombo_company.currentData():
                self.company_list.append("'" + i + "'")
        else:
            self.company_list.append("'" "'")

        if len(self.Qcombo_branchEdition.currentData()) > 0:
            for i in self.Qcombo_branchEdition.currentData():
                self.branch_list.append("'" + i + "'")


        try:
            self.company_list.clear()
            self.branch_list.clear()

            if len(self.Qcombo_company.currentData()) > 0 and len(self.Qcombo_branchEdition.currentData()) > 0:
                for i in self.Qcombo_company.currentData():
                    self.company_list.append("'" + i + "'")
                for i in self.Qcombo_branchEdition.currentData():
                    self.branch_list.append("'" + i + "'")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "برجاء تحديد محددات البحث")
                self.company_list.append("'" "'")
                self.branch_list.append("'" "'")


            if self.QcheckBox_multi.isChecked():
                    self.multi = "AND COP_MULTI_USE = 1 "
            else:
                self.multi = ""

            if len(self.Qline_promotion.text()) > 0:
                self.copNum = "Cop_ID = '" + self.Qline_promotion.text() + "' AND "
            else:
                self.copNum = ""



            self.Qtable_promotion.setRowCount(0)
            self.conn = db1.connect()

            mycursor = self.conn.cursor()
            query = ""
            if self.cond == 1:
                self.Qbtn_search.setEnabled(False)
                self.query = (
                        "SELECT COP_ID رقم_الكوبون, COP_DESC وصف_الكوبون, BRANCH_DESC_A اسم_الشركة, "
                        "COP_DISCOUNT_VAL قيمة_الخصم, COP_DISCOUNT_PERCENT نسبة_الخصم, "
                        "COP_SERIAL_COUNT عدد_السريال, COP_MULTI_USE متعدد_الاستخدام, COP_MULTI_USE_COUNT "
                        "عدد_الاستخدامات_المتاحة, COP_CREAED_ON تاريخ_الانشاء, COP_CHANGED_ON تاريخ_التغيير, "
                        "COP_VALID_FROM متاح_من, COP_VALID_TO متاح_الي, COP_STATUS الحالة FROM COUPON "
                        "join COUPON_BRANCH on COP_ID = COUPON_ID "
                        "join BRANCH on COUPON_BRANCH.BRANCH_NO = BRANCH.BRANCH_NO "
                        "WHERE " + self.copNum + self.prom_status+" COP_VALID_FROM >= '" + self.Qdate_from.dateTime().toString(
                    'yyyy-MM-dd') + "' and COP_VALID_TO<='"
                        + self.Qdate_to.dateTime().toString(
                    'yyyy-MM-dd') + "'") + self.multi + "AND BRANCH.COMPANY_ID IN (" + ','.join(self.company_list) + ") " \
                    "and BRANCH.BRANCH_NO IN (" + ','.join(self.branch_list) + ")"

                self.runQuery(mycursor)
                self.Qbtn_search.setEnabled(True)
                self.field_names = ['رقم_الكوبون', 'وصف_الكوبون', 'اسم_الشركة', 'قيمة_الخصم' , 'نسبة_الخصم' ,
                                    'عدد_السريال' , 'متعدد_الاستخدام' , 'عدد_الاستخدامات_المتاحة' , 'متاح_من' ,
                                    'متاح_الي' , 'الحالة']

            elif self.cond == 0:
                QtWidgets.QMessageBox.warning(self, "Error", "برجاء تحديد محددات البحث")
                mycursor.close()

            self.disable()
        except:
            print(sys.exc_info())

    def runQuery(self,mycursor):
        print(self.query)
        mycursor.execute(self.query)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.Qtable_promotion.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Qtable_promotion.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        mycursor.close()
    def FN_GET_Company(self):
        #Todo: method for fills the company combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    def FN_GET_Branch(self):
        #Todo: method for fills the Branch combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH")
        records = mycursor.fetchall()
        for row ,val in records:
            for bra in CL_userModule.branch:
                if val in bra:
                  self.Qcombo_branchEdition.addItem(row,val)
        mycursor.close()






    def FN_Check_Active(self):
        #Todo: method for change status to active

        self.disable()
        self.prom_status = "COP_STATUS = '1' AND "


    def FN_Check_Expired(self):
        #Todo: method for change status to Expired

        self.disable()
        self.prom_status = "COP_STATUS = '0' AND "


    def FN_Check_All(self):
        #Todo: method for change status to Expired

        self.disable()
        self.prom_status = ""


    def handleSave(self):
        #Todo: method for export reports excel file

        frame = pd.read_sql(str(self.query), self.conn)
        df = pd.DataFrame(frame,
                          columns=self.field_names)

        # Dump Pandas DataFrame to Excel sheet
        writer = pd.ExcelWriter('myreport.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', startrow=2)
        writer.save()
        import os
        os.system('myreport.xlsx')
        ####################################

    def printpreviewDialog(self):
        #Todo: method for export reports pdf file

        title = Text()
        title.setName("Invoice")
        title.setFooter(
            " س ت 36108 ملف  ضريبي 212/306/5 مأموريه  ضرائب الشركات المساهمة رقم التسجيل بضرائب المبيعات 153/846/310 ")
        title.setFont('Scheherazade-Regular.ttf')
        title.setFontsize(10)
        title.setcodeText("15235")
        title.setwaterText("hyperone company")
        title.settelText("1266533")
        title.setbrachText("Entrance 1,EL Sheikh Zayed City")
        title.setCursor(self.Qline_promotion.text)
        title.setQuery(self.query)
        title.setCursor(self.field_names)
        body()
        QtWidgets.QMessageBox.information(self, "Success", "Report is printed successfully")
        import os
        os.system('my_file.pdf')


    def disable(self):
        #Todo: method for disable or enable table based on count of row

        if self.Qtable_promotion.rowCount() == 0:
            self.Qbtn_exprot.setEnabled(False)
            self.Qbtn_print.setEnabled(False)
        else:
            self.Qbtn_exprot.setEnabled(True)
            self.Qbtn_print.setEnabled(True)




    def __init__(self):
        #Todo: method for initialization components


        super(CL_report1, self).__init__()
        try:
            cwd = Path.cwd()
            mod_path = Path(__file__).parent.parent.parent
            dirname = mod_path.__str__() + '/presentation/reports_ui'
            filename = dirname + '/Coupon_display.ui'
            loadUi(filename, self)
            self.setWindowTitle('تقرير الكوبون')

            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(450, 50, 200, 18)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_branchEdition = CheckableComboBox(self)
            self.Qcombo_branchEdition.setGeometry(450, 120, 200, 18)
            self.Qcombo_branchEdition.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branchEdition.setStyleSheet("background-color: rgb(198, 207, 199)")


            self.Qbtn_exit.clicked.connect(self.FN_close)
            self.Qbtn_search.clicked.connect(self.FN_loadData)
            self.FN_GET_Company()
            self.FN_GET_Branch()


            self.Qtable_promotion.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.radioBtnPromExpired.clicked.connect(self.FN_Check_Expired)
            self.radioBtnPromActive.clicked.connect(self.FN_Check_Active)
            self.radioBtnPromAll.clicked.connect(self.FN_Check_All)

            self.Qbtn_exprot.clicked.connect(self.handleSave)
            self.Qbtn_print.clicked.connect(self.printpreviewDialog)

            self.disable()

        except:
            print(sys.exc_info())


class CL_controller():
    def __init__(self):
        pass

    def FN_show_login(self):
        self.report = CL_report1()
        self.report.show()

    def FN_show_main(self):
        self.window = CL_report1()

        self.report.close()

        self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = CL_controller()
    controller.FN_show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
