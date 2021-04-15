from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from access.configuration_class.Parameters import CL_Parameters
from access.coupon_class.CreateCoupon import CL_CreateCoupon
from access.coupon_class.EditCoupon import CL_EditCoupon
from access.coupon_class.StoppedSerial import CL_StoppedSerial
from access.coupon_class.printCoupon import CL_printCoupon
from access.coupon_class.stoppedCoupon import CL_modifyCoupon
from access.loyalty_class.loyalityProg import CL_loyProg
from access.loyalty_class.redeemItem import CL_redItem
from access.loyalty_class.redeemVoucher import CL_redVouch
from access.reports_class.reporting import CL_report

from access.authorization_class.Role import CL_role
from access.authorization_class.branch import CL_branch
from access.authorization_class.form import CL_form
from access.authorization_class.formItem import CL_formItem
from access.authorization_class.privilage import CL_privilage
from access.authorization_class.user import CL_user
from access.authorization_class.user_module import CL_userModule
# from access.main_login_class.login import  CL_login
from access.loyalty_class.customer import CL_customer
from access.loyalty_class.customerGP import CL_customerGP
from access.loyalty_class.customerType import CL_customerTP

# Promotion
from access.promotion_class.Promotion_Add import CL_create_promotion
from PyQt5.QtWidgets import QMessageBox

from access.voucher_class.CreateVoucher import CL_CreateVoucher
from access.voucher_class.EditVoucher import CL_EditVoucher


