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
    # self.Qtime_from.dateTime().toString('hh:mm:ss')
    model = QStandardItemModel()

    switch_window = QtCore.pyqtSignal()
    cond = 0
    status = 0
    query = ""
    # sponsor_list = []
    magazine_list = []
    company_list = []
    branch_list = []
    conn = db1.connect()

    prom_status = ""
    prom_CG = ""
    sponsor_prom = ""
    magazine_prom = ""
    list_num = []
    field_names = []

    def FN_close(self):
        #Todo: method for close window

        self.close()



    def FN_loadData(self, PROM_ID):
        #Todo: method for searching about promotions in data base
        try:
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
            else:
                self.branch_list.append("'" "'")



            # if self.QcheckBox_magazine.isChecked():
            #     if len(self.Qcombo_magazine.currentData()) > 0:
            #         for i in self.Qcombo_magazine.currentData():
            #             self.magazine_list.append("'" + i + "'")
            #         self.magazine_prom = "AND `PROMOTION_HEADER`.`MAGAZINE_ID` IN (" + ','.join(
            #             self.magazine_list) + ")"


            self.Qtable_promotion.setRowCount(0)
            self.conn = db1.connect()

            mycursor = self.conn.cursor()
            query = ""
            if self.cond == 1:
                self.query = (
                        "SELECT COP_ID , COP_DESC, COP_DISCOUNT_VAL , COP_DISCOUNT_PERCENT , COP_SERIAL_COUNT , COP_MULTI_USE , COP_MULTI_USE_COUNT , COP_CREAED_ON , COP_CHANGED_ON , COP_VALID_FROM , COP_VALID_TO , COP_STATUS FROM COUPON WHERE COP_ID = '" + self.Qline_promotion.text() + "'"+self.prom_status)
                self.runQuery(mycursor)
                # # print(mycursor.description)
                # print(mycursor.column_names)
                self.field_names = ['COP_ID' , 'COP_DESC', 'COP_DISCOUNT_VAL' , 'COP_DISCOUNT_PERCENT' , 'COP_SERIAL_COUNT' , 'COP_MULTI_USE' , 'COP_MULTI_USE_COUNT' , 'COP_CREAED_ON' , 'COP_CHANGED_ON' , 'COP_VALID_FROM' , 'COP_VALID_TO' , 'COP_STATUS']

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

    def FN_GET_MAGAZINE(self):
        #Todo: method for fills the MAGAZINE combobox

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT MAGAZINE_DESC , MAGAZINE_ID FROM MAGAZINE")
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_magazine.addItem(row, val)
        mycursor.close()


    def FN_Checked_Selected2(self):
        #Todo: method for change kind of Search parameters to search by promotion number

        self.radioBtnPromNum.setChecked(True)
        self.Qline_promotion.setEnabled(True)
        self.cond = 1
        self.Qtable_promotion.setRowCount(0)
        self.disable()


    def FN_Check_Active(self):
        #Todo: method for change status to active

        self.status = 1
        self.Qtable_promotion.setRowCount(0)
        self.disable()
        self.prom_status = "and `COUPON`.`COP_STATUS`='1'"


    def FN_Check_Expired(self):
        #Todo: method for change status to Expired

        self.status = 2
        self.Qtable_promotion.setRowCount(0)
        self.disable()
        self.prom_status = "and `COUPON`.`COP_STATUS`='0'"


    def handleSave(self):
        #Todo: method for export reports excel file

        frame = pd.read_sql(str(self.query), self.conn)
        df = pd.DataFrame(frame,
                          columns=['COP_ID' , 'COP_DESC', 'COP_DISCOUNT_VAL' , 'COP_DISCOUNT_PERCENT' , 'COP_SERIAL_COUNT' , 'COP_MULTI_USE' , 'COP_MULTI_USE_COUNT' , 'COP_CREAED_ON' , 'COP_CHANGED_ON' , 'COP_VALID_FROM' , 'COP_VALID_TO' , 'COP_STATUS'])

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
            self.setWindowTitle('HyperPOS Reporting')

            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(242, 20, 179, 18)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")

            self.Qcombo_branchEdition = CheckableComboBox(self)
            self.Qcombo_branchEdition.setGeometry(242, 45, 179, 18)
            self.Qcombo_branchEdition.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.Qcombo_branchEdition.setStyleSheet("background-color: rgb(198, 207, 199)")


            self.Qbtn_exit.clicked.connect(self.FN_close)
            self.Qbtn_search.clicked.connect(self.FN_loadData)
            self.FN_GET_Company()
            self.FN_GET_Branch()


            # self.FN_GET_promotion_type()
            self.Qtable_promotion.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.radioBtnPromNum.clicked.connect(self.FN_Checked_Selected2)
            # self.radioButton_2.clicked.connect(self.FN_Checked_Selected)
            # self.radioBtnPromNum_2.clicked.connect(self.FN_Checked_Selected3)
            self.radioBtnPromExpired.clicked.connect(self.FN_Check_Expired)
            # self.radioBtnPromStop.clicked.connect(self.FN_Check_Stopped)
            self.radioBtnPromActive.clicked.connect(self.FN_Check_Active)
            # self.radioBtnPromAll.clicked.connect(self.FN_Check_All)

            self.Qline_promotion.setEnabled(False)
            # self.QcheckBox_customer_group.toggled.connect(self.FN_Check_Group)
            # self.QcheckBox_sponsor_prom.toggled.connect(self.FN_Check_Sponsor)
            # self.QcheckBox_department.toggled.connect(self.FN_Check_department)
            # self.QcheckBox_magazine.toggled.connect(self.FN_Check_Magazine)
            self.Qbtn_exprot.clicked.connect(self.handleSave)
            self.groupBox_2.setEnabled(False)
            # self.Qcombo_promotion.setEnabled(False)
            # self.Qline_promotion_2.setEnabled(False)
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
