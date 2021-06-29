import time
from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import xlwt.Workbook
from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from access.promotion_class.Promotion_Add import CheckableComboBox
from data_connection.h1pos import db1
from mysql.connector import Error
import xlrd
from datetime import datetime
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from PyQt5.QtCore import *
from access.utils.util import *

class CL_loyProg(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    def __init__(self,pp):
        super(CL_loyProg, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))
        self.p=pp
    def onClicked(self):
        #radioButton = self.sender()
        #print(radioButton.name)
        if self.Qradio_barcode.isChecked ():
            self.Qline_barcode.setEnabled(True)
            self.CMB_department.setEnabled(False)
            self.CMB_section.setEnabled(False)
            self.CMB_level4.setEnabled(False)

        elif self.Qradio_bmc.isChecked ():
            self.Qline_barcode.setEnabled(False)
            self.CMB_department.setEnabled(True)
            self.CMB_section.setEnabled(True)
            self.CMB_level4.setEnabled(True)

    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/createModifyLoyalityProg.ui'
        loadUi(filename, self)
        conn = db1.connect()
        mycursor = conn.cursor()

        valid_from = str(datetime.today().strftime('%Y-%m-%d'))

        xto = valid_from.split("-")
        print(xto)
        d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
        self.Qdate_from.setDate(d)

        self.Qradio_barcode.clicked.connect(self.onClicked)
        self.Qradio_bmc.clicked.connect(self.onClicked)
        self.Qradio_bmc.setChecked(True)
        self.Qradio_active.setChecked(True)

        self.Qcombo_group2 = CheckableComboBox(self)
        self.Qcombo_group2.setGeometry(385, 64, 179, 18)
        self.Qcombo_group2.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_group3 = CheckableComboBox(self)
        self.Qcombo_group3.setGeometry(385, 25, 179, 18)
        self.Qcombo_group3.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_group4 = CheckableComboBox(self)
        self.Qcombo_group4.setGeometry(385, 45, 179, 18)
        self.Qcombo_group4.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_group5 = CheckableComboBox(self)
        self.Qcombo_group5.setGeometry(385, 85, 179, 18)
        self.Qcombo_group5.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_group6 = CheckableComboBox(self)
        self.Qcombo_group6.setGeometry(205, 152, 120, 18)
        self.Qcombo_group6.setStyleSheet("background-color: rgb(198, 207, 199)")
        self.setFixedWidth(1028)
        self.setFixedHeight(560)
        self.CMB_custGroup.hide()
        self.CMB_branch.hide()
        self.CMB_company.hide()
        self.CMB_loyalityType.hide()
        self.CMB_level4.hide()



        self.FN_GET_COMPANIES()
        self.FN_GET_BRANCHES()

        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()
    #
        self.FN_GET_DEPARTMENTS()

        #self.FN_GET_SECTIONS()
        #self.FN_GET_BMCLEVEL4()
        self.CMB_department.activated.connect( self.FN_GET_SECTIONS )
        self.CMB_section.activated.connect(self.FN_GET_BMCLEVEL4)
        #self.Qbtn_add.clicked.connect(self.FN_ADD_LOYPROG)

        self.Qbtn_search.clicked.connect(self.FN_SEARCH_LOYPROG)
        self.Qbtn_exit.clicked.connect(self.FN_exit)
    # #     #check authorization
        #print(CL_userModule.myList)
        for row_number, row_data in enumerate( CL_userModule.myList ):
           if  row_data[1] =='Display_Loyality':
               if row_data[4] =='None':
                print('hh')
               else:
                   sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                   x = (row_data[4],)
                   mycursor.execute(sql_select_query, x)

                   result = mycursor.fetchone()
                   #print(result)
                   if result[0] == 'create' :
                        self.Qbtn_create.setEnabled(True)
                        self.Qbtn_create.clicked.connect(self.FN_CREATE_LOYPROG)
                   elif result[0] == 'modify':
                        self.Qbtn_modify.setEnabled(True)
                        self.Qbtn_modify.clicked.connect(self.FN_MODIFY_LOYPROG)
                   elif result[0] == 'upload':
                       try:
                        self.Qbtn_upload.setEnabled(True)
                        self.Qbtn_upload.clicked.connect(self.FN_UPLOAD_LOYPROG)
                       except Exception as err:
                         print(err)
                   elif result[0] == 'activate':
                       try:
                        self.Qbtn_activate.setEnabled(True)
                        self.Qbtn_activate.clicked.connect(self.FN_ACTIVATE_LOYPROG)
                       except Exception as err:
                         print(err)

    def FN_ACTIVATE_LOYPROG(self):

        ids = []
        id = self.label_ID.text().strip()
        if self.Qradio_active.isChecked():
            status = 1
        else:
            status = 0
        conn = db1.connect()
        mycursor = conn.cursor()


        sql = "update   Hyper1_Retail.LOYALITY_PROGRAM set LOY_STATUS=%s where LOY_PROGRAM_ID = %s "
        val = (status, id)
        mycursor.execute(sql, val)
        mycursor.close()
        QtWidgets.QMessageBox.information(self, "نجاح", "  تم تعديل الحاله")

        db1.connectionCommit(conn)
        db1.connectionClose(conn)
        if str(status) != str(self.old_status):
            util.FN_INSERT_IN_LOG("LOYALITY_PROGRAM", "status", status, self.old_status, id)
        ids.append(id)
        self.FN_REFRESH_DATA_GRID(ids)

    def FN_DISPLAY_TEMP(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)

             wb = xlwt.Workbook()

             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'اسم البرنامج')
             sheet.write(0, 1, 'الوصف')
             sheet.write(0, 2, 'تاريخ البدايه')
             sheet.write(0, 3, 'تاريخ النهايه')


             sheet.write(0, 4, 'الحاله')
             sheet.write(0, 5, 'الشركه')
             sheet.write(0, 6, 'الفرع')
             sheet.write(0, 7, 'مجموعه العملاء')
             sheet.write(0, 8, 'نوع العضويه')
             sheet.write(0, 9, 'الباركود')
             sheet.write(0, 10, 'BMC')

             sheet.write(0, 11, 'مبلغ الشراء')
             sheet.write(0, 12, 'النقاط المستحقه')

             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)
    def FN_LOAD_UPLOAD(self):
        try:
            filename = self.dirname + '/uploadLoyalityProg.ui'
            loadUi(filename, self)
            self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
            self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD)
            self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP)
            #self.fileName = ''
            self.setFixedWidth(576)
            self.setFixedHeight(178)
        except (Error, Warning) as e:
            print(e)
    def FN_GET_BRANCHES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.company = self.CMB_company.currentData()
        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A ,`BRANCH_NO`  FROM Hyper1_Retail.BRANCH where BRANCH_STATUS   = 1 and COMPANY_ID = '"+self.company+"'"
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row, val in records:
            for br in CL_userModule.branch:
                if str(val) in br:
                    self.Qcombo_group4.addItem(row, val)
                    self.CMB_branch.addItem(row, val)
        mycursor.close()

    def FN_GET_COMPANIES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_company.clear()
        sql_select_query = "SELECT COMPANY_DESC ,COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row, val in records:
            self.Qcombo_group3.addItem(row, val)
            self.CMB_company.addItem(row, val)
        mycursor.close()

    def FN_GET_DEPARTMENTS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_department.clear()
        sql_select_query = "SELECT DEPARTMENT_DESC FROM Hyper1_Retail.DEPARTMENT where DEPARTMENT_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_department.addItems( [row[0]] )

        mycursor.close()
        self.FN_GET_SECTIONS()
    def FN_GET_SECTIONS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_section.clear()
        dept = self.CMB_department.currentText()

        sql_select_query = "SELECT SECTION_DESC ,SECTION_ID  FROM Hyper1_Retail.SECTION s inner join Hyper1_Retail.DEPARTMENT d ON " \
                           "d.`DEPARTMENT_ID` = s.`DEPARTMENT_ID`" \
                           "where SECTION_STATUS   = 1 and `DEPARTMENT_DESC`= '"+dept+"'"
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        if mycursor.rowcount >0 :
            for row, val in records:
                for sec in CL_userModule.section:
                    if str(val) in sec:
                        self.CMB_section.addItem(row, val)


            self.FN_GET_BMCLEVEL4()
        mycursor.close()
    def FN_GET_BMCLEVEL4(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.Qcombo_group6.clear()
        sec = self.CMB_section.currentData()
        if sec !=  None:

            sql_select_query = "SELECT BMC_LEVEL4_DESC ,BMC_LEVEL4 FROM Hyper1_Retail.BMC_LEVEL4 b where BMC_LEVEL4_STATUS   = 1 " \
                               "and SECTION_ID= '"+sec+"'"
            #print(sql_ select_query)
            mycursor.execute( sql_select_query )
            records = mycursor.fetchall()
            self.Qcombo_group6.addItem("All")
            for row, val in records:
                self.Qcombo_group6.addItem(row, val)
            mycursor.close()
            self.Qcombo_group6.setChecked(0)
    def FN_GET_CUSTGP(self):
        #print("pt11")
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT CG_DESC ,CG_GROUP_ID FROM Hyper1_Retail.CUSTOMER_GROUP order by CG_GROUP_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        #print("pt12")
        for row, val in records:
            self.CMB_custGroup.addItem(row, val)
            self.Qcombo_group2.addItem(row, val)
        #print(self.Qcombo_group2.currentData())

    def FN_GET_CUSTTP(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_DESC ,LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE order by LOYCT_TYPE_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        for row, val in records:
            self.CMB_loyalityType.addItem(row, val)
            self.Qcombo_group5.addItem(row, val)

    def FN_GET_CUSTTP_ID(self,desc):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+desc+"'" )
        records = mycursor.fetchone()
        mycursor.close()
        return records[0]

    def FN_CHECK_VALID_BMC(self,id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql="SELECT * FROM Hyper1_Retail.BMC_LEVEL4 where BMC_LEVEL4 = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount>0:
                mycursor11.close()
                return True
            else :
                mycursor11.close()
                return False
        except (Error, Warning) as e:
            print(e)

    def FN_CHECK_VALID_BARCCODE(self,id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_ITEM where POS_GTIN = '" + str(id) + "'"
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False
        except (Error, Warning) as e:
            print(e)

    def FN_CHECK_VALID_CUSTGP(self,id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.CUSTOMER_GROUP where CG_GROUP_ID  ='" + str(id) + "'"
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False
        except (Error, Warning) as e:
            print(e)
    def FN_CHECK_VALID_CUSTTP(self,id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID ='" + str(id) + "'"
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False
        except (Error, Warning) as e:
            print(e)
    def FN_CHECK_VALID_COMPANY(self,id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.COMPANY where COMPANY_ID = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False
        except (Error, Warning) as e:
            print(e)
    def FN_CHECK_VALID_BRANCH(self,id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.BRANCH where BRANCH_NO = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False
        except (Error, Warning) as e:
            print(e)
    # # endregion
    def FN_CHECK_EXIST(self,comp,branch,ctgp,cttp,level4,barcode):
        conn = db1.connect()
        cursor = conn.cursor()
        comp = str(comp)
        level4= str(level4)
        if barcode =='' :
            sql ="SELECT *  FROM Hyper1_Retail.LOYALITY_PROGRAM where LOY_STATUS = 1 and  COPMAPNY_ID ='"+str(comp)+"' and BRANCH_NO = '"+branch+"' and CG_GROUP_ID='"+str(ctgp)+"' and LOYCT_TYPE_ID ='"+str(cttp)+"' and BMC_ID = '"+str(level4)+"' "
            #print(sql)
            cursor.execute(sql)
        else :
            sql = "SELECT *  FROM Hyper1_Retail.LOYALITY_PROGRAM where  LOY_STATUS = 1 and COPMAPNY_ID ='" + str(comp) + "' and BRANCH_NO = '" + branch + "' and CG_GROUP_ID='" + str(ctgp) + "' and LOYCT_TYPE_ID ='" + str(cttp) + "' and POS_GTIN = '" + str(barcode) + "'"
            #print(sql)
            cursor.execute(sql)
        myresult = cursor.fetchone()

        try:
            if cursor.rowcount > 0:
                #cursor.close()
                return True
            else:
                cursor.close()
                return False
        except (Error, Warning) as e:
            return False

    def FN_GET_CUSTGP_DESC(self, id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CG_DESC FROM Hyper1_Retail.CUSTOMER_GROUP where CG_GROUP_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        return myresult[0]

    def FN_GET_BMC_DESC(self, id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT BMC_LEVEL4_DESC  FROM Hyper1_Retail.BMC_LEVEL4 where BMC_LEVEL4=  '" + id + "'")
        myresult = mycursor.fetchone()
        return myresult[0]

    def FN_CLEAR_FEILDS(self):
        self.label_ID.setText("")
        self.Qline_name.setText("")

        self.Qtext_desc.setText("")
        self.Qline_purchAmount.setValue(0)
        self.Qline_points.setValue(0)
    def FN_SEARCH_LOYPROG(self):

       try:
            self.FN_CLEAR_FEILDS()
            for i in reversed(range(self.Qtable_loyality.rowCount())):
                self.Qtable_loyality.removeRow(i)
            sec = self.CMB_section.currentText()
            BMC_LEVEL4s = self.Qcombo_group6.currentData()
            #self.mycursor = self.conn.cursor()
            cust_gps = self.Qcombo_group2.currentData()
            cust_tps = self.Qcombo_group5.currentData()
            branchs = self.Qcombo_group4.currentData()
            companies = self.Qcombo_group3.currentData()
            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            conn = db1.connect()
            mycursor = conn.cursor()
            whereClause = ""

            if self.Qradio_active.isChecked():
                whereClause = whereClause + 'LOY_STATUS = 1 '
            elif self.Qradio_inactive.isChecked():
                whereClause = whereClause + 'LOY_STATUS = 0 '

            whereClause = whereClause + " and LOY_VALID_FROM >= '" + date_from + "' and LOY_VALID_TO <= '" + date_to + "' "

            if self.Qradio_barcode.isChecked():
                barcode = self.Qline_barcode.text().strip()
                whereClause = whereClause + " and POS_GTIN ='" + barcode + "'"
            elif self.Qradio_bmc.isChecked():
                # get bmc_level4
                BMC_LEVEL4_list = []
                if len(BMC_LEVEL4s) == 0:
                    BMC_LEVEL4s[0] = 'All'
                if BMC_LEVEL4s[0] == 'All':
                    mycursor.execute(
                        "SELECT BMC_LEVEL4  FROM Hyper1_Retail.BMC_LEVEL4 b inner join Hyper1_Retail.SECTION s ON " \
                        "b.`SECTION_ID` = s.`SECTION_ID`" \
                        "where BMC_LEVEL4_STATUS   = 1 and `SECTION_DESC`= '" + sec + "'")
                    records =mycursor.fetchall()
                    for row in records:
                        BMC_LEVEL4_list.append(row[0])
                else:
                    # for BMC_LEVEL4 in BMC_LEVEL4s:
                    #     sql = "SELECT BMC_LEVEL4 FROM Hyper1_Retail.BMC_LEVEL4 where BMC_LEVEL4_DESC = '" + BMC_LEVEL4 + "'"
                    #     mycursor.execute(sql)
                    #     myresult = mycursor.fetchone()
                    #     BMC_LEVEL4_list.append(myresult[0])
                    BMC_LEVEL4_list = BMC_LEVEL4s

                if len(BMC_LEVEL4_list) > 0:
                    if len(BMC_LEVEL4_list) == 1 :
                        if BMC_LEVEL4_list == 'ALL' :
                            BMC_LEVEL4_list_tuple = tuple(BMC_LEVEL4_list)
                            whereClause = whereClause + " and BMC_ID in {}".format(BMC_LEVEL4_list_tuple)
                        else:
                            whereClause = whereClause + " and BMC_ID = '" + BMC_LEVEL4_list[0] + "'"
                    else:
                        BMC_LEVEL4_list_tuple = tuple(BMC_LEVEL4_list)
                        whereClause = whereClause + " and  BMC_ID in {}".format(BMC_LEVEL4_list_tuple)

            # get COMPANY
            company_list = companies

            if len(company_list) > 0:
                if len(company_list) == 1:
                    whereClause = whereClause + " and COPMAPNY_ID = '" + company_list[0] + "'"
                else:
                    company_list_tuple = tuple(company_list)
                    whereClause = whereClause + " and COPMAPNY_ID in {}".format(company_list_tuple)
                    # get branchs
            branch_list = branchs

            if len(branch_list) > 0:
                if len(branch_list) == 1:
                    whereClause = whereClause + " and BRANCH_NO ='" + branch_list[0] + "'"
                else:
                    branch_list_tuple = tuple(branch_list)
                    whereClause = whereClause + " and BRANCH_NO in {} ".format(branch_list_tuple)

            # get customer gp id
            cust_gp_list = cust_gps

            if len(cust_gp_list) > 0:
                if len(cust_gp_list) == 1:
                    whereClause = whereClause + " and CG_GROUP_ID ='" + cust_gp_list[0] + "'"
                else:
                    cust_gp_list_tuple = tuple(cust_gp_list)
                    whereClause = whereClause + " and CG_GROUP_ID in {}".format(cust_gp_list_tuple)

            # get customer type
            cust_tp_list = cust_tps

            if len(cust_tp_list) > 0:
                if len(cust_tp_list) == 1:
                    whereClause = whereClause + " and LOYCT_TYPE_ID = '" + cust_tp_list[0] + "'"
                else:
                    cust_tp_list_tuple = tuple(cust_tp_list)
                    whereClause = whereClause + " and LOYCT_TYPE_ID in {}".format(cust_tp_list_tuple)

            sql_select_query = "select LOY_PROGRAM_ID, LOY_NAME ,LOY_DESC,LOY_VALID_FROM,LOY_VALID_TO, LOY_STATUS,COPMAPNY_ID,BRANCH_NO,CG_GROUP_ID,LOYCT_TYPE_ID,POS_GTIN,BMC_ID,LOY_VALUE,LOY_POINTS from Hyper1_Retail.LOYALITY_PROGRAM    where " + whereClause
            print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_loyality.insertRow(row_number)

                for column_number, data in enumerate(row_data):

                    if column_number == 5:
                        data = util.FN_GET_STATUS_DESC(str(data))
                    elif column_number == 6:
                        data = util.FN_GET_COMP_DESC(str(data))
                    elif column_number == 7:
                        data = util.FN_GET_BRANCH_DESC(str(data))
                    elif column_number == 8:
                        data = self.FN_GET_CUSTGP_DESC(str(data))
                    elif column_number == 9:
                        data = util.FN_GET_CUSTTP_DESC(str(data))
                    elif column_number == 11:
                        data = self.FN_GET_BMC_DESC(str(data))

                    self.Qtable_loyality.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.Qtable_loyality.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.Qtable_loyality.doubleClicked.connect(self.FN_GET_LOYPROG)
            mycursor.close()
       except (Error, Warning) as e:
           print(e)
    def FN_GET_LOYPROG(self):
        try:
            if len(self.Qtable_loyality.selectedIndexes()) > 0:
                rowNo = self.Qtable_loyality.selectedItems()[0].row()
                id =self.Qtable_loyality.item(rowNo, 0).text()
                name = self.Qtable_loyality.item(rowNo, 1).text()
                desc = self.Qtable_loyality.item(rowNo, 2).text()
                status = self.Qtable_loyality.item(rowNo, 5).text()
                amount = self.Qtable_loyality.item(rowNo, 12).text()
                points = self.Qtable_loyality.item(rowNo, 13).text()
                valid_from =self.Qtable_loyality.item(rowNo, 3).text()
                valid_to= self.Qtable_loyality.item(rowNo, 4).text()

                self.old_name=name
                self.old_status=util.FN_GET_STATUS_id(status)
                self.old_amount=amount
                self.old_points=points
                self.old_valid_from = valid_from
                self.old_valid_to = valid_to

                self.Qline_name.setText(name)
                self.label_ID.setText(id)
                self.Qtext_desc.setText(desc)
                self.Qline_purchAmount.setValue(float(amount))
                self.Qline_points.setValue(int(points))

                if status == 'Active' :
                    self.Qradio_active.setChecked(True)
                else:
                    self.Qradio_inactive.setChecked(True)

                xto = valid_from.split("-")
                print(xto)
                d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
                self.Qdate_from.setDate(d)
                xto = valid_to.split("-")

                d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
                self.Qdate_to.setDate(d)

        except Exception as err:
            print(err)

    def FN_exit(self):
        QApplication.quit()
    def   FN_CREATE_LOYPROG(self):
        ids=[]
        cust_gps = self.Qcombo_group2.currentData()
        cust_tps = self.Qcombo_group5.currentData()
        branchs = self.Qcombo_group4.currentData()
        companies = self.Qcombo_group3.currentData()
        self.name = self.Qline_name.text().strip()
        self.desc = self.Qtext_desc.toPlainText().strip()
        self.date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
        self.date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
        BMC_LEVEL4s = self.Qcombo_group6.currentData()
        self.section = self.CMB_section.currentData()
        self.level4 = self.CMB_level4.currentData()
        self.barcode = self.Qline_barcode.text().strip()
        self.purchAmount = self.Qline_purchAmount.text().strip()
        self.points = self.Qline_points.text().strip()

        conn = db1.connect()
        # mycursor = self.conn.cursor(buffered=True)
        self.mycursor = conn.cursor()
        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        company_list = companies
        branch_list = branchs
        cust_gp_list = cust_gps
        cust_tp_list = cust_tps
        if self.Qradio_barcode.isChecked():
            self.barcode = self.Qline_barcode.text().strip()

        elif self.Qradio_bmc.isChecked():

            # get BMC level
            BMC_LEVEL4_list = []
            if len(self.Qcombo_group6.currentData()) > 0:
                if BMC_LEVEL4s[0] =='All' :
                    conn = db1.connect()
                    mycursor = conn.cursor()
                    sql_select_query = "SELECT BMC_LEVEL4_DESC ,BMC_LEVEL4 FROM Hyper1_Retail.BMC_LEVEL4 b where BMC_LEVEL4_STATUS   = 1 " \
                                       "and SECTION_ID= '" + self.section + "'"
                    mycursor.execute(sql_select_query)
                    records = mycursor.fetchall()
                    for row in records:
                        BMC_LEVEL4_list.append(row[1])
                    mycursor.close()
                else:
                        BMC_LEVEL4_list= BMC_LEVEL4s


        if len(self.Qcombo_group2.currentData()) == 0 or len(self.Qcombo_group3.currentData()) == 0 or len(
                self.Qcombo_group4.currentData()) == 0 or  len(self.Qcombo_group6.currentData()) == 0 or len(
                self.Qcombo_group5.currentData()) == 0 or self.name == '' or self.desc == '' or float(self.purchAmount) == 0 or self.points == '0' or self.date_from == '' or self.date_to == '' \
                :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
        elif self.date_to  < self.date_from :
            QtWidgets.QMessageBox.warning(self, "خطأ",
                                          "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
        elif self.date_from < self.creationDate1:
                QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ الإنشاء  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")

        else:
            for com in company_list:
                for br in branch_list:
                    for ctgp in cust_gp_list:
                        for cttp in cust_tp_list:
                            for BMC_LEVEL4 in     BMC_LEVEL4_list :
                                ret = self.FN_CHECK_EXIST(com, br, ctgp, cttp, BMC_LEVEL4, self.barcode)

                                if ret == False:
                                    try:
                                        print("pt1")
                                        # self.mycursor.close()

                                        self.mycursor1 = conn.cursor()
                                        self.mycursor1.execute(
                                            "SELECT max(cast(LOY_PROGRAM_ID AS UNSIGNED)) FROM Hyper1_Retail.LOYALITY_PROGRAM")
                                        myresult = self.mycursor1.fetchone()
                                        if myresult[0] == None:
                                            self.id = "1"
                                        else:
                                            self.id = int(myresult[0]) + 1
                                        ids.append(self.id)
                                        # mycursor = self.conn.cursor()
                                        sql = "INSERT INTO Hyper1_Retail.LOYALITY_PROGRAM (LOY_PROGRAM_ID,COPMAPNY_ID," \
                                              "BRANCH_NO,CG_GROUP_ID,BMC_ID,POS_GTIN,LOY_NAME,LOY_DESC,LOY_CREATED_ON,LOY_CREATED_BY," \
                                              "LOY_VALID_FROM,LOY_VALID_TO,LOY_VALUE,LOY_POINTS,LOYCT_TYPE_ID,LOY_STATUS)" \
                                              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                                        val = (self.id, com, br, ctgp, BMC_LEVEL4, self.barcode, self.name, self.desc,
                                               creationDate, CL_userModule.user_name, self.date_from, self.date_to,
                                               self.purchAmount, self.points, cttp, '0')

                                        self.mycursor1.execute(sql, val)

                                        db1.connectionCommit(conn)
                                        self.mycursor1.close()

                                    except (Error, Warning) as e:
                                        print(e)
                                else:
                                    QtWidgets.QMessageBox.warning(self, "Error", "المدخلات بالفعل نوجوده")
                                    continue

        self.FN_REFRESH_DATA_GRID(ids)
        # self.close()
    def    FN_REFRESH_DATA_GRID(self,ids):
        try:
            for i in reversed(range(self.Qtable_loyality.rowCount())):
               self.Qtable_loyality.removeRow(i)
            #time.sleep(5)
            conn = db1.connect()
            mycursor = conn.cursor()
            i = 0
            for id in ids:

                sql_select_query = "select LOY_PROGRAM_ID, LOY_NAME ,LOY_DESC,LOY_VALID_FROM,LOY_VALID_TO, LOY_STATUS,COPMAPNY_ID,BRANCH_NO,CG_GROUP_ID,LOYCT_TYPE_ID,POS_GTIN,BMC_ID,LOY_VALUE,LOY_POINTS from Hyper1_Retail.LOYALITY_PROGRAM    where LOY_PROGRAM_ID =%s"

                val = (id,)
                mycursor.execute(sql_select_query,val)
                record = mycursor.fetchone()
                self.Qtable_loyality.insertRow(i)
                for column_number, data in enumerate(record):

                    if column_number == 5:
                        data = util.FN_GET_STATUS_DESC(str(data))
                    elif column_number == 6:
                        data = util.FN_GET_COMP_DESC(str(data))
                    elif column_number == 7:
                        data = util.FN_GET_BRANCH_DESC(str(data))
                    elif column_number == 8:
                        data = self.FN_GET_CUSTGP_DESC(str(data))
                    elif column_number == 9:
                        data = util.FN_GET_CUSTTP_DESC(str(data))
                    elif column_number == 11:
                        data = self.FN_GET_BMC_DESC(str(data))

                    self.Qtable_loyality.setItem(i, column_number, QTableWidgetItem(str(data)))
                i=i+1
        except (Error, Warning) as e:
            print(e)
        self.Qtable_loyality.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def FN_UPLOAD_LOYPROG(self):
        self.window_two = CL_loyProg()
        self.window_two.FN_LOAD_UPLOAD()
        self.window_two.show()

    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  " Files (*.xlsx)", options=options)
        self.LE_fileName.setText(fileName)
    def FN_SAVE_UPLOAD(self):
        #self.fileName ="C:/Users/Shaymaa/Desktop/Book2.xlsx"
        #self.FN_OPEN_FILE()
        fileName = self.LE_fileName.text()

        if fileName !='':
            #self.LE_fileName.setText(self.fileName)
            wb = xlrd.open_workbook(fileName)
            sheet = wb.sheet_by_index(0)

            errorMsg = ''
            createdProg = 0
            nonCreatedProg = 0

            for i in range(sheet.nrows):
                try:
                    name = sheet.cell_value(i, 0)
                    desc = sheet.cell_value(i, 1)
                    #validFrom = sheet.cell_value(i, 2)
                    validFrom =  str(sheet.cell_value(i, 2))
                    validTo = sheet.cell_value(i, 3)
                    status = int(sheet.cell_value(i, 4))
                    company = int(sheet.cell_value(i, 5))
                    branch = sheet.cell_value(i, 6)
                    custGroup = int(sheet.cell_value(i, 7))
                    loyalityType = int(sheet.cell_value(i, 8))
                    barcode = ''
                    if sheet.cell_value(i, 9) == '' :
                        print('barcode')
                    else:
                        barcode = int(sheet.cell_value(i, 9))
                    bmc = int(sheet.cell_value(i, 10))
                    purchAmount = int(sheet.cell_value(i, 11))
                    points = int(sheet.cell_value(i, 12))
                except Exception as err:
                    print(err)
                if name == '' or desc == '' or validFrom == '' or validTo == '' or status == '' or company == '' or branch == '' \
                            or custGroup == '' or loyalityType == ''  or purchAmount == '' or points == '':
                        nonCreatedProg = nonCreatedProg + 1
                        QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")

                elif validTo < validFrom:
                    QtWidgets.QMessageBox.warning(self, "خطأ",
                                                  "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                    break
                elif validFrom < self.creationDate1:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ الإنشاء  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")
                    break

                #                 #     try:
                #elif CL_validation.FN_validate_date1(validFrom) == True and CL_validation.FN_validation_int(status):
                else:
                    try:
                        ret= self.FN_CHECK_EXIST(company, branch, custGroup, loyalityType, bmc,barcode)
                        ids = []
                        if barcode == '':
                            ret2 = True
                            bmc = int(bmc)
                            ret1 = self.FN_CHECK_VALID_BMC(bmc)
                        else:
                            ret1=True
                            ret2 = self.FN_CHECK_VALID_BARCCODE(barcode)

                        ret3 = self.FN_CHECK_VALID_CUSTGP(custGroup)
                        ret4 = self.FN_CHECK_VALID_CUSTTP(loyalityType)
                        ret5 = self.FN_CHECK_VALID_BRANCH(branch)
                        ret6 = self.FN_CHECK_VALID_COMPANY(company)

                        if ret == False and ret1 == True and ret2 == True and ret3 == True and ret4 == True and ret5 == True and ret6 == True :
                          # get max userid
                            conn = db1.connect()
                            mycursor1 = conn.cursor()
                            mycursor1.execute("SELECT max(cast(LOY_PROGRAM_ID AS UNSIGNED)) FROM Hyper1_Retail.LOYALITY_PROGRAM")
                            myresult = mycursor1.fetchone()

                            if myresult[0] == None:
                                self.id = "1"
                            else:
                                self.id = int(myresult[0]) + 1
                            ids.append(self.id)

                            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                            sql = "INSERT INTO Hyper1_Retail.LOYALITY_PROGRAM (LOY_PROGRAM_ID,COPMAPNY_ID," \
                                  "BRANCH_NO,CG_GROUP_ID,BMC_ID,POS_GTIN,LOY_NAME,LOY_DESC,LOY_CREATED_ON,LOY_CREATED_BY," \
                                  "LOY_VALID_FROM,LOY_VALID_TO,LOY_VALUE,LOY_POINTS,LOYCT_TYPE_ID,LOY_STATUS)" \
                                  "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            # "values ('"+self.id+"','" +com+"', '"+br+"',' "+ctgp+"','','"+self.barcode+"','" +self.name+"' ,'" +self.desc+"','" + creationDate+"',CL_userModule.user_name+"',' \
                            # '" +self.date_to+"'+ self.purchAmount+"',self.points+"','" +cttp+"','" +self.status +"")"

                            val = (self.id, company, branch, custGroup, bmc, barcode, name, desc,
                                   creationDate, CL_userModule.user_name, validFrom, validTo,
                                   purchAmount, points, loyalityType, status)
                            mycursor1.execute(sql, val)
                            createdProg = createdProg + 1
                            db1.connectionCommit(conn)
                            mycursor1.close()
                #
                        else:
                            nonCreatedProg = nonCreatedProg + 1
                            self.msgBox1 = QMessageBox()
                            self.msgBox1.setWindowTitle("Information")
                            self.msgBox1.setStandardButtons(QMessageBox.Ok)


                            if ret ==True:
                                j=i+1
                                self.msgBox1.setText("Line " + str(j) + " already exists")
                            elif ret1==False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid BMC")
                            elif ret2 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Barcode")
                            elif ret3 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Customer Gp")
                            elif ret4 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Customer Type")
                            elif ret5 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Branch")
                            elif ret6 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Company")

                            self.msgBox1.show()
                            #self.close()
                            break
                    except Exception as err:
                        print(err)
            if createdProg >0:
                db1.connectionClose(conn)
            # QtWidgets.QMessageBox.warning( self, "Information", "No of created user ",counter)
            self.msgBox = QMessageBox()

            # Set the various texts
            self.msgBox.setWindowTitle("Information")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.setText(
                "No of created programs '" + str(createdProg) + "'  No of non created programs  '" + str(nonCreatedProg) + "'")
            self.msgBox.show()
            #if createdProg>0:
                #self.FN_REFRESH_DATA_GRID(ids)
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إختيار الملف ")
    def FN_MODIFY_LOYPROG(self):
        try:

            ids=[]
            id = self.label_ID.text().strip()
            if len(id) == 0:
                QtWidgets.QMessageBox.warning(self, "خطأ", "لم يتم إختيار أي برنامج")
            else:
                name = self.Qline_name.text().strip()
                desc = self.Qtext_desc.toPlainText().strip()
                purchAmount = self.Qline_purchAmount.text().strip()
                points = self.Qline_points.text().strip()
                date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
                date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
                if name == '' or desc == '' or float(purchAmount) == 0 or points == '0' or date_from == '' or date_to == '' \
                        :
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
                elif date_to < date_from:
                    QtWidgets.QMessageBox.warning(self, "خطأ",
                                                  "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                elif date_from < self.creationDate1:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ التعديل  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")

                else:

                    conn = db1.connect()
                    mycursor = conn.cursor()

                    changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
                    # get customer gp id

                    sql = "update   Hyper1_Retail.LOYALITY_PROGRAM set LOY_NAME = %s , LOY_DESC = %s , LOY_VALID_FROM = %s ,LOY_VALID_TO = %s ,LOY_VALUE = %s ,LOY_POINTS = %s  , LOY_CHANGED_BY = %s where LOY_PROGRAM_ID = %s "
                    val = (name ,desc ,date_from,date_to, purchAmount ,points,CL_userModule.user_name,id)
                    mycursor.execute(sql, val)
                    mycursor.close()
                    ids.append(id)
                    print( mycursor.rowcount, "record updated." )
                    QtWidgets.QMessageBox.information(self, "Success", "تم التعديل")

                    db1.connectionCommit( conn )
                    db1.connectionClose( conn )
                    #self.close()


                    if str(points) != str(self.old_points):
                        util.FN_INSERT_IN_LOG("LOYALITY_PROGRAM", "points", points, self.old_points,id)

                    if str(date_from) != str(self.old_valid_from):
                        util.FN_INSERT_IN_LOG("LOYALITY_PROGRAM", "valid_from", date_from, self.old_valid_from,id)

                    if str(date_to) != str(self.old_valid_to):
                        util.FN_INSERT_IN_LOG("LOYALITY_PROGRAM", "valid_to", date_to, self.old_valid_to,id)

                    if str(purchAmount) != str(self.old_amount):
                        util.FN_INSERT_IN_LOG("LOYALITY_PROGRAM", "amount", purchAmount, self.old_amount,id)
                    if str(name) != str(self.old_name):
                        util.FN_INSERT_IN_LOG("LOYALITY_PROGRAM", "name", name, self.old_name,id)
                    print( "in modify cust" )
                    self.FN_REFRESH_DATA_GRID(ids)
        except Exception as err:
            print(err)