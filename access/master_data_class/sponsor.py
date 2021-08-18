from pathlib import Path

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from access.authorization_class.user_module import CL_userModule
from access.utils.util import *
from datetime import datetime


class CL_sponsor(QtWidgets.QDialog):
    dirname = ''
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(CL_sponsor, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/master_data_ui'
        self.conn = db1.connect()
        self.conn1 = db1.connect()

    def FN_GET_SPONSORTYPE(self):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute(
            "SELECT SPONSOR_TYPE_DESC, SPONSOR_TYPE  FROM Hyper1_Retail.SPONSOR_TYPE  where STATUS = 1 order by SPONSOR_TYPE asc")
        records = mycursor.fetchall()
        mycursor.close()

        return records
    def FN_GET_SPONSORTYPEDESC(self,id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute(
            "SELECT SPONSOR_TYPE_DESC  FROM Hyper1_Retail.SPONSOR_TYPE  where  SPONSOR_TYPE = '"+id+"'")
        records = mycursor.fetchone()
        return records[0]
    def FN_GET_SPONSORTYPEID(self,desc):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute(
            "SELECT SPONSOR_TYPE  FROM Hyper1_Retail.SPONSOR_TYPE  where  SPONSOR_TYPE_DESC = '"+desc+"'")
        records = mycursor.fetchone()
        return records[0]
    def FN_LOAD_DISPlAY(self):
        try:
            filename = self.dirname + '/sponsor.ui'
            loadUi(filename, self)

            records = self.FN_GET_SPONSORTYPE()
            for row, val in records:
                self.CMB_sponsorType.addItem(str(row), val)

            self.FN_GET_ALL()

            self.CMB_status.addItem("Active", '1')
            self.CMB_status.addItem("Inactive", '0')
            self.LB_status.setText('1')
            self.CMB_status.activated.connect(self.FN_GET_STATUS)
            self.BTN_create.clicked.connect(self.FN_CREATE)
            self.BTN_modify.clicked.connect(self.FN_MODIFY)
            self.BTN_search.clicked.connect(self.FN_SEARCH)
            self.BTN_search_all.clicked.connect(self.FN_GET_ALL)


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

                whereClause = " where `SPONSOR_STATUS` = 1  "
            else:
                whereClause = " where `SPONSOR_STATUS` = 0 "

            if name != '' :
                whereClause = whereClause + " and `SPONSOR_NAME` like '%" + str(name) + "%'"

            sql_select_query = " select `SPONSOR`.`SPONSOR_ID`,`SPONSOR`.`SPONSOR_SAP_CODE`,`SPONSOR`.`SPONSOR_TYPE`,    " \
                               "`SPONSOR`.`SPONSOR_NAME`,   `SPONSOR`.`SPONSOR_CONTACT_PERSON`,     `SPONSOR`.`SPONSOR_ADDRESS`,  " \
                               "        " \
                               " `SPONSOR`.`SPONSOR_TEL`,    `SPONSOR`.`SPONSOR_FAX`,  `SPONSOR`.`SPONSOR_EMAIL`,  `SPONSOR`.`SPONSOR_STATUS` FROM `Hyper1_Retail`.`SPONSOR`" + whereClause + "  order by `SPONSOR_ID`*1 asc"
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row_number, row_data in enumerate(records):
                self.Qtable.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    if column_number == 9 :
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    elif column_number == 2:
                        data = self.FN_GET_SPONSORTYPEDESC(str(data))
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
            mycursor.execute(" select `SPONSOR`.`SPONSOR_ID`,`SPONSOR`.`SPONSOR_SAP_CODE`,`SPONSOR`.`SPONSOR_TYPE`,    " \
                               "`SPONSOR`.`SPONSOR_NAME`,   `SPONSOR`.`SPONSOR_CONTACT_PERSON`,     `SPONSOR`.`SPONSOR_ADDRESS`,  " \
                               "        " \
                               " `SPONSOR`.`SPONSOR_TEL`,    `SPONSOR`.`SPONSOR_FAX`,  `SPONSOR`.`SPONSOR_EMAIL`,  `SPONSOR`.`SPONSOR_STATUS` FROM `Hyper1_Retail`.`SPONSOR` order by SPONSOR_ID*1 asc " )
            records = mycursor.fetchall()

            for row_number, row_data in enumerate(records):
                self.Qtable.insertRow(row_number)
                for column_number, data in enumerate(row_data):

                    if column_number == 9:
                        data = util.FN_GET_STATUS_DESC(str(data))
                        item = QTableWidgetItem(str(data))
                    elif column_number == 2:
                        data = self.FN_GET_SPONSORTYPEDESC(str(data))
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
                sponsorId= self.Qtable.item(rowNo, 0).text()
                sponsorCode = self.Qtable.item(rowNo, 1).text()
                sponsorType = self.Qtable.item(rowNo, 2).text()
                name = self.Qtable.item(rowNo, 3).text()
                contactPerson = self.Qtable.item(rowNo, 4).text()
                address = self.Qtable.item(rowNo, 5).text()
                phone1 = self.Qtable.item(rowNo, 6).text()
                fax = self.Qtable.item(rowNo, 7).text()
                email = self.Qtable.item(rowNo, 8).text()
                status = self.Qtable.item(rowNo, 9).text()

                self.LE_code.setText(sponsorCode)
                self.LE_desc.setText(name)
                self.LE_contactPerson.setText(contactPerson)
                self.LE_address.setText(address)
                self.LE_phone1.setText(phone1)
                self.LE_fax.setText(fax)
                self.LE_email.setText(email)
                self.LB_status.setText(util.FN_GET_STATUS_id(status))
                self.LB_id.setText(sponsorId)
                self.CMB_sponsorType.setCurrentText(sponsorType)
                self.CMB_status.setCurrentText(status)
                # self.FN_MODIFY_CUSTTP()
        except Exception as err:
            print(err)
    def FN_CHECK_DUP_NAME(self,name,id=''):
        self.conn1 = db1.connect()
        mycursor1 = self.conn1.cursor()
        sql = "SELECT SPONSOR_NAME  FROM Hyper1_Retail.SPONSOR where SPONSOR_NAME = '"+name+"' and SPONSOR_ID !='"+str(id)+"'"
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
        mycursor = self.conn.cursor()

        sponsorCode= self.LE_code.text().strip()
        name = self.LE_desc.text().strip()
        contactPerson = self.LE_contactPerson.text().strip()
        phone1 = self.LE_phone1.text().strip()
        fax = self.LE_fax.text().strip()
        address = self.LE_address.text().strip()
        email = self.LE_email.text().strip()
        status = self.CMB_status.currentData()
        sponsorType = str(self.CMB_sponsorType.currentData())
        # get max id
        mycursor.execute("SELECT max(cast(SPONSOR_ID  AS UNSIGNED)) FROM Hyper1_Retail.SPONSOR")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            id = "1"
        else:
            id = int(myresult[0]) + 1

        if name == '' :
            QtWidgets.QMessageBox.warning(self, "خطأ", "برجاءادخال الاسم")

        else:
            try:
                if self.FN_CHECK_DUP_NAME(name ) != False:
                    QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                    mycursor.close()
                else:

                    sql = "INSERT INTO `Hyper1_Retail`.`SPONSOR` (`SPONSOR_ID`,`SPONSOR_SAP_CODE`,`SPONSOR_NAME`,`SPONSOR_TYPE`," \
                          "`SPONSOR_ADDRESS`,`SPONSOR_CONTACT_PERSON`,`SPONSOR_EMAIL`,`SPONSOR_TEL`,`SPONSOR_FAX`,`SPONSOR_STATUS`)   VALUES ( %s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
                    val = (id,sponsorCode,name,sponsorType,address,contactPerson ,email,phone1,fax,status )
                    mycursor.execute(sql, val)
                    print(mycursor.rowcount, "sponsor inserted.")
                    QtWidgets.QMessageBox.information(self, "نجاح", "تم الإنشاء")
                    db1.connectionCommit(self.conn)
                    self.FN_GET_ALL()
                    self.FN_CLEAR_FEILDS()
                    mycursor.close()
                    #db1.connectionClose(self.conn)
                    #self.close()
            except Exception as err:
                print(err)
        print("in create sponsor", name)

        # insert into db

    def FN_MODIFY(self):
        try:
            self.conn1 = db1.connect()
            if len(self.Qtable.selectedIndexes()) >0 :
                rowNo = self.Qtable.selectedItems()[0].row()
                name_old = self.Qtable.item(rowNo, 3).text()
                status_old = util.FN_GET_STATUS_id( self.Qtable.item(rowNo, 9).text())
                sponsorCode = self.LE_code.text().strip()
                name = self.LE_desc.text().strip()
                contactPerson = self.LE_contactPerson.text().strip()
                phone1 = self.LE_phone1.text().strip()
                fax = self.LE_fax.text().strip()
                address = self.LE_address.text().strip()
                email = self.LE_email.text().strip()
                sponsorType = str(self.CMB_sponsorType.currentData())
                status = self.CMB_status.currentData()
                id= self.LB_id.text().strip()
                error = 0
                if name == '':
                    QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء إدخال الاسم")

                else:
                    if name != name_old:
                        if self.FN_CHECK_DUP_NAME(name,id) != False:
                            QtWidgets.QMessageBox.warning(self, "خطأ", "الاسم مكرر")
                            error=1

                    if error!=1:
                        try:
                            mycursor = self.conn1.cursor()
                            changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
                            sql = "UPDATE `Hyper1_Retail`.`SPONSOR` SET `SPONSOR_SAP_CODE` =  %s,`SPONSOR_NAME` =  %s," \
                                  " `SPONSOR_TYPE`= %s,`SPONSOR_ADDRESS` =  %s,`SPONSOR_CONTACT_PERSON` =  %s,`SPONSOR_EMAIL` =  %s,`SPONSOR_TEL` = %s,`SPONSOR_FAX` =  %s,`SPONSOR_STATUS` = %s WHERE SPONSOR_ID = %s"
                            val = (sponsorCode,name, sponsorType,address,contactPerson ,email,  phone1,  fax, status , id)

                            mycursor.execute(sql, val)
                            #mycursor.close()
                            #
                            print(mycursor.rowcount, "record updated.")
                            QtWidgets.QMessageBox.information(self, "نجاح", "تم التعديل")
                            db1.connectionCommit(self.conn1)
                            self.FN_GET_ALL()
                            self.FN_CLEAR_FEILDS ()
                            if str(status) != str(status_old):
                                util.FN_INSERT_IN_LOG("SPONSOR", "status", status, status_old, id)
                        except Exception as err:
                            print(err)
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", "برجاء اختيار السطر المراد تعديله ")
        except Exception as err:
                print(err)
    def FN_CLEAR_FEILDS (self):
        self.LB_id.clear()
        self.LE_code.clear()
        self.LE_desc.clear()
        self.LE_contactPerson.clear()
        self.LE_phone1.clear()
        self.LE_fax.clear()
        self.LE_address.clear()
        self.LE_email.clear()
        self.CMB_status.setCurrentText(util.FN_GET_STATUS_DESC('1'))
        self.LB_status.setText('1')
