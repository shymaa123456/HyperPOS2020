from pathlib import Path

from PyQt5 import QtWidgets, QtCore
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
            #for column_number, data in enumerate( row_data ):
                #self.w1.setItem( row_number, column_number, QTableWidgetItem( str( data ) ) )

        x = forms.count( "1" )
        if  x > 0:
            self.QAct_Create_User.triggered.connect( self.FN_CREATE_USER )
        else:
            self.QAct_Create_User.setEnabled( False )

        x = forms.count( "2" )
        if x > 0:
            self.QAct_Modify_User.triggered.connect( self.FN_MODIFY_USER )
        else:
            self.QAct_Modify_User.setEnabled( False )

        x = forms.count( "3" )
        if x > 0:
            self.QAct_Assign_User_to_Roles.triggered.connect( self.FN_ASSIGN )
        else:
            self.QAct_Assign_User_to_Roles.setEnabled( False )
        x = forms.count( "4" )
        if x > 0:
            self.QAct_Create_Role.triggered.connect( self.FN_CREATE_ROLE )
        else:
            self.QAct_Create_Role.setEnabled( False )
        x = forms.count( "5" )
        if x > 0:
            self.QAct_Modify_Role.triggered.connect( self.FN_MODIFY_ROLE )
        else:
            self.QAct_Modify_Role.setEnabled( False )

        self.QAct_Copy_User.triggered.connect(self.FN_COPY_USER)
        self.QAct_Reset_User_Password.triggered.connect(self.FN_RESET_USER)
        self.QAct_Copy_Role.triggered.connect( self.FN_COPY_ROLE)

        self.QAct_Create_Privilage.triggered.connect( self.FN_CREATE_PRIV )
        self.QAct_Create_Form.triggered.connect( self.FN_create_form )
        self.QAct_Modify_Form.triggered.connect( self.FN_modify_form )

        self.QAct_Create_Form_Item.triggered.connect( self.FN_create_form_item )
        self.QAct_Modify_Form_Item.triggered.connect( self.FN_modify_form_item )
        self.QAct_Exit.triggered.connect( self.FN_exit )
        self.setWindowTitle( 'HyperPOS Main Page' )

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

