import time
from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

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


class CL_redItem(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''

    def __init__(self):
        super(CL_redItem, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'

    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/createModifyReedemItem.ui'
        loadUi(filename, self)
        conn = db1.connect()
        mycursor = conn.cursor()
        self.Qbtn_search.clicked.connect(self.FN_SEARCH_REDITEM)
        #self.Qbtn_export.clicked.connect(self.FN_SAVE)
        self.Qbtn_exit.clicked.connect(self.FN_exit)

        self.Qradio_active.setChecked(True)

        self.Qcombo_group3 = CheckableComboBox(self)
        self.Qcombo_group3.setGeometry(190, 45, 179, 18)
        self.Qcombo_group3.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_group4 = CheckableComboBox(self)
        self.Qcombo_group4.setGeometry(190, 100, 179, 18)
        self.Qcombo_group4.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.CMB_branch.hide()
        self.CMB_company.hide()

        self.FN_GET_COMPANIES()
        self.FN_GET_BRANCHES()
        for row_number, row_data in enumerate(CL_userModule.myList):
            if row_data[1] == 'Redeem_Item':
                if row_data[4] == 'None':
                    print('hh')
                else:
                    sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                    x = (row_data[4],)
                    mycursor.execute(sql_select_query, x)

                    result = mycursor.fetchone()
                    # print(result)
                    if result[0] == 'create':
                        self.Qbtn_create.setEnabled(True)
                        self.Qbtn_create.clicked.connect(self.FN_CREATE_REDITEM)
                    elif result[0] == 'modify':
                        self.Qbtn_modify.setEnabled(True)
                        self.Qbtn_modify.clicked.connect(self.FN_MODIFY_REDITEM)
                    elif result[0] == 'upload':
                        try:
                            self.Qbtn_upload.setEnabled(True)
                            self.Qbtn_upload.clicked.connect(self.FN_UPLOAD_REDITEM)
                        except Exception as err:
                            print(err)

    def FN_GET_BRANCHES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.company = self.CMB_company.currentText()
        mycursor.execute("SELECT COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_DESC = '" + self.company + "'")
        myresult = mycursor.fetchone()
        self.companyId = myresult[0]

        self.CMB_branch.clear()
        sql_select_query = "SELECT BRANCH_DESC_A  FROM Hyper1_Retail.BRANCH where BRANCH_STATUS   = 1 and COMPANY_ID = '" + self.companyId + "'"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.Qcombo_group4.addItems([row[0]])
            self.CMB_branch.addItems([row[0]])
        mycursor.close()

    def FN_GET_COMPANIES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_company.clear()
        sql_select_query = "SELECT COMPANY_DESC  FROM Hyper1_Retail.COMPANY where COMPANY_STATUS   = 1 "
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.Qcombo_group3.addItems([row[0]])
            self.CMB_company.addItems([row[0]])
        mycursor.close()


    def FN_SEARCH_REDITEM(self):
       try:
            for i in reversed(range(self.Qtable_redeem.rowCount())):
                self.Qtable_redeem.removeRow(i)

            branchs = self.Qcombo_group4.currentData()
            companies = self.Qcombo_group3.currentData()
            date_from = self.Qdate_from.dateTime().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.dateTime().toString('yyyy-MM-dd')
            conn = db1.connect()
            mycursor = conn.cursor()
            whereClause = ""

            if self.Qradio_active.isChecked():
                whereClause = whereClause + 'REDEEM_STATUS = 1 '
            elif self.Qradio_inactive.isChecked():
                whereClause = whereClause + 'REDEEM_STATUS = 0 '

            whereClause = whereClause + " and REDEEM_VALID_FROM >= '" + date_from + "' and REDEEM_VALID_TO <= '" + date_to + "' "

            barcode = self.Qline_barcode.text().strip()
            if  barcode !='' :

                whereClause = whereClause + " and POS_GTIN ='" + barcode + "'"


            # get COMPANY
            company_list = []
            for comp in companies:
                sql = "SELECT COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_DESC = '" + comp + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                company_list.append(myresult[0])

            if len(company_list) > 0:
                if len(company_list) == 1:
                    whereClause = whereClause + " and COMPANY_ID = '" + company_list[0] + "'"
                else:
                    company_list_tuple = tuple(company_list)
                    whereClause = whereClause + " and COMPANY_ID in {}".format(company_list_tuple)
                    # get branchs
            branch_list = []
            for branch in branchs:
                sql = "SELECT BRANCH_NO FROM Hyper1_Retail.BRANCH where BRANCH_DESC_A = '" + branch + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                branch_list.append(myresult[0])

            if len(branch_list) > 0:
                if len(branch_list) == 1:
                    whereClause = whereClause + " and BRANCH_NO ='" + branch_list[0] + "'"
                else:
                    branch_list_tuple = tuple(branch_list)
                    whereClause = whereClause + " and BRANCH_NO in {} ".format(branch_list_tuple)
            # print(whereClause)


            # print(whereClause)
            sql_select_query = "select POS_GTIN, COMPANY_ID,BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_VALID_FROM,REDEEM_VALID_TO,REDEEM_STATUS from Hyper1_Retail.REDEEM_ITEM   where " + whereClause
            print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_redeem.insertRow(row_number)

                for column_number, data in enumerate(row_data):

                    if column_number == 6:
                        data = self.FN_GET_STATUS_DESC(str(data))

                    self.Qtable_redeem.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.Qtable_redeem.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.Qtable_redeem.doubleClicked.connect(self.FN_GET_REDITEM)
            mycursor.close()
       except Exception as err:
            print(err)
    def FN_GET_REDITEM(self):
        try:
            if len(self.Qtable_redeem.selectedIndexes()) > 0:
                rowNo = self.Qtable_redeem.selectedItems()[0].row()

                bar = self.Qtable_redeem.item(rowNo, 0).text()
                company = self.Qtable_redeem.item(rowNo, 1).text()
                branch = self.Qtable_redeem.item(rowNo, 2).text()
                points = self.Qtable_redeem.item(rowNo, 3).text()
                valid_from =self.Qtable_redeem.item(rowNo, 4).text()
                valid_to= self.Qtable_redeem.item(rowNo, 5).text()
                status = self.Qtable_redeem.item(rowNo, 6).text()
                self.Qline_barcode.setText(bar)
                self.Qline_points.setText(points)

                self.CMB_branch.show()
                self.CMB_company.show()
                comp=self.FN_GET_COMP_DESC(company)
                br =self.FN_GET_BRANCH_DESC(branch,company)
                #self. self.Qcombo_group3.hide()
                self.CMB_branch.setCurrentText(br)
                self.CMB_company.setCurrentText(comp)
                self.Qcombo_group3.hide()
                self.Qcombo_group4.hide()
                self.Qline_barcode.setEnabled(False)


                if status == 'Active' :
                    self.Qradio_active.setChecked(True)
                else:
                    self.Qradio_inactive.setChecked(True)

                xto = valid_from.split("-")
                xto1 = xto[2].split(" ")
                print(xto1)
                d = QDate(int(xto[0]), int(xto[1]), int(xto1[0]))
                self.Qdate_from.setDate(d)

                xto = valid_to.split("-")
                xto1 = xto[2].split(" ")
                d1 = QDate(int(xto[0]), int(xto[1]), int(xto1[0]))
                self.Qdate_to.setDate(d1)


        except (Error, Warning) as e:

            return False

    def FN_CREATE_REDITEM(self):
       try:

           branchs = self.Qcombo_group4.currentData()
           companies = self.Qcombo_group3.currentData()
           bar = self.Qline_barcode.text().strip()

           date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
           date_to = self.Qdate_to.date().toString('yyyy-MM-dd')

           points = self.Qline_points.text().strip()
           if self.Qradio_active.isChecked():
              status = 1
           else:
               status = 0

           # mycursor = self.conn.cursor(buffered=True)
           conn=db1.connect()
           mycursor = conn.cursor()
           creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

           # get COMPANY
           company_list = []
           for comp in companies:
               sql = "SELECT COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_DESC = '" + comp + "'"
               mycursor.execute(sql)
               myresult = mycursor.fetchone()
               company_list.append(myresult[0])

           # get branchs
           branch_list = []
           for branch in branchs:
               sql = "SELECT BRANCH_NO FROM Hyper1_Retail.BRANCH where BRANCH_DESC_A = '" + branch + "'"
               mycursor.execute(sql)
               myresult = mycursor.fetchone()
               branch_list.append(myresult[0])



           if  len(self.Qcombo_group3.currentData()) == 0 or len(
                   self.Qcombo_group4.currentData()) == 0  or bar == ''  or points == '' or date_from == '' or date_to == ''    :
               QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")
           else:
               for com in company_list:
                   for br in branch_list:
                       ret = self.FN_CHECK_EXIST(com, br,  bar)
                       if ret == False:
                           sql = "INSERT INTO Hyper1_Retail.REDEEM_ITEM (POS_GTIN,COMPANY_ID," \
                                 "BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_CREATED_ON,REDEEM_CREATED_BY,REDEEM_VALID_FROM" \
                                 ",REDEEM_VALID_TO,REDEEM_STATUS)" \
                                 "values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                           val = (bar, com, br,points, creationDate, CL_userModule.user_name, date_from, date_to,  status)

                           mycursor.execute(sql, val)
                           db1.connectionCommit(conn)
                           mycursor.close()
                           self.FN_REFRESH_DATA_GRID()
                       else:
                           QtWidgets.QMessageBox.warning(self, "Error", "your inputs already exists ")


       except Exception as err:
            print(err)

    def FN_CHECK_EXIST(self,comp,branch,barcode):
        try:
            conn = db1.connect()
            cursor = conn.cursor()
            comp = str(comp)
            barcode =str(barcode)
            sql = "SELECT *  FROM Hyper1_Retail.REDEEM_ITEM where  POS_GTIN ='" + barcode + "' and COMPANY_ID ='" + comp + "' and BRANCH_NO = '" + branch + "'"
            print(sql)
            cursor.execute(sql)
            myresult = cursor.fetchone()
            if cursor.rowcount > 0:
                return True
            else:
                cursor.close()
                return False
        except (Error, Warning) as e:
            return False

    def    FN_REFRESH_DATA_GRID(self):
        try:
            for i in reversed(range(self.Qtable_redeem.rowCount())):
               self.Qtable_redeem.removeRow(i)
            time.sleep(5)
            conn = db1.connect()
            mycursor = conn.cursor()

            sql_select_query = "select POS_GTIN, COMPANY_ID,BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_VALID_FROM,REDEEM_VALID_TO,REDEEM_STATUS from Hyper1_Retail.REDEEM_ITEM "

            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_redeem.insertRow(row_number)

                for column_number, data in enumerate(row_data):

                    if column_number == 6:
                        data = self.FN_GET_STATUS_DESC(str(data))

                    self.Qtable_redeem.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.Qtable_redeem.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.Qtable_redeem.doubleClicked.connect(self.FN_GET_REDITEM)
            mycursor.close()

        except (Error, Warning) as e:
            print(e)
        self.Qtable_redeem.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


    def FN_MODIFY_REDITEM(self):
        try:
            self.CMB_branch.hide()
            self.CMB_company.hide()
            self.Qcombo_group3.show()
            self.Qcombo_group4.show()
            self.Qline_barcode.setEnabled(True)


            branch = self.CMB_branch.currentText()
            comp = self.CMB_company.currentText()
            bar = self.Qline_barcode.text().strip()
            date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
            date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
            comp = self.FN_GET_COMP_ID(comp)
            branch = self.FN_GET_BRANCH_ID(branch,comp)
            points = self.Qline_points.text().strip()

            self.Qline_barcode.setText('')
            self.Qline_points.setText('')
            if self.Qradio_active.isChecked():
                status = 1
            else:
                status = 0


            conn = db1.connect()
            mycursor = conn.cursor()

            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
            # get customer gp id

            sql = "update   Hyper1_Retail.REDEEM_ITEM " \
                  "set REDEEM_POINTS_QTY =%s,REDEEM_VALID_FROM =%s , REDEEM_VALID_TO = %s , " \
                  "REDEEM_STATUS =%s where POS_GTIN = %s and COMPANY_ID = %s and BRANCH_NO = %s "
            val = ( points,   date_from, date_to, status,bar,comp,branch)

            mycursor.execute(sql, val)
            mycursor.close()

            print(mycursor.rowcount, "record updated.")
            QtWidgets.QMessageBox.information(self, "Success", "redeem item is modified successfully")

            db1.connectionCommit(conn)
            self.FN_REFRESH_DATA_GRID()
            print("in modify red item")
        except Exception as err:
            print(err)

    def FN_GET_COMP_ID(self,desc):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_DESC = '" + desc + "'")
        myresult = mycursor.fetchone()
        return myresult[0]

    def FN_GET_BRANCH_ID(self, desc,comp ):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT BRANCH_NO FROM Hyper1_Retail.BRANCH where BRANCH_DESC_A = '" + desc + "' and COMPANY_ID ='"+comp+"'" )
        myresult = mycursor.fetchone()
        return myresult[0]

    def FN_UPLOAD_REDITEM(self):
       try:
           self.window_two = CL_redItem()
           self.window_two.FN_LOAD_UPLOAD()
           self.window_two.show()
       except Exception as err:
            print(err)

    def FN_LOAD_UPLOAD(self):
        try:
            filename = self.dirname + '/uploadRedeemItem.ui'
            loadUi(filename, self)
            self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
            self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD)
            #self.fileName = ''
        except (Error, Warning) as e:
            print(e)

    def FN_GET_STATUS_DESC(self,id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    def FN_GET_COMP_DESC(self,id):
        conn=db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM Hyper1_Retail.COMPANY where COMPANY_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        return myresult[0]

    def FN_GET_BRANCH_DESC(self, id,comp):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT `BRANCH_DESC_A` FROM Hyper1_Retail.BRANCH where BRANCH_NO = '" + id + "' and COMPANY_ID = '"+comp+ "'" )
        myresult = mycursor.fetchone()
        return myresult[0]


    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  " Files (*.xlsx)", options=options)
        self.LE_fileName.setText(fileName)
    def FN_SAVE_UPLOAD(self):
        try:
            fileName = self.LE_fileName.text()

            if fileName !='':
                #self.LE_fileName.setText(self.fileName)
                wb = xlrd.open_workbook(fileName)
                sheet = wb.sheet_by_index(0)

                errorMsg = ''
                createdItem = 0
                nonCreatedItem = 0

                for i in range(sheet.nrows):

                    bar = int(sheet.cell_value(i, 0))

                    company = int(sheet.cell_value(i, 1))
                    branch = sheet.cell_value(i, 2)
                    points = int(sheet.cell_value(i, 3))
                    validFrom = sheet.cell_value(i, 4)
                    validTo = sheet.cell_value(i, 5)
                    status = int(sheet.cell_value(i, 6))

                    if validFrom == '' or validTo == '' or status == '' or company == '' or branch == '' \
                           or points == '':
                        nonCreatedItem = nonCreatedItem + 1
                        QtWidgets.QMessageBox.warning(self, "Error", "Some fields arenot filled")
                        break
                    #                 #     try:
                    #elif CL_validation.FN_validate_date1(validFrom) == True and CL_validation.FN_validation_int(status):
                    else:

                        ret2 = self.FN_CHECK_VALID_BARCCODE(bar)
                        ret5 = self.FN_CHECK_VALID_BRANCH(branch)
                        ret6 = self.FN_CHECK_VALID_COMPANY(company)
                        ret = self.FN_CHECK_EXIST(company, branch, bar)

                        if ret == False and  ret5 == True and ret6 == True and ret2 == True:
                               # \

                          # get max userid
                            conn = db1.connect()
                            mycursor1 = conn.cursor()


                            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                            sql = "INSERT INTO Hyper1_Retail.REDEEM_ITEM (POS_GTIN,COMPANY_ID," \
                              "BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_CREATED_ON,REDEEM_CREATED_BY,REDEEM_VALID_FROM" \
                              ",REDEEM_VALID_TO,REDEEM_STATUS)" \
                              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                            val = (bar, company, branch, points, creationDate, CL_userModule.user_name, validFrom, validTo, status)

                            mycursor1.execute(sql, val)
                            db1.connectionCommit(conn)
                            createdItem = createdItem + 1
                            db1.connectionCommit(conn)
                            mycursor1.close()
                #
                        else:
                            nonCreatedItem = nonCreatedItem + 1
                            self.msgBox1 = QMessageBox()
                            self.msgBox1.setWindowTitle("Information")
                            self.msgBox1.setStandardButtons(QMessageBox.Ok)

                            if ret == True:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " already exists")
                            if ret2 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Barcode")

                            elif ret5 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Branch")
                            elif ret6 == False:
                                j = i + 1
                                self.msgBox1.setText("Line " + str(j) + " has invalid Company")

                            self.msgBox1.show()
                            #self.close()
                            break


                # QtWidgets.QMessageBox.warning( self, "Information", "No of created user ",counter)
                self.msgBox = QMessageBox()

                # Set the various texts
                self.msgBox.setWindowTitle("Information")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.setText(
                    "No of created items '" + str(createdItem) + "'  No of non created items  '" + str(nonCreatedItem) + "'")
                self.msgBox.show()
                self.close()

            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Choose a file")
        except Exception as err:
           print(err)

    def FN_CHECK_VALID_BARCCODE(self, id):
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

    def FN_CHECK_VALID_COMPANY(self, id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.COMPANY where COMPANY_ID = '" + str(id) + "'"
            # print(sql)
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

    def FN_CHECK_VALID_BRANCH(self, id):
        try:
            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.BRANCH where BRANCH_NO = '" + str(id) + "'"
            # print(sql)
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

    def FN_exit(self):
        QApplication.quit()