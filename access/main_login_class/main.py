from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from access.authorization_class.Role import CL_role
from access.authorization_class.branch import CL_branch
from access.authorization_class.form import CL_form
from access.authorization_class.formItem import CL_formItem
from access.authorization_class.privilage import CL_privilage
from access.authorization_class.user import CL_user
from access.authorization_class.user_module import CL_userModule
#from access.main_login_class.login import  CL_login
from access.loyalty_class.customer import CL_customer
from access.loyalty_class.customerGP import CL_customerGP
from access.loyalty_class.customerType import CL_customerTP

class CL_main( QtWidgets.QMainWindow ):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        forms = []
        super( CL_main, self ).__init__()
        cwd = Path.cwd()
        mod_path = Path( __file__ ).parent.parent.parent
        dirname = mod_path.__str__() + '/presentation/main_login_ui'
        filename = dirname + '/main.ui'
        loadUi( filename, self )

        print (CL_userModule.user_name)
        CL_userModule.loadPrivilages(self)
        for row_number, row_data in enumerate( CL_userModule.myList ):
            forms.append(row_data[1])

        forms=list(dict.fromkeys(forms))

        print(forms)
        for row in forms:
            #print(row)
            but_name= 'QAct_'+row
            self.findChild( QObject, but_name ).setEnabled( True )

        self.QAct_Create_User.triggered.connect( self.FN_CREATE_USER )
        self.QAct_Modify_User.triggered.connect( self.FN_MODIFY_USER )
        self.QAct_Copy_User.triggered.connect( self.FN_COPY_USER )
        self.QAct_Reset_User_Password.triggered.connect( self.FN_RESET_USER )
        self.QAct_Assign_User_to_Roles.triggered.connect( self.FN_ASSIGN )
        print("hi")
        self.QAct_Create_Role.triggered.connect( self.FN_CREATE_ROLE )
        self.QAct_Modify_Role.triggered.connect( self.FN_MODIFY_ROLE )
        self.QAct_Copy_Role.triggered.connect( self.FN_COPY_ROLE )

        self.QAct_Create_Customer.triggered.connect( self.FN_CREATE_CUST )
        self.QAct_Modify_Customer.triggered.connect( self.FN_MODIFY_CUST )
        self.QAct_Deactivate_Customer.triggered.connect(self.FN_DEACTIVATE_CUST)

        self.QAct_Create_CustGp.triggered.connect( self.FN_CREATE_CUSTGP )
        self.QAct_Modify_CustGp.triggered.connect( self.FN_MODIFY_CUSTGP )
        self.QAct_Deactivate_CustGp.triggered.connect( self.FN_MODIFY_CUSTGP )

        self.QAct_Create_CustTp.triggered.connect( self.FN_CREATE_CUSTTP )
        self.QAct_Modify_CustTp.triggered.connect( self.FN_MODIFY_CUSTTP )

        self.QAct_Cust_Upload_Data.triggered.connect(self.FN_UPLOAD_CUST)

        self.QAct_Create_Privilage.triggered.connect( self.FN_CREATE_PRIV )
        self.QAct_Create_Form.triggered.connect( self.FN_create_form )
        self.QAct_Modify_Form.triggered.connect( self.FN_modify_form )

        self.QAct_Create_Form_Item.triggered.connect( self.FN_create_form_item )
        self.QAct_Modify_Form_Item.triggered.connect( self.FN_modify_form_item )


        self.QAct_Exit.triggered.connect( self.FN_exit )
        self.setWindowTitle( 'HyperPOS Main Page' )

    def FN_CREATE_CUST(self):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()



    def FN_MODIFY_CUST(self):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()
    def FN_DEACTIVATE_CUST(self):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_DEACTIVATE()
        self.window_two.show()

    def FN_UPLOAD_CUST(self):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_UPLOAD()
        self.window_two.show()

    def FN_CREATE_CUSTGP(self):
        self.window_two = CL_customerGP()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_MODIFY_CUSTGP(self):
        self.window_two = CL_customerGP()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

    def FN_CREATE_CUSTTP(self):
        self.window_two = CL_customerTP()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_MODIFY_CUSTTP(self):
        self.window_two = CL_customerTP()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()


    def FN_exit(self):
        QApplication.quit()

    def FN_create_branch(self):
        self.window_two = CL_branch()
        # self.window_two.fn_create_branch()
        self.window_two.show()

    def FN_display_item(self):
        self.window_two = CL_formItem()
        self.window_two.FN_DISPLAY_ITEMS()
        self.window_two.show()

    def FN_CREATE_USER(self):
        self.window_two = CL_user()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_COPY_USER(self):
        self.window_two = CL_user()
        self.window_two.FN_LOAD_COPY()
        self.window_two.show()

    def FN_RESET_USER(self):
        self.window_two = CL_user()
        self.window_two.FN_LOAD_RESET()
        self.window_two.show()


    def FN_MODIFY_USER(self):
        self.window_two = CL_user()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

    def FN_CREATE_ROLE(self):
        self.window_two = CL_role()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_MODIFY_ROLE(self):
        self.window_two = CL_role()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

    def FN_COPY_ROLE(self):
        self.window_two = CL_role()
        self.window_two.FN_LOAD_COPY()
        self.window_two.show()

    def FN_ASSIGN(self):
        self.window_two = CL_role()
        self.window_two.FN_ASSIGN()
        self.window_two.show()

    def FN_modify_form(self):
        self.window_two = CL_form()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

    def FN_create_form(self):
        self.window_two = CL_form()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_CREATE_PRIV(self):
        self.window_two = CL_privilage()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    # def FN_MODIFY_PRIV(self):
    #     self.window_two = CL_privilage()
    #     self.window_two.FN_LOAD_MODFIY()
    #     self.window_two.show()

    # def FN_CREATE_PRIV_ITEM(self):
    #     self.window_two = CL_privilageItem()
    #     self.window_two.FN_LOAD_CREATE()
    #     self.window_two.show()
    # def FN_MODIFY_PRIV_ITEM(self):
    #     self.window_two = CL_privilage()
    #     self.window_two.FN_LOAD_MODFIY()
    #     self.window_two.show()

    def FN_create_form_item(self):
        self.window_two = CL_formItem()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_modify_form_item(self):
        self.window_two = CL_formItem()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

