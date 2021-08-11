from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from access.utils.util import *
from datetime import datetime


class CL_branch(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(CL_branch, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/master_data_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()


    def FN_LOAD_DISPlAY(self):
        filename = self.dirname + '/branch.ui'
        loadUi(filename, self)

        self.FN_GET_ALL()
        try:
            self.CMB_status.addItems(["Active", "Inactive"])
            self.LB_status.setText('1')
            self.CMB_status.activated.connect(self.FN_GET_STATUS)
            self.BTN_create.clicked.connect(self.FN_CREATE)
            self.BTN_modify.clicked.connect(self.FN_MODIFY)
            self.BTN_search.clicked.connect(self.FN_SEARCH)
            self.BTN_search_all.clicked.connect(self.FN_GET_ALL)

            records = util.FN_GET_CITIES()
            for row, val in records:
                self.CMB_city.addItem(row, val)

            records = util.FN_GET_COMPANIES()
            for row, val in records:
                self.CMB_company.addItem(row, val)
            self.Qtable.doubleClicked.connect(self.FN_GET_ONE)
            css_path = Path(__file__).parent.parent.parent
            path = css_path.__str__() + '/presentation/Themes/Style.css'
            self.setStyleSheet(open(path).read())

        except Exception as err:
            print(err)

    def FN_SEARCH(self):
        self.conn1 = db1.connect()
        try:
            for i in reversed(range(self.Qtable.rowCount())):
                self.Qtable.removeRow(i)

            mycursor = self.conn1.cursor()
            name = self.LE_desc.text().strip()
            status = self.CMB_status.currentText()
            if status == 'Active':

                whereClause = "where `BRANCH_STATUS` = 1  "
            else:
                whereClause = "where `BRANCH_STATUS` = 0 "

            if name != '' :
                whereClause = whereClause + "and `BRANCH_DESC_A` like '%" + str(name) + "%'"

            sql_select_query = "select  `COMPANY_ID`,    `BRANCH_NO`,    `BRANCH_DESC_A`,    `BRANCH_DESC_E`,    `BRANCH_ADDRESS`,    `BRANCH_CITY`,    `BRANCH_TEL1`,    `BRANCH_TEL2`,    `BRANCH_FAX`,    `BRANCH_EMAIL`,    `BRANCH_NOTES`,      `BRANCH_CURRENCY`,    `BRANCH_STATUS` from Hyper1_Retail.BRANCH " + whereClause + "  order by BRANCH_NO asc"
            #print(sql_select_query)
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable.insertRow(row_number)

                for column_number, data in enumerate(row_data):

                    if column_number == 12 :
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    elif column_number == 5:
                        data = util.FN_GET_CITY_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    elif column_number == 0:
                        data = util.FN_GET_COMP_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    else:
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable.setItem(row_number, column_number, item)

        except Exception as err:
             print(err)

    def FN_GET_ALL(self):
        self.conn = db1.connect()
        try:
            for i in reversed(range(self.Qtable.rowCount())):
                self.Qtable.removeRow(i)

            mycursor = self.conn.cursor()
            mycursor.execute("SELECT  `COMPANY_ID`,    `BRANCH_NO`,    `BRANCH_DESC_A`,    `BRANCH_DESC_E`,    `BRANCH_ADDRESS`,    `BRANCH_CITY`,    `BRANCH_TEL1`,    `BRANCH_TEL2`,    `BRANCH_FAX`,    `BRANCH_EMAIL`,    `BRANCH_NOTES`,      `BRANCH_CURRENCY`,    `BRANCH_STATUS`  FROM Hyper1_Retail.BRANCH   order by BRANCH_NO    asc")
            records = mycursor.fetchall()

            for row_number, row_data in enumerate(records):
                self.Qtable.insertRow(row_number)
                for column_number, data in enumerate(row_data):

                    if column_number == 12:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    elif column_number == 5:
                        data = util.FN_GET_CITY_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    elif column_number == 0:
                        data = util.FN_GET_COMP_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    else:
                        item = QTableWidgetItem(str(data))
                    item.setFlags(QtCore.Qt.ItemFlags(~QtCore.Qt.ItemIsEditable))
                    self.Qtable.setItem(row_number, column_number, item)

        except Exception as err:
            print(err)

    def FN_GET_ONE(self):
        try:
            if len(self.Qtable.selectedIndexes()) >= 0:
                rowNo = self.Qtable.selectedItems()[0].row()
                branchNo = self.Qtable.item(rowNo, 1).text()
                company = self.Qtable.item(rowNo, 0).text()
                name = self.Qtable.item(rowNo, 2).text()
                nameEn = self.Qtable.item(rowNo, 3).text()
                address = self.Qtable.item(rowNo, 4).text()
                city = self.Qtable.item(rowNo, 5).text()

                phone1 = self.Qtable.item(rowNo, 6).text()
                phone2 = self.Qtable.item(rowNo, 7).text()
                fax = self.Qtable.item(rowNo, 8).text()

                email = self.Qtable.item(rowNo, 9).text()
                notes = self.Qtable.item(rowNo, 10).text()
                currency = self.Qtable.item(rowNo, 11).text()
                status = self.Qtable.item(rowNo, 12).text()

                self.branchNo.setText(branchNo)
                self.CMB_company.setCurrentText(company)
                self.CMB_city.setCurrentText(city)
                self.LE_desc.setText(name)
                self.LE_desc_2.setText(nameEn)
                self.address.setText(address)
                self.phone1.setText(phone1)
                self.phone2.setText(phone2)
                self.fax.setText(fax)
                self.email.setText(email)
                self.currency.setText(currency)
                self.notes.setText(notes)
                #self.LB_id.setText(id)
                self.LB_status.setText(util.FN_GET_STATUS_id(status))
                self.CMB_status.setCurrentText(status)
                # self.FN_MODIFY_CUSTTP()
        except Exception as err:
            print(err)
    def FN_CHECK_DUP_NAME(self,name,id=''):
        self.conn1 = db1.connect()
        mycursor1 = self.conn1.cursor()
        sql = "SELECT BRANCH_DESC_A  FROM Hyper1_Retail.BRANCH where BRANCH_DESC_A = '"+name+"' and BRANCH_NO !='"+id+"'"
        mycursor1.execute(sql)
        myresult = mycursor1.fetchall()
        len = mycursor1.rowcount
        print(len)
        if len > 0:
            #mycursor1.close()
            return True
        else:
            #mycursor1.close()
            return False

    def FN_GET_STATUS(self):
        status = self.CMB_status.currentText()
        if status == 'Active'  :
            self.LB_status.setText('1')
        else :
            self.LB_status.setText('0')

    def FN_CREATE(self):
        self.conn = db1.connect()
        branchNo = self.LE_branchNo.text().strip()
        company = self.CMB_company.currentData()
        name = self.LE_desc.text().strip()
        nameEn = self.LE_desc_2.text().strip()
        city = self.CMB_city.currentData()

        phone1 = self.LE_phone1.text().strip()
        phone2 = self.LE_phone2.text().strip()
        fax = self.LE_fax.text().strip()
        address = self.LE_address.text().strip()
        email = self.LE_email.text().strip()
        currency = self.LE_currency.text().strip()
        notes = self.LE_notes.toPlainText().strip()
        status = self.CMB_status.currentText()
        if status == 'Active':
            self.status = 1
        else:
            self.status = 0

        mycursor = self.conn.cursor()

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        if name == '' :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاءادخال الاسم")

        else:
            try:
                if self.FN_CHECK_DUP_NAME(self.name) != False:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                    mycursor.close()
                else:

                    sql = "INSERT INTO Hyper1_Retail.BRANCH  VALUES ( %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s ,%s)"
                    val = (company,branchNo,name, nameEn,address,city,phone1,phone2,fax,email,notes,'',currency,status )
                    mycursor.execute(sql, val)
                    # mycursor.execute(sql)

                    mycursor.close()

                    print(mycursor.rowcount, "branch inserted.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                    db1.connectionCommit(self.conn)
                    self.FN_GET_ALL()
                    self.FN_CLEAR_FEILDS()
                    #db1.connectionClose(self.conn)
                    #self.close()
            except Exception as err:
                print(err)
        print("in create company", self.name)

        # insert into db

    def FN_MODIFY(self):
        self.conn1 = db1.connect()
        if len(self.Qtable.selectedIndexes()) >0 :
            rowNo = self.Qtable.selectedItems()[0].row()
            #id = self.LB_id.text().strip()
            name_old = self.Qtable.item(rowNo, 2).text()
            status_old =  self.Qtable.item(rowNo, 12).text()
            branchNo = self.LE_branchNo.text().strip()
            company = self.CMB_company.currentData()
            name = self.LE_desc.text().strip()
            nameEn = self.LE_desc_2.text().strip()
            city = self.CMB_city.currentData()

            phone1 = self.LE_phone1.text().strip()
            phone2 = self.LE_phone2.text().strip()
            fax = self.LE_fax.text().strip()
            address = self.LE_address.text().strip()
            email = self.LE_email.text().strip()
            currency = self.LE_currency.text().strip()
            notes = self.LE_notes.toPlainText().strip()
            status = self.CMB_status.currentText()

            error = 0
            if self.desc == '':
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")

            else:
                if name != name_old:
                    if self.FN_CHECK_DUP_NAME(name,id) != False:
                        QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                        error=1

                if error!=1:
                    mycursor = self.conn1.cursor()
                    changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                    sql = "UPDATE `Hyper1_Retail`.`BRANCH` SET `BRANCH_DESC_A` =  %s,`BRANCH_DESC_E` =  %s,`BRANCH_ADDRESS` =  %s,`BRANCH_CITY` =  %s,`BRANCH_TEL1` =  %s,`BRANCH_TEL2` =  %s,`BRANCH_FAX` = %s,`BRANCH_EMAIL` =  %s,`BRANCH_NOTES` = %s,`BRANCH_CHANGED_ON` = %s ,`BRANCH_CURRENCY` =  %s,`BRANCH_STATUS` =  %s,WHERE `COMPANY_ID` = %s  AND `BRANCH_NO` = %s"
                    val = (name, nameEn, address, city, phone1, phone2, fax, email, notes, changeDate, currency,                    status)

                    mycursor.execute(sql, val)
                    #mycursor.close()
                    #
                    print(mycursor.rowcount, "record updated.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                    db1.connectionCommit(self.conn1)
                    self.FN_GET_ALL()
                    self.FN_CLEAR_FEILDS ()
                    if str(status) != str(status_old):
                        util.FN_INSERT_IN_LOG("BRANCH", "status", status, status_old, id)
        else:
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")

    def FN_CLEAR_FEILDS (self):
        #self.LB_id.clear()
        self.LE_branchNo.clear()

        self.LE_desc.clear()
        self.LE_desc_2.clear()
        self.LE_phone1.clear()
        self.LE_phone2.clear()
        self.LE_fax.clear()
        self.LE_address.clear()
        self.LE_email.clear()
        self.LE_currency.clear()
        self.LE_notes.clear()

        self.CMB_status.setCurrentText('Active')
        self.LB_status.setText('1')
