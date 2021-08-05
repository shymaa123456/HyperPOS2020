from pathlib import Path
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

from Validation.Validation import CL_validation

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
import xlrd
from datetime import datetime
import xlwt.Workbook
from access.utils.util import *


class CL_customer(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    parent =''
    modify_flag=0
    def __init__(self):
        super(CL_customer, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()

    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadCustomers.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
        self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD)
        self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP)
        self.fileName = ''
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        #self.setFixedWidth(576)
        #self.setFixedHeight(178)
    def FN_LOAD_UPLOAD_PT(self):

        filename = self.dirname + '/uploadCustPt.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
        self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD1)
        self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP1)
        self.fileName = ''
        self.FN_GET_BRANCHES()
        self.FN_GET_REDEEMTPS()
        # self.setFixedWidth(576)
        # self.setFixedHeight(178)

        # Set Style
        # self.voucher_num.setStyleSheet(label_num)
        # self.label_2.setStyleSheet(desc_5)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
    def FN_GET_BRANCHES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT BRANCH_DESC_A ,`BRANCH_NO`  FROM Hyper1_Retail.BRANCH where BRANCH_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        self.CMB_branch.addItem('أختر الفرع', "")
        for row , val in records:
            for br in CL_userModule.branch :
                if str(val) in  br:
                    self.CMB_branch.addItem(row,val)
        mycursor.close

    def FN_GET_REDEEMTPS(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        self.CMB_redeemType.addItem('أختر النوع', "")
        sql_select_query =    "SELECT REDEEMT_DESC,REDEEMT_TYPE_ID FROM Hyper1_Retail.REDEEM_TYPE where REDEEMT_STATUS = '1' order by REDEEMT_TYPE_ID*1   asc"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row , val in records:
            self.CMB_redeemType.addItem(row,val)
        mycursor.close
        return records

    def FN_DISPLAY_TEMP(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)

             wb = xlwt.Workbook()

             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'اسم العميل')
             sheet.write(0, 1, 'مجموعه العملاء')
             sheet.write(0, 2, 'نوع العضويه')
             sheet.write(0, 3, 'رقم الهاتف')
             sheet.write(0, 4, 'الموبايل')
             sheet.write(0, 5, 'الوظيفه')
             sheet.write(0, 6, 'العنوان')
             sheet.write(0, 7, 'المدينه')
             sheet.write(0, 8, 'المجاوره')
             sheet.write(0, 9, 'المبنى')

             sheet.write(0, 10, 'الطابق')
             sheet.write(0, 11, 'الإيميل')
             sheet.write(0, 12, 'الشركه')
             sheet.write(0, 13, 'تليفون الشركه')
             sheet.write(0, 14, 'عنوان الشركه')
             sheet.write(0, 15, 'الحاله')
             sheet.write(0, 16, 'ملاحظات')
             sheet.write(0, 17, 'رقم البطاقه')

             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)
