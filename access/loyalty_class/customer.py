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

class CL_customer(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    def __init__(self):
        super(CL_customer, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        conn = db1.connect()


    def FN_LOAD_DISPLAY(self):
        filename = self.dirname + '/customer_display.ui'
        loadUi(filename, self)
        conn = db1.connect()
        mycursor = conn.cursor()
        self.Qbtn_search.clicked.connect(self.FN_SEARCH_CUST)
        self.Qbtn_export.clicked.connect(self.FN_SAVE_CUST)
        self.Rbtn_custNo.clicked.connect(self.onClicked)
        self.Rbtn_custTp.clicked.connect(self.onClicked)

        self.Rbtn_custPhone.clicked.connect(self.onClicked)
        self.chk_search_other.stateChanged.connect(self.onClickedCheckBox)
        self.chk_search_status.stateChanged.connect(self.onClickedCheckBox)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(1028)
        self.setFixedHeight(560)
        #check authorization
        for row_number, row_data in enumerate( CL_userModule.myList ):
           if  row_data[1] =='Display_Customer':
               if row_data[4] =='None':
                print('hh')
               else:
                   sql_select_query = "select  i.ITEM_DESC from Hyper1_Retail.SYS_FORM_ITEM  i where  ITEM_STATUS= 1 and i.item_id =%s"
                   x = (row_data[4],)
                   mycursor.execute(sql_select_query, x)
                   result = mycursor.fetchone()
                   if result[0] == 'create' :
                        self.Qbtn_create.setEnabled(True)
                        self.Qbtn_create.clicked.connect(self.FN_CR_CUST)
                   elif result[0] == 'modify':
                         self.Qbtn_modify.setEnabled(True)
                         self.Qbtn_modify.clicked.connect(self.FN_MD_CUST)
                   elif result[0] == 'upload':
                         self.Qbtn_upload.setEnabled(True)
                         self.Qbtn_upload.clicked.connect(self.FN_UP_CUST)

    def FN_LOAD_MODIFY(self, id):
        print("id is ", id)
        filename = self.dirname + '/modifyCustomer.ui'
        loadUi(filename, self)

        self.FN_GET_CITIES()
        self.FN_GET_DISTRICTS()
        self.FN_GET_CUST(id)
        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()

        self.CMB_city.currentIndexChanged.connect(self.FN_GET_DISTRICT)
        self.BTN_modifyCustomer.clicked.connect(self.FN_MODIFY_CUST)
        self.CMB_status.addItems(["Active", "Inactive"])
        self.setFixedWidth(1001)
        self.setFixedHeight(648)
    def FN_LOAD_UPLOAD(self):

        filename = self.dirname + '/uploadCustomers.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
        self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD)
        self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP)
        self.fileName = ''

        self.setFixedWidth(576)
        self.setFixedHeight(178)
    def FN_LOAD_UPLOAD_PT(self):

        filename = self.dirname + '/uploadCustPt.ui'
        loadUi(filename, self)
        self.BTN_browse.clicked.connect(self.FN_OPEN_FILE)
        self.BTN_load.clicked.connect(self.FN_SAVE_UPLOAD1)
        self.BTN_uploadTemp.clicked.connect(self.FN_DISPLAY_TEMP1)
        self.fileName = ''
        self.setFixedWidth(576)
        self.setFixedHeight(178)
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
             sheet.write(0, 12, 'حاله العميل')


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

             # # wb.save('test11.xls')
             wb.save(str(filename[0]))
             # wb.close()
             import webbrowser
             webbrowser.open(filename[0])
         except Exception as err:
             print(err)
    def FN_GET_CUSTTP_DESC(self, id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        return myresult[0]

    def FN_GET_STATUS_DESC(self,id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"



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
                    self.phone = sheet.cell_value( i, 3)
                    self.mobile = sheet.cell_value( i, 4)
                    self.job = sheet.cell_value( i, 5)
                    self.address = sheet.cell_value( i, 6)
                    self.city = sheet.cell_value( i, 7 )
                    self.district = sheet.cell_value( i, 8 )
                    self.building = sheet.cell_value( i, 9 )
                    self.floor = int(sheet.cell_value( i, 10 ))
                    self.email = sheet.cell_value( i, 11 )
                    self.company = sheet.cell_value( i, 12 )
                    self.workPhone = int(sheet.cell_value( i, 13 ))
                    self.workAddress = sheet.cell_value( i, 14 )
                    self.status = int (sheet.cell_value( i, 15 ) )
                    self.notes = sheet.cell_value( i, 16 )

                    #QtWidgets.QMessageBox.warning(self, "Error", "Please select the row you want to modify ")
                    if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.city == '' or self.district == '' or self.building == '' \
                            or self.email == '':

                        error = 1
                        error_message= error_message + " user has an empty fields"

                    ret = CL_validation.FN_validation_mobile(self.mobile)
                    if ret == 3:

                        error_message = error_message + " has Invalid mobile no ,len must be = 11"

                        error = 1
                    elif ret == 2:
                        error_message = error_message + ", has Invalid mobile no,no must start with '01'"

                        error = 1

                    ret = CL_validation.FN_validation_int(self.phone)
                    if ret == False:
                        error_message = error_message + " , has Invalid phone number"

                        error = 1

                    # ret = CL_validation.FN_validation_int(self.workPhone)
                    # if ret == False:
                    #     error_message = error_message + " ,has Invalid work Phone"
                    #
                    #     error = 1

                    ret = CL_validation.FN_valedation_mail(self.email)
                    if ret == False:
                        error_message = error_message + " ,has Invalid email"

                        error = 1


                    if error != 1:
                    # get max userid
                        mycursor.execute( "SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM Hyper1_Retail.POS_CUSTOMER" )
                        myresult = mycursor.fetchone()

                        if myresult[0] == None:
                            self.id = "1"
                        else:
                            self.id = int( myresult[0] ) + 1

                        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
                        sql = "INSERT INTO Hyper1_Retail.POS_CUSTOMER(POSC_CUST_ID, LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                              " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                              "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                              "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS) " \
                              "         VALUES ( %s, %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                              "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s)"

                        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                        val = (self.id, self.loyalityType, self.custGroup, self.name, self.phone, self.mobile,
                               self.job, self.address, self.city, self.district, self.building, self.floor, self.email,
                               CL_userModule.user_name, creationDate, ' ', self.company, self.workPhone, self.workAddress,
                               self.notes, self.status
                               )
                        #print(val)
                        mycursor.execute( sql, val )
                        createdCust=createdCust+1
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
            QtWidgets.QMessageBox.warning(self, "Error", "Choose a file")
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

        if self.fileName !='':
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
                for i in range( sheet.nrows ):

                    try:
                        cust = sheet.cell_value( i, 0 )
                        pts = sheet.cell_value(i, 1)
                        cust = int(cust)
                        pts = int(pts)
                        sql = "select POSC_POINTS_AFTER from Hyper1_Retail.POS_CUSTOMER_POINT where POSC_CUSTOMER_ID = '"+str(cust)+"'"
                        mycursor.execute(sql)
                        result = mycursor.fetchone()
                        before_points = int(result[0])

                        creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
                        sql = "update Hyper1_Retail.POS_CUSTOMER_POINT set POSC_POINTS_BEFORE =%s ,POSC_POINTS_AFTER=%s , POINTS_CHANGED_ON =%s , TRANS_SIGN = '0' where POSC_CUSTOMER_ID = %s"
                        val = (before_points, pts, creationDate, str(cust))
                        mycursor.execute(sql, val)
                        db1.connectionCommit(conn)
                        QtWidgets.QMessageBox.warning(self, "Done", "customer points are updated")

                        mycursor.execute( sql, val )
                        db1.connectionCommit( conn )
                    except Exception as err:
                         print(err)
            elif error == 1:
                QtWidgets.QMessageBox.warning(self, "Error", "Sheet contain empty fields")
            elif error1 == 1:
                QtWidgets.QMessageBox.warning(self, "Error", "Sheet contain invalid customers")

            mycursor.close()
#            self.close()
        #Extracting number of rows
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Choose a file")
    def FN_GET_CUST(self,id):
        #self.FN_GET_CustID()
        #self.id = self.LB_custID.text()
        self.LB_custID.setText(id)
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "select * from Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = %s "
        x = (id,)
        mycursor.execute( sql_select_query, x )
        record = mycursor.fetchone()
        #print( record )
        self.LE_name.setText(record[3])
        self.lE_phone.setText( record[4] )
        self.lE_mobile.setText( record[5] )
        self.LE_job.setText( record[6] )
        self.LE_address.setText( record[7] )
        self.CMB_city.setCurrentText( record[8] )
        self.CMB_district.setCurrentText( record[9] )
        self.LE_building.setText( record[10] )
        self.LE_floor.setText( record[11] )
        self.LE_email.setText( record[12] )
        self.LE_company.setText( record[17] )
        self.LE_workPhone.setText( record[18] )
        self.LE_workAddress.setText( record[19] )
        self.LE_notes.setText( record[20] )
        if record[21] == '1':
            self.CMB_status.setCurrentText('Active')
        else:
            self.CMB_status.setCurrentText( 'Inactive' )

        self.CMB_custGroup.setCurrentText( record[2] )
        self.CMB_loyalityType.setCurrentText( record[1] )
        mycursor.close()

    def FN_CR_CUST(self,funct):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()


    def FN_MD_CUST(self, funct):

        self.window_two = CL_customer()
        #get first selected row
        try:
            rowNo=self.Qtable_customer.selectedItems()[0].row()
            if rowNo >0 :
                id =self.Qtable_customer.item(rowNo, 0).text()
                self.window_two.FN_LOAD_MODIFY(id)
                self.window_two.show()
        except Exception as err:
            print(err)
            #QtWidgets.QMessageBox.warning(self, "Error", "Please select the row you want to modify ")

            #else:



    def FN_UP_CUST(self, funct):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_UPLOAD()
        self.window_two.show()

    # def FN_UP_CUST_PT(self, funct):
    #     self.window_two = CL_customer()
    #     self.window_two.FN_LOAD_UPLOAD_PT()
    #     self.window_two.show()


    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createCustomer.ui'
        loadUi( filename, self )
        self.FN_GET_CUSTGP()
        self.FN_GET_CUSTTP()
        self.FN_GET_CITIES()
        #self.FN_GET_DISTRICTS()
        self.FN_GET_DISTRICT()
        self.CMB_city.currentIndexChanged.connect( self.FN_GET_DISTRICT )
        self.CMB_status.addItems( ["Active", "Inactive"] )
        self.BTN_createCustomer.clicked.connect(self.FN_CREATE_CUST)

        self.setFixedWidth(1034)
        self.setFixedHeight(651)
    def FN_GET_CITIES(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CITY_NAME FROM Hyper1_Retail.City  where CITY_STATUS = 1 order by CITY_ID asc")
        records = mycursor.fetchall()

        for row in records:
            self.CMB_city.addItems([row[0]])
        mycursor.close()
    def FN_GET_DISTRICT(self):
        self.CMB_district.clear()
        if self.CMB_city.currentText() !=None:
            conn = db1.connect()
            mycursor = conn.cursor()
            mycursor.execute("SELECT DISTRICT_NAME FROM Hyper1_Retail.DISTRICT d inner join Hyper1_Retail.City c on d.CITY_ID = c.CITY_ID where CITY_NAME = '"+self.CMB_city.currentText()+"' and DISTRICT_STATUS = 1  order by DISTRICT_ID asc")
            records = mycursor.fetchall()

            for row in records:
                self.CMB_district.addItems([row[0]])
            mycursor.close()

    def FN_GET_DISTRICTS(self):
        self.CMB_district.clear()
        if self.CMB_city.currentText() != None:
            conn = db1.connect()
            mycursor = conn.cursor()
            mycursor.execute(
                "SELECT DISTRICT_NAME FROM Hyper1_Retail.DISTRICT d where DISTRICT_STATUS = 1  order by DISTRICT_ID asc")
            records = mycursor.fetchall()

            for row in records:
                self.CMB_district.addItems([row[0]])
            mycursor.close()
#fill the combo box of customer group
    def FN_GET_CUSTGP(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT CG_DESC FROM Hyper1_Retail.CUSTOMER_GROUP order by CG_GROUP_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.CMB_custGroup.addItems( [row[0]] )

    # fill the combo box of customer type
    def FN_GET_CUSTTP(self):
        self.CMB_loyalityType.clear()
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE order by LOYCT_TYPE_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        for row in records:
            self.CMB_loyalityType.addItems( [row[0]] )

    # return customer tye id
    def FN_GET_CUSTTP_ID(self,desc):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+desc+"'" )
        records = mycursor.fetchone()
        mycursor.close()
        return records[0]

    def onClickedCheckBox(self):
        if self.chk_search_other.isChecked():
            # self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custNo.setChecked(True)

            self.Rbtn_custNo.setEnabled(True)
            self.Rbtn_custTp.setEnabled(True)
            self.Rbtn_custPhone.setEnabled(True)
            self.LE_custNo.setEnabled(True)
            self.LE_custPhone.setEnabled(True)
            self.CMB_loyalityType.setEnabled(True)
        else:
            self.Rbtn_custNo.setChecked(False)
            self.Rbtn_custTp.setChecked(False)
            self.Rbtn_custPhone.setChecked(False)

            self.Rbtn_custNo.setEnabled(False)
            self.Rbtn_custTp.setEnabled(False)
            self.Rbtn_custPhone.setEnabled(False)
            self.LE_custNo.setEnabled(False)
            self.LE_custPhone.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setText('')
            self.CMB_loyalityType.setEnabled(False)

        if self.chk_search_status.isChecked():

            # self.LE_custNo.setEnabled(False)
            self.Rbtn_stsAll.setChecked(True)
            self.Rbtn_stsActive.setEnabled(True)
            self.Rbtn_stsInactive.setEnabled(True)
            self.Rbtn_stsAll.setEnabled(True)
        else:
            self.Rbtn_stsAll.setChecked(False)
            self.Rbtn_stsActive.setEnabled(False)
            self.Rbtn_stsInactive.setEnabled(False)
            self.Rbtn_stsAll.setEnabled(False)

    def onClicked(self):

        if self.Rbtn_custTp.isChecked():
            self.FN_GET_CUSTTP()
            self.CMB_loyalityType.setEnabled(True)
            self.LE_custNo.setEnabled(False)
            self.LE_custNo.setText('')
            self.LE_custPhone.setEnabled(False)
        elif self.Rbtn_custNo.isChecked():
            self.CMB_loyalityType.setEnabled(False)
            self.LE_custNo.setEnabled(True)

            self.LE_custPhone.setEnabled(False)
            self.LE_custPhone.setText('')
        elif self.Rbtn_custPhone.isChecked():
            self.CMB_loyalityType.setEnabled(False)
            self.LE_custNo.setEnabled(False)
            self.LE_custNo.setText('')

            self.LE_custPhone.setEnabled(True)
    def FN_VALIDATE_FIELDS(self):

        self.name = self.LE_name.text().strip()

        self.phone = self.lE_phone.text().strip()
        self.mobile = self.lE_mobile.text().strip()


        self.building = self.LE_building.text().strip()
        self.floor = self.LE_floor.text().strip()
        self.email = self.LE_email.text().strip()
        self.company = self.LE_company.text().strip()
        self.workPhone = self.LE_workPhone.text().strip()
        self.workAddress = self.LE_workAddress.text().strip()

        error = 0
        if self.name == '' or self.mobile == '' or self.job == '' or self.address == '' or self.building == '' \
                or self.floor == '' or self.email == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter all required fields")
            error = 1
            return error
        ret = CL_validation.FN_validation_int(self.phone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid phone number")
            error = 1

        ret = CL_validation.FN_validation_mobile(self.mobile)
        if ret == 3:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid mobile n0,len must be = 11")
            error = 1
        elif ret == 2:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid mobile no,no must start with '01'")
            error = 1

        ret = self.FN_CHECK_REPEATED_MOBILE(self.mobile)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "Error", "Repeated Mobile no ")
            error = 1

        ret = CL_validation.FN_validation_int(self.workPhone)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid work Phone")
            error = 1
        ret = CL_validation.FN_validation_int(self.building)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid building number")
            error = 1

        ret = CL_validation.FN_validation_int(self.floor)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid floor Phone")
            error = 1

        ret = CL_validation.FN_valedation_mail(self.email)
        if ret == False:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid email")
            error = 1
        return error
    def FN_CHECK_REPEATED_MOBILE(self,mobile):
       try:
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max id
            mycursor.execute("SELECT POSC_MOBILE FROM Hyper1_Retail.POS_CUSTOMER where POSC_MOBILE ='"+mobile+"'")
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                return True
            else:
                return False

       except Exception as err:
             print(err)
    def FN_CREATE_CUST(self):
        #get customer data
        try:
            self.name = self.LE_name.text().strip()
            self.custGroup = self.CMB_custGroup.currentText()
            self.loyalityType =self.CMB_loyalityType.currentText()
            self.phone = self.lE_phone .text().strip()
            self.mobile = self.lE_mobile.text().strip()
            self.job = self.LE_job.text().strip()
            self.address = self.LE_address.text().strip()
            self.city = self.CMB_city.currentText()
            self.district = self.CMB_district.currentText()
            self.building = self.LE_building.text().strip()
            self.floor = self.LE_floor.text().strip()
            self.email = self.LE_email.text().strip()
            self.company = self.LE_company.text().strip()
            self.workPhone =  self.LE_workPhone.text().strip()
            self.workAddress = self.LE_workAddress.text().strip()
            self.status = self.CMB_status.currentText()
            self.notes = self.LE_notes.toPlainText().strip()
            conn = db1.connect()
            mycursor = conn.cursor()
            # get max id
            mycursor.execute( "SELECT max(cast(POSC_CUST_ID  AS UNSIGNED)) FROM Hyper1_Retail.POS_CUSTOMER" )
            myresult = mycursor.fetchone()

            if myresult[0] == None:
                self.id = "1"
            else:
                self.id = int( myresult[0] ) + 1

            creationDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )

            #get customer gp id
            mycursor.execute( "SELECT CG_GROUP_ID FROM Hyper1_Retail.CUSTOMER_GROUP where CG_DESC = '"+self.custGroup+"'" )
            myresult = mycursor.fetchone()
            self.custGroup = myresult[0]

            #get customer type
            mycursor.execute( "SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '"+self.loyalityType +"'" )
            myresult = mycursor.fetchone()
            self.loyalityType = myresult[0]

            self.status = self.CMB_status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0

            error =0
            error = self.FN_VALIDATE_FIELDS()

            if error !=1:

                sql = "INSERT INTO Hyper1_Retail.POS_CUSTOMER(POSC_CUST_ID, LOYCT_TYPE_ID, CG_GROUP_ID, POSC_NAME, POSC_PHONE," \
                      " POSC_MOBILE, POSC_JOB, POSC_ADDRESS, POSC_CITY, POSC_DISTICT, POSC_BUILDING,POSC_FLOOR, POSC_EMAIL, " \
                      "POSC_CREATED_BY, POSC_CREATED_ON ,POSC_CHANGED_BY ,  POSC_COMPANY, " \
                      "POSC_WORK_PHONE, POSC_WORK_ADDRESS, POSC_NOTES, POSC_STATUS) " \
                      "         VALUES ( %s, %s, %s,  %s,%s,%s, %s, %s, %s, %s, " \
                      "%s,%s,  %s, %s,%s, %s,%s, %s, %s, %s,%s)"

                           # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                val = (self.id,self.loyalityType,self.custGroup,self.name,self.phone,self.mobile,
                       self.job, self.address, self.city, self.district, self.building, self.floor ,self.email,
                       CL_userModule.user_name, creationDate, ' ',self.company, self.workPhone, self.workAddress,
                       self.notes, self.status
                )
                mycursor.execute( sql, val )
                # mycursor.execute(sql)

                mycursor.close()

                print( mycursor.rowcount, "record inserted." )
                db1.connectionCommit( conn )
                #db1.connectionClose( self.conn )
                QtWidgets.QMessageBox.information(self, "Success", "Customer is created successfully")

                self.close()

                print("in create cust" ,self.name)
        except Exception as err:
            print(err)


    def FN_MODIFY_CUST(self):
        try:
            self.id = self.LB_custID.text().strip()
            self.name = self.LE_name.text().strip()
            self.custGroup = self.CMB_custGroup.currentText()
            self.loyalityType = self.CMB_loyalityType.currentText()
            self.phone = self.lE_phone.text().strip()
            self.mobile = self.lE_mobile.text().strip()
            self.job = self.LE_job.text().strip()
            self.address = self.LE_address.text().strip()
            self.city = self.CMB_city.currentText()
            self.district = self.CMB_district.currentText()
            self.building = self.LE_building.text().strip()
            self.floor = self.LE_floor.text().strip()
            self.email = self.LE_email.text().strip()
            self.company = self.LE_company.text().strip()
            self.workPhone = self.LE_workPhone.text().strip()
            self.workAddress = self.LE_workAddress.text().strip()
            self.status = self.CMB_status.currentText()
            self.notes = self.LE_notes.toPlainText().strip()

            conn = db1.connect()
            mycursor = conn.cursor()

            changeDate = str( datetime.today().strftime( '%Y-%m-%d-%H:%M-%S' ) )
            # get customer gp id
            mycursor.execute( "SELECT CG_GROUP_ID FROM Hyper1_Retail.CUSTOMER_GROUP where CG_DESC = '" + self.custGroup + "'" )
            myresult = mycursor.fetchone()
            self.custGroup = myresult[0]

            # get customer type
            mycursor.execute(
                "SELECT LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_DESC = '" + self.loyalityType + "'" )
            myresult = mycursor.fetchone()
            self.loyalityType = myresult[0]

            self.status = self.CMB_status.currentText()
            if self.status == 'Active':
                self.status = 1
            else:
                self.status = 0
            error = 0
            error = self.FN_VALIDATE_FIELDS()

            if error != 1:


                sql = "update  Hyper1_Retail.POS_CUSTOMER  set  LOYCT_TYPE_ID=%s, CG_GROUP_ID=%s,  POSC_NAME = %s , POSC_PHONE=%s," \
                      " POSC_MOBILE=%s, POSC_JOB=%s, POSC_ADDRESS=%s, POSC_CITY=%s, POSC_DISTICT=%s, POSC_BUILDING=%s,POSC_FLOOR=%s, POSC_EMAIL=%s, " \
                      "POSC_CHANGED_BY =%s, POSC_CHANGED_ON =%s, POSC_COMPANY=%s, " \
                      "POSC_WORK_PHONE=%s, POSC_WORK_ADDRESS=%s, POSC_NOTES=%s, POSC_STATUS=%s where POSC_CUST_ID = %s"

                # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
                val = ( self.loyalityType, self.custGroup, self.name, self.phone, self.mobile,
                       self.job, self.address, self.city, self.district, self.building, self.floor ,self.email,
                       CL_userModule.user_name, changeDate,  self.company, self.workPhone, self.workAddress,
                       self.notes, self.status ,self.id  )
                mycursor.execute( sql, val )
                # mycursor.execute(sql)

                mycursor.close()

                print( mycursor.rowcount, "record updated." )
                QtWidgets.QMessageBox.information(self, "Success", "Customer is modified successfully")

                db1.connectionCommit( conn )
                #db1.connectionClose( self.conn )
               # self.FN_INSERT_IN_LOG(tableName,)
                self.close()
        except Exception as err:
            print(err)


   # def FN_INSERT_IN_LOG(tableName,fieldName,value):
       # try:
       #     conn = db1.connect()
        #    mycursor = conn.cursor()

        #    changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
       # except Exception as err:
         #   print(err)



# export to a file

    def FN_SAVE_CUST(self):
        try:
            filename = QFileDialog.getSaveFileName(self, "Save File", '', "(*.xls)")
            print(filename)

            wb = xlwt.Workbook()

            # add_sheet is used to create sheet.
            sheet = wb.add_sheet('Sheet 1')
            sheet.write(0, 0, 'رقم العميل')
            sheet.write(0, 1, 'اسم العميل')
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
            sheet.write(0, 12, 'حاله العميل')

            rowNo= self.Qtable_customer.rowCount()+1

            for currentColumn in range(self.Qtable_customer.columnCount()):
                for currentRow in range(self.Qtable_customer.rowCount()):
                    teext = str(self.Qtable_customer.item(currentRow, currentColumn).text())
                    sheet.write(currentRow+1, currentColumn, teext)
            # # wb.save('test11.xls')
            wb.save(str(filename[0]))
            # wb.close()
            import webbrowser
            webbrowser.open(filename[0])
        except Exception as err:
            print(err)

#search for a customer
    def FN_SEARCH_CUST(self):
        # print('in search')
        # self.Qtable_customer.clearcontents()
        self.Qbtn_search.setEnabled(False)
        for i in reversed(range(self.Qtable_customer.rowCount())):
            self.Qtable_customer.removeRow(i)
        conn = db1.connect()
        mycursor = conn.cursor()
        whereClause = ""
        if self.chk_search_other.isChecked():
            if self.Rbtn_custNo.isChecked():
                id = self.LE_custNo.text()
                whereClause = " POSC_CUST_ID = '" + id + "'"

            elif self.Rbtn_custTp.isChecked():
                type = self.CMB_loyalityType.currentText()
                whereClause = " LOYCT_TYPE_ID ='" + self.FN_GET_CUSTTP_ID(type) + "'"

            elif self.Rbtn_custPhone.isChecked():
                phone = self.LE_custPhone.text()
                whereClause = " POSC_PHONE = '" + phone + "'"

        if self.chk_search_status.isChecked():
            if self.Rbtn_stsActive.isChecked():
                if whereClause != '':
                    whereClause = whereClause + ' and '
                whereClause = whereClause + 'POSC_STATUS = 1'
            elif self.Rbtn_stsInactive.isChecked():
                if whereClause != '':
                    whereClause = whereClause + ' and '
                whereClause = whereClause + 'POSC_STATUS = 0'
            elif self.Rbtn_stsAll.isChecked():
                if whereClause != '':
                    whereClause = whereClause + ' and '
                whereClause = whereClause + 'POSC_STATUS in ( 0,1)'
        if self.chk_search_status.isChecked() == False and self.chk_search_other.isChecked() == False:
            QtWidgets.QMessageBox.warning(self, "Error", "أختر أي من محدادات البحث")
        else:
            # print(whereClause)
            sql_select_query = "select  POSC_CUST_ID ,POSC_NAME,LOYCT_TYPE_ID,POSC_PHONE, POSC_MOBILE,POSC_JOB,    POSC_ADDRESS,POSC_CITY,POSC_DISTICT,POSC_BUILDING,POSC_FLOOR,POSC_EMAIL,POSC_STATUS from Hyper1_Retail.POS_CUSTOMER where " + whereClause
            print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable_customer.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    if column_number == 12:
                        data = self.FN_GET_STATUS_DESC(str(data))

                    elif column_number == 2:
                        data = self.FN_GET_CUSTTP_DESC(str(data))
                    self.Qtable_customer.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.Qtable_customer.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            mycursor.close()
        self.Qbtn_search.setEnabled(True)


