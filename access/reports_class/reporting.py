#!/usr/bin/env python3
# -*     - coding: utf-8 -*-
"""
Created on Mon Jun 29 19:52:06 2020

@author: hossam
"""

#####
import csv
import os
import sys
import pandas as pd
import numpy as np
from appdirs import unicode
from pandas.tests.io.excel.test_xlwt import xlwt

from access.reports_class.ReportPDF import body, Text
from Validation.Validation import CL_validation
import tempfile
from pathlib import Path

from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets, QtPrintSupport, Qt

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.uic import loadUi
from pdf2image import convert_from_path

from data_connection.h1pos import db1
import sys
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.Qt import QFileInfo
class CL_report(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    cond=4


    def FN_close(self):
        self.close()

    def FN_loadData(self, PROM_ID):
        print(self.cond)
        print(self.Qdate_to.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_from.dateTime().toString('hh:mm:ss'))

        self.Qtable_promotion.setRowCount(0)
        self.conn = db1.connect()


        mycursor = self.conn.cursor()
        query=""
        if self.cond==1:
            query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_ID`= '"+self.Qline_promotion.text()+"'JOIN `prom_branch` ON `prom_branch`.`BRANCH_NO`=(SELECT `branch`.`BRANCH_NO` FROM `branch` WHERE `branch`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==3:
            query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_DETAIL`.`POS_GTIN`= '"+self.Qline_promotion_2.text()+"' and `PROMOTION_DETAIL`.`PROM_START_DATE`='"+self.Qdate_from.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_from.dateTime().toString('hh:mm:ss')+"' and `PROMOTION_DETAIL`.`PROM_END_DATE`='"+self.Qdate_to.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_to.dateTime().toString('hh:mm:ss')+"' JOIN `prom_branch` ON `prom_branch`.`BRANCH_NO`=(SELECT `branch`.`BRANCH_NO` FROM `branch` WHERE `branch`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==2:
            query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_TYPE_ID`= '"+self.Qcombo_promotion.currentText()+"'and `PROMOTION_DETAIL`.`PROM_START_DATE`='"+self.Qdate_from.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_from.dateTime().toString('hh:mm:ss')+"' and `PROMOTION_DETAIL`.`PROM_END_DATE`='"+self.Qdate_to.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_to.dateTime().toString('hh:mm:ss')+"' JOIN `prom_branch` ON `prom_branch`.`BRANCH_NO`=(SELECT `branch`.`BRANCH_NO` FROM `branch` WHERE `branch`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==4:
            query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_STATUS`= 3 JOIN `prom_branch` ON `prom_branch`.`BRANCH_NO`=(SELECT `branch`.`BRANCH_NO` FROM `branch` WHERE `branch`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==5:
            query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_STATUS`= 3 JOIN `prom_branch` ON `prom_branch`.`BRANCH_NO`=(SELECT `branch`.`BRANCH_NO` FROM `branch` WHERE `branch`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")

        mycursor.execute(query)
        records = mycursor.fetchall()
        print(records)
        for row_number, row_data in enumerate( records ):

          self.Qtable_promotion.insertRow( row_number )
          for column_number, data in enumerate( row_data ):
               self.Qtable_promotion.setItem( row_number, column_number, QTableWidgetItem( str( data ) ) )
        mycursor.close()


    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT COMPANY_DESC FROM company" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_company.addItems( row )
        mycursor.close()


    def FN_GET_Branch(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT BRANCH_DESC_A FROM branch" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_branch.addItems( row )
        mycursor.close()
    def FN_GET_CustomerGroup(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT CG_DESC FROM customer_group" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_cust_group.addItems( row )
        mycursor.close()
    def FN_GET_MAGAZINE(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT MAGAZINE_DESC FROM magazine" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_magazine.addItems( row )
        mycursor.close()
    def FN_GET_department(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT DEPARTMENT_DESC FROM department" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_sponsor_2.addItems( row )
        mycursor.close()
    def FN_GET_promotion_sponser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT SPONSER_NAME FROM sponser" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_sponsor.addItems( row )
        mycursor.close()
    def FN_GET_promotion_type(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT PROMT_NAME_EN FROM promotion_type" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_promotion.addItems( row )
        mycursor.close()

    def FN_Checked_Selected(self):
       self.radioBtnPromNum_2.setChecked(False)
       self.radioBtnPromNum.setChecked(False)
       self.Qline_promotion.setEnabled(False)
       self.Qline_promotion.clear()
       self.groupBox_2.setEnabled(True)
       self.Qcombo_promotion.setEnabled(True)
       self.Qline_promotion_2.setEnabled(False)
       self.Qline_promotion_2.clear()
       self.cond=2

    def FN_Checked_Selected2(self):
       self.radioBtnPromNum_2.setChecked(False)
       self.radioButton_2.setChecked(False)
       self.Qcombo_promotion.setEnabled(False)
       self.Qline_promotion.setEnabled(True)
       self.groupBox_2.setEnabled(False)
       self.Qline_promotion_2.setEnabled(False)
       self.Qline_promotion_2.clear()
       self.cond=1

    def FN_Checked_Selected3(self):
       self.radioBtnPromNum.setChecked(False)
       self.radioButton_2.setChecked(False)
       self.Qline_promotion.clear()
       self.Qline_promotion_2.setEnabled(True)
       self.groupBox_2.setEnabled(False)
       self.groupBox_2.setEnabled(True)
       self.Qcombo_promotion.setEnabled(False)
       self.cond=3


    def FN_Check_Group(self):
        if self.QcheckBox_customer_group.isChecked():
            self.Qcombo_cust_group.setEnabled(True)
        else:
            self.Qcombo_cust_group.setEnabled(False)
    def FN_Check_Sponsor(self):
        if self.QcheckBox_sponsor_prom.isChecked():
            self.Qcombo_sponsor.setEnabled(True)
        else:
            self.Qcombo_sponsor.setEnabled(False)
    def FN_Check_department(self):
        if self.QcheckBox_department.isChecked():
            self.Qcombo_sponsor_2.setEnabled(True)
        else:
            self.Qcombo_sponsor_2.setEnabled(False)
    def FN_Check_Magazine(self):
        if self.QcheckBox_magazine.isChecked():
            self.Qcombo_magazine.setEnabled(True)
        else:
            self.Qcombo_magazine.setEnabled(False)

    def handleSave(self):


        # Sample DataFrame
        df = pd.DataFrame(np.random.randn(5, 4), columns=['one', 'two', 'three', 'four'],
                          index=['a', 'b', 'c', 'd', 'e'])

        # Dump Pandas DataFrame to Excel sheet
        writer = pd.ExcelWriter('myreport.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', startrow=2)
        writer.save()
        import os
        os.system('myreport.xlsx')
        ####################################
    def saveFile(self):
        df = pd.DataFrame()
        savePath = QtGui.QFileDialog.getSaveFileName(None, "Blood Hound",
                                                         "Testing.csv", "CSV files (*.csv)")
        rows = self.Qtable_promotion.rowCount()
        columns = self.Qtable_promotion.columnCount()

        for i in range(rows):
            for j in range(columns):
                df.loc[i, j] = str(self.Qtable_promotion.item(i, j).text())
        df.to_csv((savePath), header=None, index=0)

    def printpreviewDialog(self):

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

        body()
        QtWidgets.QMessageBox.information(self, "Success", "Report is printed successfully")
        ######################################################
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
        #                                           " Files (*.pdf)", options=options)
        import os
        os.system('my_file.pdf')
        #print(f.read())
        # dialog = QtPrintSupport.QP
        # rintPreviewDialog()
        # dialog.paintRequested.connect(self.handlePaintRequest)
        # dialog.exec_()

    def handlePaintRequest(self, printer):
        title = Text()

        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        table = cursor.insertTable(self.Qtable_promotion.rowCount(), self.Qtable_promotion.columnCount())
        for row in range(table.rows()):
            for col in range(table.columns()):
                cursor.insertText(self.Qtable_promotion.item(row, col).text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)

        document.print_(printer)

    def __init__(self):
        super(CL_report, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        dirname = mod_path.__str__() + '/presentation/reports_ui'
        filename = dirname + '/Promotion_display.ui'
        loadUi(filename, self)
        self.setWindowTitle('HyperPOS Reporting')
        self.Qbtn_exit.clicked.connect(self.FN_close)
        self.Qbtn_search.clicked.connect(self.FN_loadData)
        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.FN_GET_CustomerGroup()
        self.FN_GET_MAGAZINE()
        self.FN_GET_department()
        self.FN_GET_promotion_sponser()
        self.FN_GET_promotion_type()
        self.Qtable_promotion.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.radioBtnPromNum.clicked.connect(self.FN_Checked_Selected2)
        self.radioButton_2.clicked.connect(self.FN_Checked_Selected)
        self.radioBtnPromNum_2.clicked.connect(self.FN_Checked_Selected3)
        self.Qline_promotion.setEnabled(False)
        self.Qcombo_cust_group.setEnabled(False)
        self.Qcombo_sponsor.setEnabled(False)
        self.Qcombo_sponsor_2.setEnabled(False)
        self.Qcombo_magazine.setEnabled(False)
        self.QcheckBox_customer_group.toggled.connect(self.FN_Check_Group)
        self.QcheckBox_sponsor_prom.toggled.connect(self.FN_Check_Sponsor)
        self.QcheckBox_department.toggled.connect(self.FN_Check_department)
        self.QcheckBox_magazine.toggled.connect(self.FN_Check_Magazine)
        self.Qbtn_exprot.clicked.connect(self.handleSave)
        self.groupBox_2.setEnabled(False)
        self.Qcombo_promotion.setEnabled(False)
        self.Qline_promotion_2.setEnabled(False)
        self.Qbtn_print.clicked.connect(self.printpreviewDialog)

class CL_controller():
    def __init__(self):
        pass

    def FN_show_login(self):
        self.report = CL_report()
        self.report.show()


    def FN_show_main(self):
        self.window = CL_report()

        self.report.close()

        self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = CL_controller()
    controller.FN_show_login()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