class CL_main(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal()


    def __init__(self):
        try:
            forms = []
            super(CL_main, self).__init__()
            cwd = Path.cwd()
            mod_path = Path(__file__).parent.parent.parent
            dirname = mod_path.__str__() + '/presentation/main_login_ui'
            filename = dirname + '/main.ui'
            loadUi(filename, self)

            # print (CL_userModule.user_name)
            CL_userModule.loadPrivilages(self)
            for row_number, row_data in enumerate(CL_userModule.myList):
                forms.append(row_data[1])

            forms = list(dict.fromkeys(forms))

            print(forms)
            for row in forms:
                # print(row)
                but_name = 'QAct_' + row
                self.findChild(QObject, but_name).setEnabled(True)

            self.QAct_Create_User.triggered.connect(self.FN_CREATE_USER)
            self.QAct_Modify_User.triggered.connect(self.FN_MODIFY_USER)
            self.QAct_Copy_User.triggered.connect(self.FN_COPY_USER)
            self.QAct_Reset_User_Password.triggered.connect(self.FN_RESET_USER)
            self.QAct_Assign_User_to_Roles.triggered.connect(self.FN_ASSIGN)
            # print("hi")
            self.QAct_Create_Role.triggered.connect(self.FN_CREATE_ROLE)
            self.QAct_Modify_Role.triggered.connect(self.FN_MODIFY_ROLE)
            self.QAct_Copy_Role.triggered.connect(self.FN_COPY_ROLE)

            # self.QAct_Create_Customer.triggered.connect( self.FN_CREATE_CUST )
            # self.QAct_Modify_Customer.triggered.connect( self.FN_MODIFY_CUST )
            # self.QAct_Deactivate_Customer.triggered.connect(self.FN_DEACTIVATE_CUST)
            self.QAct_Display_Customer.triggered.connect(self.FN_DISPLAY_CUST)
            self.QAct_Cust_Points_Upload.triggered.connect(self.FN_UP_CUST_PT)

            self.QAct_Display_Loyality.triggered.connect(self.FN_CREATE_LOYPROG)

            self.QAct_Display_CustGp.triggered.connect(self.FN_DISPLAY_CUSTGP)
            self.QAct_Display_CustTp.triggered.connect(self.FN_DISPLAY_CUSTTP)

            self.QAct_Redeem_Item.triggered.connect(self.FN_DISPLAY_REDITEM)
            self.QAct_Redeem_Voucher.triggered.connect(self.FN_DISPLAY_REDITEMVOUCHER)




            self.QAct_Create_Privilage.triggered.connect(self.FN_CREATE_PRIV)
            self.QAct_Create_Form.triggered.connect(self.FN_create_form)
            self.QAct_Modify_Form.triggered.connect(self.FN_modify_form)

            self.QAct_Create_Form_Item.triggered.connect(self.FN_create_form_item)
            self.QAct_Modify_Form_Item.triggered.connect(self.FN_modify_form_item)

            """ Promotion """
            self.QAct_Prom_Add.triggered.connect(self.FN_search_promotion)
            self.QAct_Report_Promotion_1.triggered.connect(self.FN_search_reporting)


            #Todo: method for Open Create Coupon Window
            self.QAct_Coupon_Add.triggered.connect(self.FN_CreateCoupon)
            self.QAct_Coupon_Deactivate.triggered.connect(self.FN_ModifyCoupon)
            self.QAct_Coupon_Activate.triggered.connect(self.FN_ModifyCoupon)
            self.QAct_Coupon_Edit.triggered.connect(self.FN_EditCoupon)
            self.QAct_Coupon_Print.triggered.connect(self.FN_PrintCoupon)
            self.QAct_Coupon_barcode.triggered.connect(self.FN_SerialCoupon)

            #Todo: method for Open Create Voucher Window
            self.QAct_Voucher_Add.triggered.connect(self.FN_CreateVoucher)
            self.QAct_Voucher_Edit.triggered.connect(self.FN_EditVoucher)



            # Parameter Form
            self.QAct_Parameter.triggered.connect(self.FN_Parameters)

            self.QAct_Exit.triggered.connect(self.FN_exit)
            self.setWindowTitle('HyperPOS Main Page')
        except Exception as err:
            print(err)

    def FN_UP_CUST_PT(self):

        try:
            self.window_two = CL_customer()
            self.window_two.FN_LOAD_UPLOAD_PT()
            self.window_two.show()

        except Exception as err:
         print(err)
    def FN_CREATE_LOYPROG(self):
        self.window_two = CL_loyProg()
        self.window_two.FN_LOAD_DISPLAY()
        self.window_two.show()

    def FN_CREATE_CUST(self):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_DISPLAY_CUST(self):
        self.window_two = CL_customer()
        self.window_two.FN_LOAD_DISPLAY()
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

    def FN_DISPLAY_CUSTGP(self):
        self.window_two = CL_customerGP()
        self.window_two.FN_LOAD_DISPlAY()
        self.window_two.show()

    def FN_DISPLAY_CUSTTP(self):
        self.window_two = CL_customerTP()
        try:
            self.window_two.FN_LOAD_DISPlAY()
            self.window_two.show()
        except Exception as err:
            print(err)


    def FN_DISPLAY_REDITEM(self):
        try:
            self.window_two = CL_redItem()

            self.window_two.FN_LOAD_DISPlAY()
            self.window_two.show()
        except Exception as err:
            print(err)

    def FN_DISPLAY_REDITEMVOUCHER(self):
        try:
            self.window_two = CL_redVouch()

            self.window_two.FN_LOAD_DISPlAY()
            self.window_two.show()
        except Exception as err:
            print(err)

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
        self.window_two.FN_LOAD_RESET_MAIN()
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

    """ Promotion """

    def FN_search_promotion(self):
        self.window_two = CL_create_promotion()
        self.window_two.FN_LOAD_CREATE_PROM()
        self.window_two.show()



    def FN_search_reporting(self):
        self.window_two = CL_report()
        self.window_two.show()


    def FN_CreateCoupon(self):
        self.window_two = CL_CreateCoupon()
        self.window_two.FN_LOADUI()
        self.window_two.show()


    def FN_ModifyCoupon(self):
        self.window_two = CL_modifyCoupon()
        self.window_two.FN_LOADUI()
        self.window_two.show()

    def FN_EditCoupon(self):
        self.window_two = CL_EditCoupon()
        self.window_two.FN_LOADUI()
        self.window_two.show()

    def FN_PrintCoupon(self):
        self.window_two = CL_printCoupon()
        self.window_two.FN_LOADUI()
        self.window_two.show()

    def FN_SerialCoupon(self):
        self.window_two = CL_StoppedSerial()
        self.window_two.FN_LOADUI()
        self.window_two.show()


    def FN_CreateVoucher(self):
        self.window_two=CL_CreateVoucher()
        self.window_two.FN_LOADUI()
        self.window_two.show()

    def FN_EditVoucher(self):
        self.window_two=CL_EditVoucher()
        self.window_two.FN_LOADUI()
        self.window_two.show()

    # Configuration Parametrs
    def FN_Parameters(self):
        self.window_two =CL_Parameters()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    # close application event
    def closeEvent(self, event):
        # print("event")
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit Application?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            event.ignore()