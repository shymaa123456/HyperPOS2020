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
import xlwt.Workbook
from access.utils.util import *
class CL_redItem(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    old_points =''

    old_valid_from =''
    old_valid_to =''
    old_status= ''

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
        self.Qbtn_search_all.clicked.connect(self.FN_REFRESH_DATA_GRID)

        #self.Qbtn_export.clicked.connect(self.FN_SAVE)
        self.Qbtn_exit.clicked.connect(self.FN_exit)
        self.Qtable_redeem.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.Qtable_redeem.doubleClicked.connect(self.FN_GET_REDITEM)
        self.Qradio_active.setChecked(True)

        self.Qcombo_group3 = CheckableComboBox(self)
        self.Qcombo_group3.setGeometry(190, 45, 179, 18)
        self.Qcombo_group3.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.Qcombo_group4 = CheckableComboBox(self)
        self.Qcombo_group4.setGeometry(190, 90, 179, 18)
        self.Qcombo_group4.setStyleSheet("background-color: rgb(198, 207, 199)")

        self.CMB_branch.hide()
        self.CMB_company.hide()

        self.FN_GET_COMPANIES()
        self.FN_GET_BRANCHES()
        # self.setFixedWidth(789)
        # self.setFixedHeight(571)

        # Set Style
        # self.voucher_num.setStyleSheet(label_num)
        # self.label_2.setStyleSheet(desc_5)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
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

        valid_from = str(datetime.today().strftime('%Y-%m-%d'))

        xto = valid_from.split("-")
        print(xto)
        d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
        self.Qdate_from.setDate(d)
        # Todo: method for get branches



    def FN_SEARCH_REDITEM(self):
       try:
            self.Qline_barcode.setEnabled(True)
            self.Qcombo_group3.show()
            self.Qcombo_group4.show()
            self.CMB_branch.hide()
            self.CMB_company.hide()
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
            company_list = companies

            if len(company_list) > 0:
                if len(company_list) == 1:
                    whereClause = whereClause + " and COMPANY_ID = '" + company_list[0] + "'"
                else:
                    company_list_tuple = tuple(company_list)
                    whereClause = whereClause + " and COMPANY_ID in {}".format(company_list_tuple)
                    # get branchs
            branch_list = branchs


            if len(branch_list) > 0:
                if len(branch_list) == 1:
                    whereClause = whereClause + " and BRANCH_NO ='" + branch_list[0] + "'"
                else:
                    branch_list_tuple = tuple(branch_list)
                    whereClause = whereClause + " and BRANCH_NO in {} ".format(branch_list_tuple)
            # print(whereClause)


            # print(whereClause)
            sql_select_query = "select POS_GTIN, COMPANY_ID,BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_VALID_FROM,REDEEM_VALID_TO,REDEEM_STATUS from Hyper1_Retail.REDEEM_ITEM   where " + whereClause
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_redeem.insertRow(row_number)

                for column_number, data in enumerate(row_data):

                    if column_number == 6:
                        data = util.FN_GET_STATUS_DESC(str(data))
                    elif column_number == 1:
                        data = util.FN_GET_COMP_DESC(str(data))
                    elif column_number == 2:
                        data = util.FN_GET_BRANCH_DESC(str(data))

                    self.Qtable_redeem.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            mycursor.close()
       except Exception as err:
            print(err)
            # Todo: method for get the redeem item details that is mentioned to modify

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
           creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))

           # get COMPANY
           company_list = companies
           # get branchs
           branch_list = branchs

           if  len(self.Qcombo_group3.currentData()) == 0 or len(
                   self.Qcombo_group4.currentData()) == 0  or bar == ''  or points == '' or date_from == '' or date_to == ''    :
               QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
           elif date_to < date_from:
               QtWidgets.QMessageBox.warning(self, "خطأ",
                                             "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
           elif date_from < creationDate1:
               QtWidgets.QMessageBox.warning(self, "خطأ","تاريخ الإنشاء  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")
           else:
               ret1 = self.FN_CHECK_VALID_BARCCODE(bar)
               if ret1 == True :
                   ret2= CL_validation.FN_validation_int(points)
                   if ret2 == True:
                       for com in company_list:
                           for br in branch_list:
                               ret = self.FN_CHECK_EXIST(com, br,  bar)
                               if ret == False:
                                   mycursor1 = conn.cursor()
                                   #get BMC ID
                                   mycursor1.execute("select BMC_ID from Hyper1_Retail.POS_ITEM where POS_GTIN ='"+bar+"'")
                                   myresult = mycursor1.fetchone()
                                   BMC_ID = myresult[0]
                                   sql = "INSERT INTO Hyper1_Retail.REDEEM_ITEM (POS_GTIN,COMPANY_ID," \
                                         "BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_CREATED_ON,REDEEM_CREATED_BY,REDEEM_VALID_FROM" \
                                         ",REDEEM_VALID_TO,REDEEM_STATUS,BMC_ID)" \
                                         "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                                   val = (bar, com, br,points, creationDate, CL_userModule.user_name, date_from, date_to,  status,BMC_ID)

                                   mycursor1.execute(sql, val)
                                   db1.connectionCommit(conn)
                                   mycursor1.close()
                                   QtWidgets.QMessageBox.information(self, "تم", "تم الإنشاء")
                               else:
                                   QtWidgets.QMessageBox.warning(self, "خطأ", "المدخلات موجوده بالفعل ")
                       self.FN_REFRESH_DATA_GRID()
                   else:
                       QtWidgets.QMessageBox.warning(self, "خطأ", "النقاط يجب أن تكون أرقام")
               else:
                   QtWidgets.QMessageBox.warning(self, "خطأ", "الباركود غير صحيح")

       except Exception as err:
            print(err)


    def    FN_REFRESH_DATA_GRID(self):
        try:
            self.Qline_barcode.setEnabled(True)
            self.Qcombo_group3.show()
            self.Qcombo_group4.show()
            self.CMB_branch.hide()
            self.CMB_company.hide()
            for i in reversed(range(self.Qtable_redeem.rowCount())):
               self.Qtable_redeem.removeRow(i)

            conn = db1.connect()
            mycursor = conn.cursor()

            sql_select_query = "select POS_GTIN, COMPANY_ID,BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_VALID_FROM,REDEEM_VALID_TO,REDEEM_STATUS from Hyper1_Retail.REDEEM_ITEM "

            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_redeem.insertRow(row_number)

                for column_number, data in enumerate(row_data):

                    if column_number == 6:
                        data = util.FN_GET_STATUS_DESC(str(data))
                    elif column_number == 1:
                        data = util.FN_GET_COMP_DESC(str(data))
                    elif column_number == 2:
                        data = util.FN_GET_BRANCH_DESC(str(data))

                    self.Qtable_redeem.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            mycursor.close()

        except (Error, Warning) as e:
            print(e)
        self.Qtable_redeem.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def FN_GET_REDITEM(self):
        try:

            if len(self.Qtable_redeem.selectedIndexes()) > 0:
                rowNo = self.Qtable_redeem.selectedItems()[0].row()
                branch = self.Qtable_redeem.item(rowNo, 2).text()
                br_id = util.FN_GET_BRANCH_ID(branch, '1')

                if br_id in CL_userModule.branch[0]:
                    bar = self.Qtable_redeem.item(rowNo, 0).text()
                    company = self.Qtable_redeem.item(rowNo, 1).text()

                    points = self.Qtable_redeem.item(rowNo, 3).text()
                    valid_from = self.Qtable_redeem.item(rowNo, 4).text()
                    valid_to = self.Qtable_redeem.item(rowNo, 5).text()
                    status = self.Qtable_redeem.item(rowNo, 6).text()
                    self.Qline_barcode.setText(bar)
                    self.Qline_points.setText(points)

                    self.old_points = points
                    self.old_valid_from = valid_from
                    self.old_valid_to = valid_to
                    self.old_status = status

                    self.Qcombo_group3.hide()
                    self.Qcombo_group4.hide()
                    self.CMB_branch.show()
                    self.CMB_company.show()

                    # comp = util.FN_GET_COMP_ID(company)
                    # br =util.FN_GET_BRANCH_DESC(branch)

                    # print(br)
                    self.CMB_branch.setCurrentText(branch)
                    self.CMB_company.setCurrentText(company)

                    self.Qline_barcode.setEnabled(False)

                    # self.CMB_company.hide()
                    # self.CMB_branch.hide()
                    if status == 'Active':
                        self.Qradio_active.setChecked(True)
                    else:
                        self.Qradio_inactive.setChecked(True)

                    xto = valid_from.split("-")

                    d = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
                    self.Qdate_from.setDate(d)

                    xto = valid_to.split("-")

                    d1 = QDate(int(xto[0]), int(xto[1]), int(xto[2]))
                    self.Qdate_to.setDate(d1)
                else:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "ليس لك صلاحيه على هذا الفرع")


        except (Error, Warning) as e:

            return False

    def FN_MODIFY_REDITEM(self):
        try:
            if len(self.Qtable_redeem.selectedIndexes()) > 0:
                branch = self.CMB_branch.currentText()
                comp = self.CMB_company.currentText()
                bar = self.Qline_barcode.text().strip()
                date_from = self.Qdate_from.date().toString('yyyy-MM-dd')
                date_to = self.Qdate_to.date().toString('yyyy-MM-dd')
                comp = util.FN_GET_COMP_ID(comp)
                branch = util.FN_GET_BRANCH_ID(branch,comp)
                points = self.Qline_points.text().strip()

                creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))


                if self.Qradio_active.isChecked():
                    status = 1
                else:
                    status = 0

                conn = db1.connect()
                mycursor = conn.cursor()
                if  points == '' :
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال النقاط ")
                elif date_to < date_from:
                    QtWidgets.QMessageBox.warning(self, "خطأ",
                                                  "تاريخ الانتهاء يجب ان يكون اكبر من او يساوي تاريخ الانشاء")
                # elif date_from < creationDate1:
                #     QtWidgets.QMessageBox.warning(self, "خطأ", "تاريخ التعديل  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")

                else:
                        self.CMB_branch.hide()
                        self.CMB_company.hide()
                        self.Qcombo_group3.show()
                        self.Qcombo_group4.show()
                        self.Qline_barcode.setEnabled(True)
                        self.Qline_barcode.setText('')
                        self.Qline_points.setText('')
                        ret2 = CL_validation.FN_validation_int(points)
                        if ret2 == True:
                            sql = "update   Hyper1_Retail.REDEEM_ITEM " \
                                  "set REDEEM_POINTS_QTY =%s,REDEEM_VALID_FROM =%s , REDEEM_VALID_TO = %s , " \
                                  "REDEEM_STATUS =%s where POS_GTIN = %s and COMPANY_ID = %s and BRANCH_NO = %s "
                            val = ( points,   date_from, date_to, status,bar,comp,branch)

                            mycursor.execute(sql, val)
                            mycursor.close()

                            print(mycursor.rowcount, "record updated.")
                            QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل ")

                            db1.connectionCommit(conn)
                            self.FN_REFRESH_DATA_GRID()
                            self.old_status = util.FN_GET_STATUS_id(str(self.old_status))
                            if str(status) != str(self.old_status):
                                util.FN_INSERT_IN_LOG("REDEEM_ITEM", "status", status, self.old_status,bar,comp,branch)
                            if str(points) != str(self.old_points):
                                util.FN_INSERT_IN_LOG("REDEEM_ITEM", "points", points, self.old_points,bar,comp,branch)

                            if str(date_from) != str(self.old_valid_from):
                                util.FN_INSERT_IN_LOG("REDEEM_ITEM", "valid_from", date_from, self.old_valid_from,bar,comp,branch)

                            if str(date_to) != str(self.old_valid_to):
                                util.FN_INSERT_IN_LOG("REDEEM_ITEM", "valid_to", date_to, self.old_valid_to,bar,comp,branch)
                            print("in modify red item")
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")
        except Exception as err:
            print(err)

    def FN_LOAD_UPLOAD(self):
        try:
            filename = self.dirname + '/uploadRedeemItem.ui'
            loadUi(filename, self)
            self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
            self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD)
            self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP1)
            self.setFixedWidth(590)
            self.setFixedHeight(175)
            # self.fileName = ''
        except (Error, Warning) as e:
            print(e)

    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  " Files (*.xlsx)", options=options)
        self.LE_fileName.setText(fileName)
    def FN_UPLOAD_REDITEM(self):
       try:
           self.window_two = CL_redItem()
           self.window_two.FN_LOAD_UPLOAD()
           self.window_two.show()
       except Exception as err:
            print(err)
    def FN_DISPLAY_TEMP1(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)

             wb = xlwt.Workbook()

             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'باركود')
             sheet.write(0, 1, 'الشركه')
             sheet.write(0, 2, 'الفرع')
             sheet.write(0, 3, 'النقاط')
             sheet.write(0, 4, 'من تاريخ')
             sheet.write(0, 5, 'إلى تاريخ')
             sheet.write(0, 6, 'الحاله')
             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)
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
                    creationDate1 = str(datetime.today().strftime('%Y-%m-%d'))
                    if validFrom == '' or validTo == '' or status == '' or company == '' or branch == '' \
                           or points == '':
                        nonCreatedItem = nonCreatedItem + 1
                        QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال جميع البيانات")
                        break
                    elif validFrom < creationDate1:
                        QtWidgets.QMessageBox.warning(self, "خطأ",
                                                      "تاريخ الإنشاء  يجب أن يكون أكبرمن أو يساوي تاريخ اليوم")
                        break
                    else:

                        ret2 = self.FN_CHECK_VALID_BARCCODE(bar)
                        ret5 = self.FN_CHECK_VALID_BRANCH(branch)
                        ret6 = self.FN_CHECK_VALID_COMPANY(company)
                        ret = self.FN_CHECK_EXIST(company, branch, bar)

                        if ret == False and  ret5 == True and ret6 == True and ret2 == True:
                            conn = db1.connect()
                            mycursor1 = conn.cursor()

                            mycursor1.execute("select BMC_ID from Hyper1_Retail.POS_ITEM where POS_GTIN ='" + str(bar) + "'")
                            myresult = mycursor1.fetchone()
                            BMC_ID = myresult[0]
                            creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                            sql = "INSERT INTO Hyper1_Retail.REDEEM_ITEM (POS_GTIN,COMPANY_ID," \
                              "BRANCH_NO,REDEEM_POINTS_QTY,REDEEM_CREATED_ON,REDEEM_CREATED_BY,REDEEM_VALID_FROM" \
                              ",REDEEM_VALID_TO,REDEEM_STATUS,BMC_ID)" \
                              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                            val = (bar, company, branch, points, creationDate, CL_userModule.user_name, validFrom, validTo, status,str(BMC_ID))

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
                QtWidgets.QMessageBox.warning(self, "خطأ", "اختر الملف ")
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
    def FN_CHECK_EXIST(self,comp,branch,barcode):
        try:
            conn = db1.connect()
            cursor = conn.cursor()
            comp = str(comp)
            barcode =str(barcode)
            sql = "SELECT *  FROM Hyper1_Retail.REDEEM_ITEM where  POS_GTIN ='" + barcode + "' and COMPANY_ID ='" + comp + "' and BRANCH_NO = '" + branch + "'"
            #print(sql)
            cursor.execute(sql)
            myresult = cursor.fetchone()
            if cursor.rowcount > 0:
                return True
            else:
                cursor.close()
                return False
        except (Error, Warning) as e:
            return False

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
            sql = "SELECT BRANCH_NO FROM Hyper1_Retail.BRANCH  where BRANCH_NO = '" + str(id) + "'"
            # print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            if mycursor11.rowcount > 0:
                if myresult[0] in CL_userModule.branch[0]:
                    mycursor11.close()
                    return True
            else:
                mycursor11.close()
                return False
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
            for br in CL_userModule.branch :
                if str(val) in  br:
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

    def FN_exit(self):
        QApplication.quit()