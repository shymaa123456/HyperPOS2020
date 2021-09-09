from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from data_connection.h1pos import db1
import sys
from Validation.Validation import CL_validation

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import xlrd
from datetime import datetime
import xlwt.Workbook
from access.utils.util import *
from access.reports_class.ReportPDF import body, Text
from access.Checkable import CheckableComboBox
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
            filename = self.dirname + '/installment.ui'
            loadUi(filename, self)
            conn = db1.connect()
            mycursor = conn.cursor()
            self.Qbtn_search.clicked.connect(self.FN_SEARCH)

            # Apply Style For Design
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

            #Get installment type
            self.FN_GET_installment_types_period()
            self.Qcombo_installmentType.addItem("Select type", '0')
            # test Multi selection for company

            #drob down list with multiselection for company
            self.Qcombo_company = CheckableComboBox(self)
            self.Qcombo_company.setGeometry(490,20,179,20)
            self.Qcombo_company.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.Qcombo_company.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.FN_GET_Company()

            # TODO Click listner for changing list of company
            self.Qcombo_company.model().dataChanged.connect(self.FN_GET_Branch)

            #drob down list with multiselection for bracnch
            self.Qcombo_branch = CheckableComboBox(self)
            self.Qcombo_branch.setGeometry(490,60,179,20)
            self.Qcombo_branch.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.Qcombo_branch.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.FN_GET_Branch()

            #validation for not pick date before today
            datefrom = str(datetime.today().strftime('%Y-%m-%d'))
            xfrom = datefrom.split("-")
            d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
            self.Qdate_from.setDate(d)
            self.Qdate_to.setDate(d)

            # Get customer Groupe
            self.Qcombo_customerGroupe = CheckableComboBox(self)
            self.Qcombo_customerGroupe.setGeometry(490, 100, 179, 20)
            self.Qcombo_customerGroupe.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.Qcombo_customerGroupe.setStyleSheet("background-color: rgb(198, 207, 199)")
            self.FN_GET_customerGroupe()

            # Multi selection for department
            self.Qcombo_department = CheckableComboBox(self)
            self.Qcombo_department.setGeometry(630, 190, 85, 22)
            self.Qcombo_department.setEnabled(False)
            self.Qcombo_department.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.Qcombo_department.setStyleSheet("background-color: rgb(198, 207, 199)")

            # TODO Click listner for changing list of department
            self.Qcombo_department.model().dataChanged.connect(self.FN_WhenChecksection)

            # get Department list if check box
            self.checkBox_department.stateChanged.connect(self.FN_WhenCheckDepartment)
            # self.FN_WhenCheckDepartment()

            # Multi selection for sections
            self.Qcombo_section = CheckableComboBox(self)
            self.Qcombo_section.setGeometry(490, 190, 80, 22)
            self.Qcombo_section.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.Qcombo_section.setEnabled(False)
            self.Qcombo_section.setStyleSheet("background-color: rgb(198, 207, 199)")

            # get sections list if check box
            self.checkBox_section.stateChanged.connect(self.FN_WhenChecksection)
            # self.FN_GET_sections()

            # TODO Click listner for changing list of department
            self.Qcombo_section.model().dataChanged.connect(self.FN_WhenCheckBMC_Level)

            # Multi selection for BMCLevel
            self.Qcombo_BMCLevel = CheckableComboBox(self)
            self.Qcombo_BMCLevel.setGeometry(270, 190, 110, 22)
            self.Qcombo_BMCLevel.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.Qcombo_BMCLevel.setEnabled(False)
            self.Qcombo_BMCLevel.setStyleSheet("background-color: rgb(198, 207, 199)")

            # get BMC LEVEL4 list if check box
            self.checkBox_BMCLevel.stateChanged.connect(self.FN_WhenCheckBMC_Level)
            # self.FN_GET_BMC_Level()

            # get Banks list if readio button clicked
            self.RBTN_bank.clicked.connect(self.FN_InstallMent_Checked)

            # get Vendor list if readio button clicked
            self.RBTN_vendor.clicked.connect(self.FN_InstallMent_Checked)

            # if readio button clicked hyperone
            self.RBTN_hyperone.clicked.connect(self.FN_InstallMent_Checked)


            # this function for what enabled or not when start
            self.EnabledWhenOpen()
            self.Rbtn_stsAll.setChecked(True)
        except Exception as err:
            print(err)


    # this function for what enabled or not when start
    def EnabledWhenOpen(self):
        self.checkBox_department.setEnabled(True)
        self.checkBox_section.setEnabled(False)
        self.Qcombo_section.setEnabled(False)
        self.checkBox_BMCLevel.setEnabled(False)
        self.Qcombo_BMCLevel.setEnabled(False)

    #get installments period list
    def FN_GET_installment_types_period(self):
        #self.Qcombo_installmentType.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT InstT_Installment_Period ,INSTT_TYPE_ID FROM INSTALLMENT_TYPE")
        records = mycursor.fetchall()
        mycursor.close()
        for row, val in records:
            self.Qcombo_installmentType.addItem(row, val)
        # get branches list

    # get companys list
    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC , COMPANY_ID FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_company.addItem(row, val)
        mycursor.close()

    # get branches list
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

            print("companies", val3)

            sqlite3 = "SELECT BRANCH_DESC_A ,BRANCH_NO FROM BRANCH WHERE COMPANY_ID in (" + val3 + ")"

            print("Branches_sqlite3", sqlite3)

            mycursor.execute(sqlite3)

            records = mycursor.fetchall()
            for row, val in records:
                for bra in CL_userModule.branch:
                    if val in bra:
                        self.Qcombo_branch.addItem(row, val)
                    i += 1
            mycursor.close()
            self.Qcombo_branch.setCurrentIndex(-1)
        except:
            print(sys.exc_info())

    # get customer Groupe list
    def FN_GET_customerGroupe(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT CG_DESC,CG_GROUP_ID FROM CUSTOMER_GROUP")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_customerGroupe.addItem(row, val)
        mycursor.close()

    # after check department check box
    def FN_WhenCheckDepartment(self):
        if self.checkBox_department.isChecked():
            self.FN_GET_Department()
            self.Qcombo_department.setEnabled(True)
            self.checkBox_section.setEnabled(True)
            self.Qcombo_department.setCurrentIndex(-1)


        else:
            self.Qcombo_department.unCheckedList()
            self.Qcombo_department.setEnabled(False)
            self.checkBox_section.setEnabled(False)
            self.checkBox_section.setChecked(False)
            self.checkBox_BMCLevel.setChecked(False)
            self.Qcombo_department.setCurrentIndex(-1)

    # get Department list
    def FN_GET_Department(self):
        self.Qcombo_department.clear()
        i = 0
        try:
            # Todo: method for fills the section combobox
            """
            self.Qcombo_department.clear()
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT DEPARTMENT_DESC,DEPARTMENT_ID FROM DEPARTMENT")
            records = mycursor.fetchall()

            for row, val in records:
                for sec in CL_userModule.section :
                    if val in sec:
                        self.Qcombo_department.addItem(row, val)
                    i += 1
            mycursor.close()
            """
            print("FN_GET_Department", CL_userModule.section)

            for row, val, row1, val1 in CL_userModule.section:
                self.Qcombo_department.addItem(val1, row1)
        except:
            print(sys.exc_info())

    # after check section check box
    def FN_WhenChecksection(self):
        if self.checkBox_section.isChecked():
            self.FN_GET_sections()
            self.checkBox_BMCLevel.setEnabled(True)
            self.Qcombo_section.setEnabled(True)
            self.Qcombo_section.setCurrentIndex(-1)

        else:
            self.Qcombo_section.unCheckedList()
            self.checkBox_BMCLevel.setChecked(False)
            self.checkBox_BMCLevel.setEnabled(False)
            self.Qcombo_section.setEnabled(False)
            self.Qcombo_section.setCurrentIndex(-1)
            # self.Qcombo_section.unChecked()

    # get sections list
    def FN_GET_sections(self):
        self.Qcombo_section.clear()
        i = 0
        try:
            conn = db1.connect()
            mycursor = conn.cursor()
            print("currentData", self.Qcombo_department.currentData())
            val3 = ""
            for a in range(len(self.Qcombo_department.currentData())):
                if a < len(self.Qcombo_department.currentData()) - 1:
                    val3 = val3 + "'" + self.Qcombo_department.currentData()[a] + "',"
                else:
                    val3 = val3 + "'" + self.Qcombo_department.currentData()[a] + "'"

            print("deparments", val3)

            mycursor.execute("SELECT SECTION_DESC,SECTION_ID FROM SECTION where DEPARTMENT_ID in (" + val3 + ")")
            # print("Query"+"SELECT SECTION_DESC,SECTION_ID FROM SECTION where DEPARTMENT_ID in ("+val3+")")
            records = mycursor.fetchall()
            mycursor.close()
            for row, val in records:
                self.Qcombo_section.addItem(row, val)
                i += 1
        except:
            print(sys.exc_info())
        # after check department check box

    # after check BMC Level check box
    def FN_WhenCheckBMC_Level(self):
        if self.checkBox_BMCLevel.isChecked():
            self.FN_GET_BMC_Level()
            self.Qcombo_BMCLevel.setEnabled(True)
            self.Qcombo_BMCLevel.setCurrentIndex(-1)
            # self.FN_
        else:
            self.Qcombo_BMCLevel.unCheckedList()
            self.checkBox_BMCLevel.setChecked(False)
            self.Qcombo_BMCLevel.setEnabled(False)
            self.Qcombo_BMCLevel.setCurrentIndex(-1)

    # get BMC LEVEL4 list
    def FN_GET_BMC_Level(self):
        self.Qcombo_BMCLevel.clear()
        i = 0
        try:
            conn = db1.connect()
            mycursor = conn.cursor()

            val3 = ""
            for a in range(len(self.Qcombo_section.currentData())):
                if a < len(self.Qcombo_section.currentData()) - 1:
                    val3 = val3 + "'" + self.Qcombo_section.currentData()[a] + "',"
                else:
                    val3 = val3 + "'" + self.Qcombo_section.currentData()[a] + "'"

            print("sections", val3)
            mycursor.execute("SELECT BMC_LEVEL4_DESC,BMC_LEVEL4 FROM BMC_LEVEL4 where SECTION_ID in (" + val3 + ")")
            records = mycursor.fetchall()
            mycursor.close()
            for row, val in records:
                self.Qcombo_BMCLevel.addItem(row, val)
                i += 1
        except:
            print(sys.exc_info())


    def FN_InstallMent_Checked(self):
        if self.RBTN_bank.isChecked():
            self.FN_GET_Banks()
            self.Qcombo_bank.setEnabled(True)
            self.Qcombo_vendor.setEnabled(False)
            self.Qcombo_vendor.clear()
            self.QTEdit_sponsorReason.setEnabled(False)

        elif self.RBTN_vendor.isChecked():
            self.Qcombo_bank.setEnabled(False)
            self.Qcombo_bank.clear()
            self.FN_GET_Vendor()
            self.Qcombo_vendor.setEnabled(True)
            self.QTEdit_sponsorReason.setEnabled(True)

        elif self.RBTN_hyperone.isChecked():
            self.Qcombo_bank.setEnabled(False)
            self.Qcombo_bank.clear()
            self.Qcombo_vendor.setEnabled(False)
            self.Qcombo_vendor.clear()
            self.QTEdit_sponsorReason.setEnabled(False)
        # TO clear Data From QTable


    def FN_SEARCH(self):
        try:

            for i in reversed(range(self.Qtable_inst.rowCount())):
                self.Qtable_inst.removeRow(i)

            cust_gps = self.Qcombo_customerGroupe.currentData()
            branchs = self.Qcombo_branch.currentData()
            companies = self.Qcombo_company.currentData()

            instType= self.Qcombo_installmentType.currentData()
            instDesc = self.LE_desc.text()

            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            conn = db1.connect()
            mycursor = conn.cursor()
            whereClause = ""
            ### Call Validation Function
            if self.Rbtn_stsActive.isChecked():
                whereClause = whereClause + ' INST_STATUS = 1'
            elif self.Rbtn_stsInactive.isChecked():
                whereClause = whereClause + '  INST_STATUS = 0'
            elif self.Rbtn_stsAll.isChecked():
                whereClause = whereClause + '  INST_STATUS in ( 0,1)'

            if instDesc !='':
                whereClause = whereClause + " and  p.INST_DESC like '%" + str(instDesc) + "%'  "

            # get COMPANY
            if len(companies) > 0:
                if len(companies) == 1:
                    whereClause = whereClause + " and c.COMPANY_ID = '" + companies[0] + "'"
                else:
                    company_list_tuple = tuple(companies)
                    whereClause = whereClause + " and c.COMPANY_ID in {}".format(company_list_tuple)
            # get branchs

            if len(branchs) > 0:
                if len(branchs) == 1:
                    whereClause = whereClause + " and b.BRANCH_NO ='" + branchs[0] + "'"
                else:
                    branch_list_tuple = tuple(branchs)
                    whereClause = whereClause + " and b.BRANCH_NO in {} ".format(branch_list_tuple)

            # get customer gp id
            if len(cust_gps) > 0:
                if len(cust_gps) == 1:
                    whereClause = whereClause + " and g.CG_GROUP_ID ='" + cust_gps[0] + "'"
                else:
                    cust_gp_list_tuple = tuple(cust_gps)
                    whereClause = whereClause + " and g.CG_GROUP_ID in {}".format(cust_gp_list_tuple)

            if instType !='0':
                whereClause = whereClause + " and tp.INSTT_TYPE_ID = '" +str(instType)+"'"
            whereClause = whereClause + " and INST_VALID_FROM >= '" + date_from + "' and INST_VALID_TO <= '" + date_to + "' "
            sql_select_query = "SELECT p.INST_PROGRAM_ID, p.INST_DESC , p.INST_VALID_FROM,p.INST_VALID_TO,p.INST_ADMIN_EXPENSES_PERC,p.INST_STATUS,r.INSTR_HYPER_RATE,r.INSTR_SPONSOR_RATE,r.INSTR_CUSTOMER_RATE,tp.INSTT_DESC,cg.CG_DESC,s.SPONSOR_ID,bank.Bank_Desc ,s.HYPERONE,spon.SPONSOR_NAME,c.COMPANY_DESC,branch.BRANCH_DESC_A FROM Hyper1_Retail.INSTALLMENT_PROGRAM p inner join Hyper1_Retail.INSTALLMENT_RULE r on p.INSTR_RULEID = r.INSTR_RULEID inner join Hyper1_Retail.INSTALLMENT_TYPE tp on  r.INSTT_TYPE_ID = tp.INSTT_TYPE_ID   inner join Hyper1_Retail.INSTALLMENT_GROUP g on  p.INST_PROGRAM_ID = g.INST_PROGRAM_ID inner join Hyper1_Retail.INSTALLMENT_BRANCH b on  p.INST_PROGRAM_ID = b.INST_PROGRAM_ID inner join Hyper1_Retail.INSTALLMENT_SPONSOR s on  p.INSTR_RULEID =  s.INSTR_RULEID  left outer join Hyper1_Retail.BANK bank on s.BANK_ID = bank.Bank_ID left outer join Hyper1_Retail.SPONSOR spon on spon.SPONSOR_ID = s.SPONSOR_ID left outer join CUSTOMER_GROUP cg on g.CG_GROUP_ID = cg.CG_GROUP_ID  inner join Hyper1_Retail.BRANCH branch on b.COMPANY_ID = branch.COMPANY_ID and  b.BRANCH_NO = branch.BRANCH_NO inner join  Hyper1_Retail.COMPANY c on branch.COMPANY_ID =c.COMPANY_ID where"+ whereClause


            print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            print(records)
        except Exception as err:
            print(err)

