from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from data_connection.h1pos import db1

class CL_create_promotion(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    def __init__(self):
        super(CL_create_promotion, self).__init__()

        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/promotion_ui'
        self.conn = db1.connect()



    def FN_LOAD_CREATE_PROM(self):
        filename = self.dirname + '/Promotion_create.ui'
        loadUi(filename, self)

        self.FN_GET_Company()
        self.FN_GET_Branch()
        self.FN_GET_CustomerGroup()
        self.FN_GET_MAGAZINE()
        self.FN_GET_department()
        self.FN_GET_promotion_sponser()
        self.FN_GET_promotion_type()



    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM COMPANY")
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

