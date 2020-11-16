#!/usr/bin/env python3
# -*     - coding: utf-8 -*-
"""
Created on Mon Jun 29 19:52:06 2020

@author: emad
"""
#####
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from mysql.connector import Error

from access.authorization_class.user import CL_user
# import Controller
from access.main_login_class.main import CL_main
from data_connection.h1pos import db1
from access.authorization_class.user_module import CL_userModule


class CL_report(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()

    def FN_login(self):

        if len(self.LE_userName.text()) > 0 and len(self.LE_password.text()) > 0:
            print("Login!")
            self.username = self.LE_userName.text()
            self.password = self.LE_password.text()
            self.LE_userName.clear()
            self.LE_password.clear()
            self.FN_loadData(self.username, self.password)

        else:

            QtWidgets.QMessageBox.warning(self, "Error", "Please enter your Username and Password")
            # print("Please enter your Username and Password")

    def FN_close(self):
        self.close()

    def FN_loadData(self, PROM_ID):
        self.Qtable_promotion.setRowCount(0)
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("select * from promotion_detail")
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
       self.radioBtnPromNum.setChecked(False)
       self.Qline_promotion.setEnabled(False)
       self.Qline_promotion.clear()
       self.groupBox_2.setEnabled(True)
       self.Qcombo_promotion.setEnabled(True)



    def FN_Checked_Selected2(self):
       self.radioButton_2.setChecked(False)
       self.Qcombo_promotion.setEnabled(False)
       self.Qline_promotion.setEnabled(True)
       self.groupBox_2.setEnabled(False)

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
        self.Qline_promotion.setEnabled(False)
        self.Qcombo_cust_group.setEnabled(False)
        self.Qcombo_sponsor.setEnabled(False)
        self.Qcombo_sponsor_2.setEnabled(False)
        self.Qcombo_magazine.setEnabled(False)
        self.QcheckBox_customer_group.toggled.connect(self.FN_Check_Group)
        self.QcheckBox_sponsor_prom.toggled.connect(self.FN_Check_Sponsor)
        self.QcheckBox_department.toggled.connect(self.FN_Check_department)
        self.QcheckBox_magazine.toggled.connect(self.FN_Check_Magazine)
        self.groupBox_2.setEnabled(False)
        self.Qcombo_promotion.setEnabled(False)


class CL_controller():
    def __init__(self):
        pass

    def FN_show_login(self):
        self.report = CL_report()
    #        self.user = self.login.username
        self.report.switch_window.connect(self.FN_show_main)
        self.report.show()

    def FN_show_main(self):
        self.window = CL_main()
        self.report.close()
        self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = CL_controller()
    controller.FN_show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

