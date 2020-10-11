from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

from datetime import datetime
class CL_customer(QtWidgets.QDialog):
    dirname = ''
    def __init__(self):
        super(CL_customer, self).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/loyalty_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/createCustomer.ui'
        loadUi( filename, self )


        self.BTN_createCustomer.clicked.connect(self.FN_CREATE_CUST)

        self.CMB_custGroup.addItems(["1","2","3"])

    def FN_CREATE_CUST(self):
        print("in create cust")