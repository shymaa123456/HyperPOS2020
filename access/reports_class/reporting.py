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
#from appdirs import unicode
from pandas.tests.io.excel.test_xlwt import xlwt
from mysql.connector import Error

import mysql.connector
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
#from pdf2image import convert_from_path

from data_connection.h1pos import db1
import sys
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.Qt import QFileInfo
class CL_report(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    cond=0
    status=0
    query=""
    conn=db1.connect()

    def FN_close(self):
        self.close()

    def FN_loadData(self, PROM_ID):
        print(self.cond)
        print(self.status)
        print(self.Qdate_to.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_from.dateTime().toString('hh:mm:ss'))

        self.Qtable_promotion.setRowCount(0)
        self.conn = db1.connect()


        mycursor = self.conn.cursor()
        query=""
        if self.cond==1:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_ID`= '"+self.Qline_promotion.text()+"'JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==3:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_DETAIL`.`POS_GTIN`= '"+self.Qline_promotion_2.text()+"' and `PROMOTION_DETAIL`.`PROM_START_DATE`='"+self.Qdate_from.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_from.dateTime().toString('hh:mm:ss')+"' and `PROMOTION_DETAIL`.`PROM_END_DATE`<='"+self.Qdate_to.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_to.dateTime().toString('hh:mm:ss')+"' JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==2:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID`and `PROMOTION_HEADER`.`PROM_TYPE_ID`= (SELECT `PROMOTION_TYPE`.`PROMOTION_TYPE_ID` FROM `PROMOTION_TYPE` WHERE `PROMOTION_TYPE`.`PROMT_NAME_AR`='"+self.Qcombo_promotion.currentText()+"')and `PROMOTION_DETAIL`.`PROM_START_DATE`<='"+self.Qdate_from.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_from.dateTime().toString('hh:mm:ss')+"' and `PROMOTION_DETAIL`.`PROM_END_DATE`>='"+self.Qdate_to.dateTime().toString('yyyy-MM-dd')+" "+self.Qtime_to.dateTime().toString('hh:mm:ss')+"' JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==4:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `promotion_group` ON `PROMOTION_GROUP`.`CG_GROUP_ID`=(SELECT `CUSTOMER_GROUP`.`CG_GROUP_ID` FROM `CUSTOMER_GROUP` WHERE `CUSTOMER_GROUP`.`CG_DESC`='"+self.Qcombo_cust_group.currentText()+"')")
        elif self.cond==5:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROMOTION_SPONSER` ON `PROMOTION_SPONSER`.`SPONSER_ID`=(SELECT `SPONSER`.`SPONSER_ID` FROM `SPONSER` WHERE `SPONSER`.`SPONSER_NAME`='"+self.Qcombo_sponsor.currentText()+"')")
        elif self.cond==6:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==7:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"') AND `PROMOTION_HEADER`.`MAGAZINE_ID`=(SELECT `MAGAZINE`.`MAGAZINE_ID` FROM `MAGAZINE` WHERE `MAGAZINE`.`MAGAZINE_DESC`='"+self.Qcombo_magazine.currentText()+"')")
        elif self.cond==8 or self.cond==9 or self.cond==10:
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` AND `PROMOTION_DETAIL`.`PROM_STATUS`='"+str(self.status)+"' JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")
        elif self.cond==11 :
            self.query=  ("SELECT `PROMOTION_HEADER`.`PROM_ID`, `PROMOTION_HEADER`.`PROM_TYPE_ID`, `PROMOTION_HEADER`.`PROM_CREATED_BY`, `PROMOTION_HEADER`.`PROM_CREATED_ON`, `PROMOTION_DETAIL`.`PROM_LINE_NO`, `PROMOTION_DETAIL`.`POS_ITEM_NO`,`PROMOTION_DETAIL`.`POS_GTIN`,`PROMOTION_DETAIL`.`BMC_ID`,`PROMOTION_DETAIL`.`PROM_PRICE_BEFORE_DISC`,`PROMOTION_DETAIL`.`PROM_ITEM_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_GROUP_SCALE_FLAG`,`PROMOTION_DETAIL`.`PROM_DISCOUNT_FLAG`,`PROMOTION_DETAIL`.`PROM_ITEM_QTY`,`PROMOTION_DETAIL`.`PROM_ITEM_DISC_VAL`,`PROMOTION_DETAIL`.`PROM_ITEM_PRICE`,`PROMOTION_DETAIL`.`PROM_START_DATE`,`PROMOTION_DETAIL`.`PROM_END_DATE`,`PROMOTION_DETAIL`.`PROM_STATUS` FROM `PROMOTION_HEADER` JOIN `PROMOTION_DETAIL` ON `PROMOTION_HEADER`.`PROM_ID`=`PROMOTION_DETAIL`.`PROM_ID` JOIN `PROM_BRANCH` ON `PROM_BRANCH`.`BRANCH_NO`=(SELECT `BRANCH`.`BRANCH_NO` FROM `BRANCH` WHERE `BRANCH`.`BRANCH_DESC_A`='"+self.Qcombo_branch.currentText()+"')")


        mycursor.execute(self.query)
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
        mycursor.execute( "SELECT COMPANY_DESC FROM COMPANY" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_company.addItems( row )
        mycursor.close()


    def FN_GET_Branch(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT BRANCH_DESC_A FROM BRANCH" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_branch.addItems( row )
        mycursor.close()
    def FN_GET_CustomerGroup(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT CG_DESC FROM CUSTOMER_GROUP" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_cust_group.addItems( row )
        mycursor.close()
    def FN_GET_MAGAZINE(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT MAGAZINE_DESC FROM MAGAZINE" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_magazine.addItems( row )
        mycursor.close()
    def FN_GET_department(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT DEPARTMENT_DESC FROM DEPARTMENT" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_sponsor_2.addItems( row )
        mycursor.close()
    def FN_GET_promotion_sponser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT SPONSER_NAME FROM SPONSER" )
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_sponsor.addItems( row )
        mycursor.close()
    def FN_GET_promotion_type(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute( "SELECT PROMT_NAME_AR FROM PROMOTION_TYPE order by PROMOTION_TYPE_ID*1 " )
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
            self.cond=4
        else:
            self.Qcombo_cust_group.setEnabled(False)
    def FN_Check_Sponsor(self):
        if self.QcheckBox_sponsor_prom.isChecked():
            self.Qcombo_sponsor.setEnabled(True)
            self.cond=5

        else:
            self.Qcombo_sponsor.setEnabled(False)
    def FN_Check_department(self):
        if self.QcheckBox_department.isChecked():
            self.Qcombo_sponsor_2.setEnabled(True)
            self.cond=6

        else:
            self.Qcombo_sponsor_2.setEnabled(False)
    def FN_Check_Magazine(self):
        if self.QcheckBox_magazine.isChecked():
            self.Qcombo_magazine.setEnabled(True)
            self.cond=7
        else:
            self.Qcombo_magazine.setEnabled(False)

    def FN_Check_Active(self):
        self.cond = 8
        self.status=3

    def FN_Check_Stopped(self):
        self.cond = 9
        self.status=0

    def FN_Check_Expired(self):
        self.cond = 10
        self.status=2
    def FN_Check_All(self):
        self.cond = 11



    def handleSave(self):

        connection = mysql.connector.connect(host='localhost', database='Hyper1_Retail'
                                             , user='root', port='3306')
        frame = pd.read_sql(str(self.query),self.conn)
        df = pd.DataFrame(frame,columns=['PROM_ID', 'PROM_TYPE_ID', 'PROM_CREATED_BY', 'PROM_CREATED_BY', 'PROM_CREATED_ON','PROM_LINE_NO'])

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
        title.setQuery(self.query)

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
        self.radioBtnPromExpired.clicked.connect(self.FN_Check_Expired)
        self.radioBtnPromStop.clicked.connect(self.FN_Check_Stopped)
        self.radioBtnPromActive.clicked.connect(self.FN_Check_Active)
        self.radioBtnPromAll.clicked.connect(self.FN_Check_All)
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