# get customer type desc
    def FN_DISPLAY_TEMP1(self):
         try:
             filename = QFileDialog.getSaveFileName(self, "Template File", '', "(*.xls)")
             print(filename)

             wb = xlwt.Workbook()

             # add_sheet is used to create sheet.
             sheet = wb.add_sheet('Sheet 1')
             sheet.write(0, 0, 'رقم العميل')
             sheet.write(0, 1, 'عدد النقاط')
             sheet.write(0, 2, 'السبب')
             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)

    def FN_OPEN_FILE(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName( self, "QFileDialog.getOpenFileName()", "",
                                                   " Files (*.xlsx)", options=options )
        self.LE_fileName.setText(self.fileName)
        #print(self.fileName)
    def FN_SAVE_UPLOAD(self):

        if self.fileName !='':
            self.LE_fileName.setText(self.fileName)
            wb = xlrd.open_workbook( self.fileName )
            sheet = wb.sheet_by_index( 0 )
            conn = db1.connect()
            mycursor = conn.cursor()
            errorMsg =''
            createdCust =0
            nonCreatedCust=0
            #print (sheet.nrows)
            error_message = ''
            for i in range( sheet.nrows ):
                error = 0
                try:

                    self.name = sheet.cell_value( i, 0 )
                    error_message = error_message + " \n username " + self.name
                    self.custGroup = int(sheet.cell_value( i, 1 ))
                    self.loyalityType = int(sheet.cell_value( i, 2 ))
                    self.phone = int(sheet.cell_value( i, 3))
                    self.mobile = sheet.cell_value( i, 4)
                    self.job = sheet.cell_value( i, 5)
                    self.address = sheet.cell_value( i, 6)
                    self.city = int(sheet.cell_value( i, 7 ))
                    self.district = int(sheet.cell_value( i, 8 ))
                    self.building = int(sheet.cell_value( i, 9 ))
                    self.floor = int(sheet.cell_value( i, 10 ))
                    self.email = sheet.cell_value( i, 11 )
                    self.company = sheet.cell_value( i, 12 )
                    self.workPhone = int(sheet.cell_value( i, 13 ))
                    self.workAddress = sheet.cell_value( i, 14 )
                    self.status = int (sheet.cell_value( i, 15 ) )
                    self.notes = sheet.cell_value( i, 16 )
                    nationalID = sheet.cell_value(i, 17)
                    #QtWidgets.QMessageBox.warning(self, "خطأ", "Please select the row you want to modify ")
                    if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.city == '' or self.district == '' or self.building == '' \
                            or self.email == '' or nationalID =='':

                        error = 1
                        error_message= error_message + " user has an empty fields"

                    ret = CL_validation.FN_validation_mobile(str(self.mobile))
                    if ret == 3:

                        error_message = error_message + "رقم الموبايل يجب أن يكون 11 رقم"

                        error = 1
                    elif ret == 2:
                        error_message = error_message + " رقم الموبايل يجب أن يبدأ ب 01"

                        error = 1

                    ret = CL_validation.FN_validation_int(str(self.phone))
                    if ret == False:
                        error_message = error_message + " , صحيح غير الهاتف رقم "

                        error = 1
                    ret = CL_validation.FN_validation_int(nationalID)
                    if ret == False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "رقم البطاقه غير صحيح")
                        error = 1
                    ret = CL_validation.FN_valedation_mail(self.email)
                    if ret == False:
                        error_message = error_message +  "  إيميل غير صحسح"
                        error = 1

                    if error != 1:
                        sql0 = "  LOCK  TABLES    Hyper1_Retail.POS_CUSTOMER   WRITE "
                        mycursor.execute(sql0)

                        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
                        sql = "INSERT INTO Hyper1_Retail.POS_CUSTOMER( LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                              " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                              "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                              "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS,`POSC_NATIONAL_ID`) " \
                              "         VALUES (%s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                              "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s,%s)"

                        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                        val = ( self.loyalityType, self.custGroup, self.name, str(self.phone), self.mobile,
                               self.job, self.address, str(self.city), str(self.district), str(self.building), self.floor, self.email,
                               CL_userModule.user_name, creationDate, ' ', self.company, self.workPhone, self.workAddress,
                               self.notes, self.status,nationalID
                               )
                        #print(val)
                        mycursor.execute( sql, val )
                        createdCust=createdCust+1
                        sql00 = "  UNLOCK   tables    "
                        mycursor.execute(sql00)

                        db1.connectionCommit( conn )
                    else:
                        nonCreatedCust = nonCreatedCust + 1
                    #     self.msgBox1.setText(error_message)
                    #     self.msgBox1.show()

                except Exception as err:
                     print(err)
            mycursor.close()
            self.msgBox = QMessageBox()

            # Set the various texts
            self.msgBox.setWindowTitle( "Information" )
            self.msgBox.setStandardButtons( QMessageBox.Ok)
            self.msgBox.setText(error_message+ "\n No of created Cust '"+str(createdCust) +"'  No of non created Cust '"+str(nonCreatedCust)+"'")
            self.msgBox.show()
            self.close()
        #Extracting number of rows
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار الملف")
    def FN_VALIDATE_CUST(self,id ):

            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()

            if mycursor11.rowcount > 0:
                mycursor11.close()
                return True
            else:
                mycursor11.close()
                return False

    def FN_SAVE_UPLOAD1(self):
        if len (self.CMB_branch.currentData())<=0 or len (self.CMB_redeemType.currentData()) <= 0:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يجب إختيار الفرع و نوع الإسترجاع ")
        elif self.fileName !='':
            self.LE_fileName.setText(self.fileName)
            wb = xlrd.open_workbook( self.fileName )
            sheet = wb.sheet_by_index( 0 )
            conn = db1.connect()
            mycursor = conn.cursor()
            error = 0
            error1 = 0
            for i in range(sheet.nrows):
                try:
                    cust = sheet.cell_value(i, 0)
                    pts = sheet.cell_value(i, 1)

                    cust = int(cust)
                    ret = self.FN_VALIDATE_CUST(cust)
                    if cust == '' or pts == '':
                        error = 1
                        break
                    if ret == False:
                        error1 = 1
                        break
                except Exception as err:
                     print(err)

            if error == 0 and error1 ==0 :
                # lock tables
                sql0 = "  LOCK  TABLES    Hyper1_Retail.POS_CUSTOMER_POINT   WRITE , " \
                       "    Hyper1_Retail.LOYALITY_POINTS_TRANSACTION_LOG   WRITE  "

                mycursor.execute(sql0)
                for i in range( sheet.nrows ):

                    try:
                        cust = sheet.cell_value( i, 0 )
                        pts = sheet.cell_value(i, 1)

                        reason     = sheet.cell_value(i, 2)
                        #branch = sheet.cell_value(i, 3)
                        cust = int(cust)
                        pts = int(pts)
                        sql = "select POSC_POINTS_AFTER from Hyper1_Retail.POS_CUSTOMER_POINT where POSC_CUSTOMER_ID = '"+str(cust)+"'"
                        mycursor.execute(sql)
                        result = mycursor.fetchone()
                        before_points = int(result[0])
                        after_points = before_points+pts
                        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

                        sql= "INSERT INTO `Hyper1_Retail`.`LOYALITY_POINTS_TRANSACTION_LOG` " \
                             "(`POSC_CUST_ID`,`REDEEM_TYPE_ID`,`COMPANY_ID`,`BRANCH_NO`,`TRANS_CREATED_BY`," \
                             "`TRANS_CREATED_ON`,`POSC_POINTS_BEFORE`,`VALUE_OF_POINTS`,`TRANS_POINTS_QTY`,`TRANS_POINTS_VALUE`,`TRANS_REASON`,`POSC_POINTS_AFTER`,`TRANS_STATUS`)" \
                             "                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                        val=(cust,self.CMB_redeemType.currentData(),'1',self.CMB_branch.currentData(),CL_userModule.user_name,creationDate,before_points,1,pts,1,reason,after_points,'2')
                        mycursor.execute(sql, val)
                        db1.connectionCommit(conn)
                        mycursor.execute("SELECT max(cast(`MEMBERSHIP_POINTS_TRANS`  AS UNSIGNED)) FROM LOYALITY_POINTS_TRANSACTION_LOG")
                        myresult = mycursor.fetchone()
                        MEMBERSHIP_POINTS_TRANS = myresult[0]
                        sql = "update Hyper1_Retail.POS_CUSTOMER_POINT set POSC_POINTS_BEFORE =%s ,POSC_POINTS_AFTER=%s , POINTS_CHANGED_ON =%s , TRANS_SIGN = '0'" \
                              ",MEMBERSHIP_POINTS_TRANS = %s , TRANS_POINTS = %s where POSC_CUSTOMER_ID = %s"
                        val = (before_points, after_points, creationDate,MEMBERSHIP_POINTS_TRANS, pts,str(cust))
                        mycursor.execute(sql, val)
                        db1.connectionCommit(conn)
                    except Exception as err:
                         print(err)

                sql00 = "  UNLOCK   tables    "
                mycursor.execute(sql00)
                db1.connectionCommit(conn)
                QtWidgets.QMessageBox.information(self, "تم", "تم رفع نقاط العملاء")
            elif error == 1:
                QtWidgets.QMessageBox.warning(self, "خطأ", "الملف يحتوي على بعض الخانات الفارغه")
            elif error1 == 1:
                QtWidgets.QMessageBox.warning(self, "خطأ", "الملف يحتوي على عملاء غير متواجدين")

            mycursor.close()
#            self.close()
        #Extracting number of rows
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار الملف")


#search for a customer

