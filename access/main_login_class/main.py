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
from access.customer_service_class.customer_complain import CL_CustService
from access.loyalty_class.CL_loyPoint import CL_loyPoint
from access.loyalty_class.customerCard import CL_customerCard
from access.loyalty_class.loyalityProg import CL_loyProg
from access.loyalty_class.redeemGift import CL_redGift
from access.loyalty_class.redeemItem import CL_redItem
from access.loyalty_class.redeemType import CL_redeemType
from access.loyalty_class.redeemVoucher import CL_redVouch
from access.reports_class.reporting import CL_report
from access.reports_class.reporting1 import CL_report1

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

from access.voucher_class.CreateVoucher import   CL_CreateVoucher
#Installment
from access.installment_class.Bank import CL_CreateBank
from access.installment_class.installment import CL_installment
from access.installment_class.installmentModfiy import CL_installmentModify
from access.installment_class.Activeinstallment import CL_installment_Activation

from access.voucher_class.CreateVoucher import CL_CreateVoucher
from access.voucher_class.EditVoucher import CL_EditVoucher
from access.voucher_class.stoppedVoucher import CL_modifyVoucher
from access.promotion_voucher_class.PromotionVoucher import CL_PromVoucher


class CL_main(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        try:
            forms = []
            super(CL_main, self).__init__()
            cwd = Path.cwd()
            mod_path = Path(__file__).parent.parent.parent
            dirname = mod_path.__str__() + '/presentation/main_login_ui'
            filename = dirname + '/main3.ui'
            self.ui = loadUi(filename, self)

            # print (CL_userModule.user_name)
            CL_userModule.loadPrivilages(self)
            CL_userModule.FN_AuthBranchUser(self)
            CL_userModule.FN_AuthSectionUser(self)
            for row_number, row_data in enumerate(CL_userModule.myList):
                forms.append(row_data[1])

            forms = list(dict.fromkeys(forms))

            #print(forms)
            for row in forms:
                #print(row)
                but_name = 'QAct_' + row
                # self.findChild(QObject, but_name).setEnabled(True)

            self.QAct_Create_User.clicked.connect(self.FN_CREATE_USER)
            self.QAct_Modify_User.clicked.connect(self.FN_MODIFY_USER)
            self.QAct_Copy_User.clicked.connect(self.FN_COPY_USER)
            self.QAct_Reset_User_Password.clicked.connect(self.FN_RESET_USER)
            self.QAct_Assign_User_to_Roles.clicked.connect(self.FN_ASSIGN)
            # print("hi")
            self.QAct_Create_Role.clicked.connect(self.FN_CREATE_ROLE)
            self.QAct_Modify_Role.clicked.connect(self.FN_MODIFY_ROLE)
            self.QAct_Copy_Role.clicked.connect(self.FN_COPY_ROLE)

            self.QAct_Display_Customer.clicked.connect(self.FN_DISPLAY_CUST)
            self.QAct_Cust_Points_Upload.clicked.connect(self.FN_UP_CUST_PT)

            self.QAct_Display_Loyality.clicked.connect(self.FN_CREATE_LOYPROG)

            self.QAct_Display_CustGp.clicked.connect(self.FN_DISPLAY_CUSTGP)
            self.QAct_Display_CustTp.clicked.connect(self.FN_DISPLAY_CUSTTP)

            self.QAct_Redeem_Item.clicked.connect(self.FN_DISPLAY_REDITEM)
            self.QAct_Redeem_Voucher.clicked.connect(self.FN_DISPLAY_REDITEMVOUCHER)
            self.QAct_Redeem_Gift.clicked.connect(self.FN_DISPLAY_REDITEMGIFT)

            """ redeem type """
            self.QAct_Redeem_Type.clicked.connect(self.FN_DISPLAY_REDEEMTP)
            self.QAct_Loyality_Point.clicked.connect(self.FN_DISPLAY_LOYPOINTS)

            ###test
            self.QAct_Create_Privilage.clicked.connect(self.FN_CREATE_PRIV)
            self.QAct_Create_Form.clicked.connect(self.FN_create_form)
            self.QAct_Modify_Form.clicked.connect(self.FN_modify_form)

            self.QAct_Create_Form_Item.clicked.connect(self.FN_create_form_item)
            self.QAct_Modify_Form_Item.clicked.connect(self.FN_modify_form_item)




            """ Promotion """
            self.QAct_Prom_Add.clicked.connect(self.FN_search_promotion)
            self.QAct_Report_Promotion_1.triggered.connect(self.FN_search_reporting)
            self.QAct_Report_Promotion_2.triggered.connect(self.FN_search_reporting1)

            # Todo: method for Open Create Coupon Window
            self.QAct_Coupon_Add.clicked.connect(self.FN_CreateCoupon)
            self.QAct_Coupon_Deactivate.clicked.connect(self.FN_ModifyCoupon)
            self.QAct_Coupon_Activate.clicked.connect(self.FN_ModifyCoupon)
            self.QAct_Coupon_Edit.clicked.connect(self.FN_EditCoupon)
            self.QAct_Coupon_Print.clicked.connect(self.FN_PrintCoupon)
            self.QAct_Coupon_barcode.clicked.connect(self.FN_SerialCoupon)

            # Todo: method for Open Create Voucher Window
            self.QAct_Voucher_Add.clicked.connect(self.FN_CreateVoucher)
            self.QAct_Voucher_Edit.clicked.connect(self.FN_EditVoucher)
            self.QAct_Voucher_Activate.clicked.connect(self.FN_StoppedVoucher)
            self.QAct_Voucher_Deactivate.clicked.connect(self.FN_StoppedVoucher)
            # Todo: method for Open promotion Voucher Window
            self.QAct_Prom_Voucher_Add.clicked.connect(self.FN_CreatePromVoucher)
            self.QAct_Prom_Voucher_Edit.clicked.connect(self.FN_EditPromVoucher)
            self.QAct_Prom_Voucher_Act.clicked.connect(self.FN_LOAD_CHANGE_STATUS_ACTIVE)
            self.QAct_Prom_Voucher_Deact.clicked.connect(self.FN_LOAD_CHANGE_STATUS_INACTIVE)

            self.QAct_Customer_Service.clicked.connect(self.FN_Customer_Service)

            # customer card
            self.QAct_Cust_Card_Add.clicked.connect(self.FN_Cust_Card_Add)
            self.QAct_Cust_Card_Edit.clicked.connect(self.FN_Cust_Card_Edit)
            # for installment
            self.QAct_Create_Bank.clicked.connect(self.FN_CREATE_Bank)
            self.QAct_Modify_Bank.clicked.connect(self.FN_Modify_Bank)
            self.QAct_Install_Add.clicked.connect(self.FN_CREATE_installment)
            self.QAct_Install_Edit.clicked.connect(self.FN_Modify_installment)
            self.QAct_Install_Activate_Deactivate.clicked.connect(self.FN_Active_installment)

            # Parameter Form
            self.QAct_Parameter.clicked.connect(self.FN_Parameters)

            self.QAct_Exit.clicked.connect(self.FN_exit)

            # self.ui.tabWidget.setTabsClosable(True)
            self.ui.tabWidget.tabCloseRequested.connect(lambda index: self.ui.tabWidget.removeTab(index))
            self.window_Active_installment = 0
            self.window_Modify_installment = 0
            self.window_CREATE_installment = 0
            self.window_Modify_Bank = 0
            self.window_CREATE_Bank = 0
            self.window_Parameters = 0
            self.window_Customer_Service = 0
            self.window_LOAD_CHANGE_STATUS_INACTIVE = 0
            self.window_LOAD_CHANGE_STATUS_ACTIVE = 0
            self.window_EditPromVoucher = 0
            self.window_CreatePromVoucher = 0
            self.window_StoppedVoucher = 0
            self.window_EditVoucher = 0
            self.window_CreateVoucher = 0
            self.window_SerialCoupon = 0
            self.window_PrintCoupon = 0
            self.window_EditCoupon = 0
            self.window_ModifyCoupon = 0
            self.window_CreateCoupon = 0
            self.window_search_reporting1 = 0
            self.window_search_reporting = 0
            self.window_search_promotion = 0
            self.window_modify_form_item = 0
            self.window_create_form_item = 0
            self.window_CREATE_PRIV = 0
            self.window_create_form = 0
            self.window_modify_form = 0
            self.window_ASSIGN = 0
            self.window_COPY_ROLE = 0
            self.window_MODIFY_ROLE = 0
            self.window_CREATE_ROLE = 0
            self.window_MODIFY_USER = 0
            self.window_RESET_USER = 0
            self.window_COPY_USER = 0
            self.window_CREATE_USER = 0
            self.window_display_item = 0
            self.window_create_branch = 0
            self.window_DISPLAY_LOYPOINTS = 0
            self.window_DISPLAY_REDEEMTP = 0
            self.window_DISPLAY_REDITEMGIFT = 0
            self.window_DISPLAY_REDITEMVOUCHER = 0
            self.window_DISPLAY_REDITEM = 0
            self.window_DISPLAY_CUSTTP = 0
            self.window_DISPLAY_CUSTGP = 0
            self.window_UPLOAD_CUST = 0
            self.window_DISPLAY_CUST = 0
            self.window_CREATE_LOYPROG = 0
            self.window_UP_CUST_PT = 0
            self.window_Cust_Card_Edit = 0
            self.window_Cust_Card_Add = 0

            #self.ui.tabWidget.blockSignals(True)
            self.ui.tabWidget.currentChanged.connect(self.onChange)
            self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
            self.ui.actionMain_Menu.triggered.connect(self.ShowHideMenu)
            # self.ui.MainMenu.clicked.connect(self.ShowHideMenu)
            #self.ui.tabWidget.blockSignals(False)
            self.setWindowTitle('HyperPOS Main Page')

        except Exception as err:
            print(err)

    def ShowHideMenu(self):
        if self.ui.widget.isVisible():
            self.ui.widget.setVisible(False)
        else:
            self.ui.widget.setVisible(True)


    def FN_Cust_Card_Add(self):
        if self.window_Cust_Card_Add == 0:
            self.window_Cust_Card_Add = CL_customerCard()
            self.window_Cust_Card_Add.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_Cust_Card_Add, 'انشاء كارت عميل')
            self.ui.tabWidget.setFixedWidth(self.window_Cust_Card_Add.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Cust_Card_Add.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Cust_Card_Add)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Cust_Card_Add.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Cust_Card_Add.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Cust_Card_Add)


    def FN_Cust_Card_Edit(self):
        if self.window_Cust_Card_Edit == 0:
            self.window_Cust_Card_Edit = CL_customerCard()
            self.window_Cust_Card_Edit.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_Cust_Card_Edit, 'تعديل كارت عميل')
            self.ui.tabWidget.setFixedWidth(self.window_Cust_Card_Edit.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Cust_Card_Edit.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Cust_Card_Edit)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Cust_Card_Edit.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Cust_Card_Edit.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Cust_Card_Edit)


    def FN_UP_CUST_PT(self):

        try:
            if self.window_UP_CUST_PT == 0:
                self.window_UP_CUST_PT = CL_customer()
                self.window_UP_CUST_PT.FN_LOAD_UPLOAD_PT()
                self.ui.tabWidget.addTab(self.window_UP_CUST_PT, 'تحميل نقاط عملاء من خارج النظام')
                self.ui.tabWidget.setFixedWidth(self.window_UP_CUST_PT.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_UP_CUST_PT.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_UP_CUST_PT)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_UP_CUST_PT.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_UP_CUST_PT.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_UP_CUST_PT)
        except Exception as err:
         print(err)




    def FN_CREATE_LOYPROG(self):
        if self.window_CREATE_LOYPROG == 0:
            self.window_CREATE_LOYPROG = CL_loyProg('aaaaa')
            self.window_CREATE_LOYPROG.FN_LOAD_DISPLAY()
            self.ui.tabWidget.addTab(self.window_CREATE_LOYPROG, 'انشاء برنامج عضوية')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_LOYPROG.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_LOYPROG.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_LOYPROG)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_LOYPROG.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_LOYPROG.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_LOYPROG)



    def  FN_DISPLAY_CUST(self):
        # self.onTabCloseRequested_DISPLAY_CUST()
        if self.window_DISPLAY_CUST == 0:
            self.window_DISPLAY_CUST = CL_customer()
            self.window_DISPLAY_CUST.FN_LOAD_DISPLAY()
            self.ui.tabWidget.addTab(self.window_DISPLAY_CUST, 'العملاء')
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUST.frameGeometry().height())
            # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested_DISPLAY_CUST)
            self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_CUST)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUST.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_CUST)



    def FN_UPLOAD_CUST(self):
        if self.window_UPLOAD_CUST == 0:
            self.window_UPLOAD_CUST = CL_customer()
            self.window_UPLOAD_CUST.FN_LOAD_UPLOAD()
            self.ui.tabWidget.addTab(self.window_UPLOAD_CUST, 'طباعة كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_UPLOAD_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UPLOAD_CUST.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_UPLOAD_CUST)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_UPLOAD_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UPLOAD_CUST.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_UPLOAD_CUST)


    def FN_DISPLAY_CUSTGP(self):
        if self.window_DISPLAY_CUSTGP == 0:
            self.window_DISPLAY_CUSTGP = CL_customerGP('aaaaa')
            self.window_DISPLAY_CUSTGP.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_DISPLAY_CUSTGP, 'مجموعة عملاء')
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUSTGP.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUSTGP.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_CUSTGP)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUSTGP.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUSTGP.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_CUSTGP)


    def FN_DISPLAY_CUSTTP(self):
        try:
            if self.window_DISPLAY_CUSTTP == 0:
                self.window_DISPLAY_CUSTTP = CL_customerTP()
                self.window_DISPLAY_CUSTTP.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_DISPLAY_CUSTTP, 'انشاء مستويات عملاء')
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUSTTP.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUSTTP.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_CUSTTP)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUSTTP.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUSTTP.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_CUSTTP)
        except Exception as err:
            print(err)



    def FN_DISPLAY_REDITEM(self):
        try:
            if self.window_DISPLAY_REDITEM == 0:
                self.window_DISPLAY_REDITEM = CL_redItem()
                self.window_DISPLAY_REDITEM.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_DISPLAY_REDITEM, 'تعريف اصناف الهدايا')
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEM.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEM.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDITEM)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEM.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEM.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDITEM)
        except Exception as err:
            print(err)


    def FN_DISPLAY_REDITEMVOUCHER(self):
        try:
            if self.window_DISPLAY_REDITEMVOUCHER == 0:
                self.window_DISPLAY_REDITEMVOUCHER = CL_redVouch()
                self.window_DISPLAY_REDITEMVOUCHER.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_DISPLAY_REDITEMVOUCHER, 'استبدال النقاط بقسيمة شراء')
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEMVOUCHER.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEMVOUCHER.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDITEMVOUCHER)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEMVOUCHER.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEMVOUCHER.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDITEMVOUCHER)
        except Exception as err:
            print(err)


    def FN_DISPLAY_REDITEMGIFT(self):
        try:
            if self.window_DISPLAY_REDITEMGIFT == 0:
                self.window_DISPLAY_REDITEMGIFT = CL_redGift()
                self.window_DISPLAY_REDITEMGIFT.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_DISPLAY_REDITEMGIFT, 'استبدال النقاط بالهدايا')
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEMGIFT.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEMGIFT.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDITEMGIFT)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEMGIFT.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEMGIFT.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDITEMGIFT)
        except Exception as err:
            print(err)



    def FN_DISPLAY_REDEEMTP(self):
        try:
            if self.window_DISPLAY_REDEEMTP == 0:
                self.window_DISPLAY_REDEEMTP = CL_redeemType()
                self.window_DISPLAY_REDEEMTP.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_DISPLAY_REDEEMTP, 'Redeem Type')
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDEEMTP.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDEEMTP.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDEEMTP)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDEEMTP.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDEEMTP.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_REDEEMTP)
        except Exception as err:
            print(err)


    def FN_DISPLAY_LOYPOINTS(self):
        try:
            if self.window_DISPLAY_LOYPOINTS == 0:
                self.window_DISPLAY_LOYPOINTS = CL_loyPoint()
                self.window_DISPLAY_LOYPOINTS.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_DISPLAY_LOYPOINTS, 'تعريف قيمة استبدال النقاط')
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_LOYPOINTS.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_LOYPOINTS.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_LOYPOINTS)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_LOYPOINTS.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_LOYPOINTS.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_DISPLAY_LOYPOINTS)
        except Exception as err:
            print(err)


    def FN_exit(self):
        QApplication.quit()

    def FN_create_branch(self):
        if self.window_create_branch == 0:
            self.window_create_branch = CL_branch()
            self.ui.tabWidget.addTab(self.window_create_branch, 'طباعة كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_create_branch.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_branch.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_create_branch)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_create_branch.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_branch.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_create_branch)


    def FN_display_item(self):
        if self.window_display_item == 0:
            self.window_display_item = CL_formItem()
            self.window_display_item.FN_DISPLAY_ITEMS()
            self.ui.tabWidget.addTab(self.window_display_item, 'طباعة كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_display_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_display_item.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_display_item)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_display_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_display_item.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_display_item)


    def FN_CREATE_USER(self):
        if self.window_CREATE_USER == 0:
            self.window_CREATE_USER = CL_user()
            self.window_CREATE_USER.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CREATE_USER, 'Create User')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_USER)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_USER)


    def FN_COPY_USER(self):
        if self.window_COPY_USER == 0:
            self.window_COPY_USER = CL_user()
            self.window_COPY_USER.FN_LOAD_COPY()
            self.ui.tabWidget.addTab(self.window_COPY_USER, 'Copy User')
            self.ui.tabWidget.setFixedWidth(self.window_COPY_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_COPY_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_COPY_USER)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_COPY_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_COPY_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_COPY_USER)


    def FN_RESET_USER(self):
        if self.window_RESET_USER == 0:
            self.window_RESET_USER = CL_user()
            self.window_RESET_USER.FN_LOAD_RESET_MAIN()
            self.ui.tabWidget.addTab(self.window_RESET_USER, 'Reset User')
            self.ui.tabWidget.setFixedWidth(self.window_RESET_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_RESET_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_RESET_USER)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_RESET_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_RESET_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_RESET_USER)


    def FN_MODIFY_USER(self):
        if self.window_MODIFY_USER == 0:
            self.window_MODIFY_USER = CL_user()
            self.window_MODIFY_USER.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_MODIFY_USER, 'Modify User')
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_MODIFY_USER)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_USER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_MODIFY_USER)


    def FN_CREATE_ROLE(self):
        if self.window_CREATE_ROLE == 0:
            self.window_CREATE_ROLE = CL_role()
            self.window_CREATE_ROLE.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CREATE_ROLE, 'Create Role')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_ROLE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_ROLE)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_ROLE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_ROLE)


    def FN_MODIFY_ROLE(self):
        if self.window_MODIFY_ROLE == 0:
            self.window_MODIFY_ROLE = CL_role()
            self.window_MODIFY_ROLE.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_MODIFY_ROLE, 'Modify Role')
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_ROLE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_MODIFY_ROLE)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_ROLE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_MODIFY_ROLE)


    def FN_COPY_ROLE(self):
        if self.window_COPY_ROLE == 0:
            self.window_COPY_ROLE = CL_role()
            self.window_COPY_ROLE.FN_LOAD_COPY()
            self.ui.tabWidget.addTab(self.window_COPY_ROLE, 'Copy Role')
            self.ui.tabWidget.setFixedWidth(self.window_COPY_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_COPY_ROLE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_COPY_ROLE)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_COPY_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_COPY_ROLE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_COPY_ROLE)


    def FN_ASSIGN(self):
        if self.window_ASSIGN == 0:
            self.window_ASSIGN = CL_role()
            self.window_ASSIGN.FN_ASSIGN()
            self.ui.tabWidget.addTab(self.window_ASSIGN, 'Assign User to Roles')
            self.ui.tabWidget.setFixedWidth(self.window_ASSIGN.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ASSIGN.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_ASSIGN)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_ASSIGN.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ASSIGN.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_ASSIGN)


    def FN_modify_form(self):
        if self.window_modify_form == 0:
            self.window_modify_form = CL_form()
            self.window_modify_form.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_modify_form, 'Modify Form')
            self.ui.tabWidget.setFixedWidth(self.window_modify_form.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_modify_form.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_modify_form)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_modify_form.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_modify_form.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_modify_form)


    def FN_create_form(self):
        if self.window_create_form == 0:
            self.window_create_form = CL_form()
            self.window_create_form.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_create_form, 'Create Form')
            self.ui.tabWidget.setFixedWidth(self.window_create_form.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_form.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_create_form)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_create_form.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_form.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_create_form)


    def FN_CREATE_PRIV(self):
        if self.window_CREATE_PRIV == 0:
            self.window_CREATE_PRIV = CL_privilage()
            self.window_CREATE_PRIV.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CREATE_PRIV, 'Create Privilage')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_PRIV.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_PRIV.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_PRIV)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_PRIV.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_PRIV.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_PRIV)


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
        if self.window_create_form_item == 0:
            self.window_create_form_item = CL_formItem()
            self.window_create_form_item.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_create_form_item, 'Create Form Item')
            self.ui.tabWidget.setFixedWidth(self.window_create_form_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_form_item.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_create_form_item)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_create_form_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_form_item.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_create_form_item)


    def FN_modify_form_item(self):
        if self.window_modify_form_item == 0:
            self.window_modify_form_item = CL_formItem()
            self.window_modify_form_item.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_modify_form_item, 'Modify Form Item')
            self.ui.tabWidget.setFixedWidth(self.window_modify_form_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_modify_form_item.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_modify_form_item)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_modify_form_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_modify_form_item.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_modify_form_item)


    """ Promotion """

    def FN_search_promotion(self):
        if self.window_search_promotion == 0:
            self.window_search_promotion = CL_create_promotion()
            self.window_search_promotion.FN_LOAD_CREATE_PROM()
            self.ui.tabWidget.addTab(self.window_search_promotion, 'انشاء العروض')
            self.ui.tabWidget.setFixedWidth(self.window_search_promotion.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_promotion.frameGeometry().height() + 20)
            self.ui.tabWidget.setCurrentWidget(self.window_search_promotion)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_search_promotion.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_promotion.frameGeometry().height() + 20)
            self.ui.tabWidget.setCurrentWidget(self.window_search_promotion)


    def FN_search_reporting(self):
        if self.window_search_reporting == 0:
            self.window_search_reporting = CL_report()
            self.ui.tabWidget.addTab(self.window_search_reporting, 'الاستعلام عن العروض')
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_search_reporting)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_search_reporting)


    def FN_search_reporting1(self):
        if self.window_search_reporting1 == 0:
            self.window_search_reporting1 = CL_report1()
            self.ui.tabWidget.addTab(self.window_search_reporting1, 'الاستعلام عن كوبونات الخصم')
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting1.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting1.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_search_reporting1)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting1.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting1.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_search_reporting1)



    def FN_CreateCoupon(self):
        if self.window_CreateCoupon == 0:
            self.window_CreateCoupon = CL_CreateCoupon()
            self.window_CreateCoupon.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_CreateCoupon, 'انشاء كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_CreateCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateCoupon.frameGeometry().height()+20)
            # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested_CreateCoupon)
            self.ui.tabWidget.setCurrentWidget(self.window_CreateCoupon)
            # self.name = self.ui.tabWidget.currentWidget().objectName()
            print(self.ui.tabWidget.currentWidget())
            print(self.window_CreateCoupon)
            self.flag2 = 1
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CreateCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateCoupon.frameGeometry().height() + 20)
            self.ui.tabWidget.setCurrentWidget(self.window_CreateCoupon)

        # if self.name == self.ui.tabWidget.currentWidget().objectName():
        #     self.ui.tabWidget.setFixedWidth(self.window_two.frameGeometry().width())
        #     self.ui.tabWidget.setFixedHeight(self.window_two.frameGeometry().height() + 20)
        # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested2)


    def FN_ModifyCoupon(self):
        if self.window_ModifyCoupon == 0:
            self.window_ModifyCoupon = CL_modifyCoupon()
            self.window_ModifyCoupon.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_ModifyCoupon, 'تفعيل او ايقاف كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_ModifyCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ModifyCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_ModifyCoupon)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_ModifyCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ModifyCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_ModifyCoupon)



    def FN_EditCoupon(self):

        if self.window_EditCoupon == 0:
            self.window_EditCoupon = CL_EditCoupon()
            self.window_EditCoupon.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_EditCoupon, 'تعديل كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_EditCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_EditCoupon)
            # self.name = self.ui.tabWidget.currentWidget().objectName()
            self.flag1 = 1
        else:
            self.ui.tabWidget.setFixedWidth(self.window_EditCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_EditCoupon)

        # if self.name == self.ui.tabWidget.currentWidget().objectName():
        #     self.ui.tabWidget.setFixedWidth(self.window_two1.frameGeometry().width())
        #     self.ui.tabWidget.setFixedHeight(self.window_two1.frameGeometry().height())
        # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)

        # self.window_two.show()

    def FN_PrintCoupon(self):
        if self.window_PrintCoupon == 0:
            self.window_PrintCoupon = CL_printCoupon()
            self.window_PrintCoupon.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_PrintCoupon, 'طباعة كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_PrintCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_PrintCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_PrintCoupon)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_PrintCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_PrintCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_PrintCoupon)


    def FN_SerialCoupon(self):
        if self.window_SerialCoupon == 0:
            self.window_SerialCoupon = CL_StoppedSerial()
            self.window_SerialCoupon.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_SerialCoupon, 'تفعيل وايقاف واستبدال كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_SerialCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_SerialCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_SerialCoupon)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_SerialCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_SerialCoupon.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_SerialCoupon)



    def FN_CreateVoucher(self):
        if self.window_CreateVoucher == 0:
            self.window_CreateVoucher = CL_CreateVoucher()
            self.window_CreateVoucher.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_CreateVoucher, 'انشاء قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_CreateVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateVoucher.frameGeometry().height() + 20)
            self.ui.tabWidget.setCurrentWidget(self.window_CreateVoucher)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CreateVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateVoucher.frameGeometry().height() + 20)
            self.ui.tabWidget.setCurrentWidget(self.window_CreateVoucher)

    def FN_EditVoucher(self):
        if self.window_EditVoucher == 0:
            self.window_EditVoucher = CL_EditVoucher()
            self.window_EditVoucher.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_EditVoucher, 'تعديل قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_EditVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_EditVoucher)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_EditVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_EditVoucher)


    def FN_StoppedVoucher(self):
        if self.window_StoppedVoucher == 0:
            self.window_StoppedVoucher = CL_modifyVoucher()
            self.window_StoppedVoucher.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_StoppedVoucher, 'تنشيط او ايقاف قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_StoppedVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_StoppedVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_StoppedVoucher)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_StoppedVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_StoppedVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_StoppedVoucher)


    def FN_CreatePromVoucher(self):
        if self.window_CreatePromVoucher == 0:
            self.window_CreatePromVoucher = CL_PromVoucher()
            self.window_CreatePromVoucher.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CreatePromVoucher, 'انشاء قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_CreatePromVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreatePromVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CreatePromVoucher)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CreatePromVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreatePromVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CreatePromVoucher)


    def FN_EditPromVoucher(self):
        if self.window_EditPromVoucher == 0:
            self.window_EditPromVoucher = CL_PromVoucher()
            self.window_EditPromVoucher.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_EditPromVoucher, 'تعديل قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_EditPromVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditPromVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_EditPromVoucher)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_EditPromVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditPromVoucher.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_EditPromVoucher)


    def FN_LOAD_CHANGE_STATUS_ACTIVE(self):
        if self.window_LOAD_CHANGE_STATUS_ACTIVE == 0:
            self.window_LOAD_CHANGE_STATUS_ACTIVE = CL_PromVoucher()
            self.window_LOAD_CHANGE_STATUS_ACTIVE.FN_LOAD_CHANGE_STATUS_ACTIVE()
            self.ui.tabWidget.addTab(self.window_LOAD_CHANGE_STATUS_ACTIVE, 'تنشيط قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_LOAD_CHANGE_STATUS_ACTIVE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_LOAD_CHANGE_STATUS_ACTIVE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_LOAD_CHANGE_STATUS_ACTIVE)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_LOAD_CHANGE_STATUS_ACTIVE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_LOAD_CHANGE_STATUS_ACTIVE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_LOAD_CHANGE_STATUS_ACTIVE)


    def FN_LOAD_CHANGE_STATUS_INACTIVE(self):
        if self.window_LOAD_CHANGE_STATUS_INACTIVE == 0:
            self.window_LOAD_CHANGE_STATUS_INACTIVE = CL_PromVoucher()
            self.window_LOAD_CHANGE_STATUS_INACTIVE.FN_LOAD_CHANGE_STATUS_INACTIVE()
            self.ui.tabWidget.addTab(self.window_LOAD_CHANGE_STATUS_INACTIVE, 'ايقاف قسيمة مشتريات')
            self.ui.tabWidget.setFixedWidth(self.window_LOAD_CHANGE_STATUS_INACTIVE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_LOAD_CHANGE_STATUS_INACTIVE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_LOAD_CHANGE_STATUS_INACTIVE)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_LOAD_CHANGE_STATUS_INACTIVE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_LOAD_CHANGE_STATUS_INACTIVE.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_LOAD_CHANGE_STATUS_INACTIVE)


    def FN_Customer_Service(self):
        if self.window_Customer_Service == 0:
            self.window_Customer_Service = CL_CustService()
            self.window_Customer_Service.FN_LOAD_DISPLAY()
            self.ui.tabWidget.addTab(self.window_Customer_Service, 'خدمة العملاء')
            self.ui.tabWidget.setFixedWidth(self.window_Customer_Service.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Customer_Service.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Customer_Service)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Pwindow_Customer_ServicerintCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Customer_Service.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Customer_Service)

    # Configuration Parametrs
    def FN_Parameters(self):
        if self.window_Parameters == 0:
            self.window_Parameters = CL_Parameters()
            self.window_Parameters.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_Parameters, 'Configuration Parametrs')
            self.ui.tabWidget.setFixedWidth(self.window_Parameters.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Parameters.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Parameters)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Parameters.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Parameters.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Parameters)


    # close application event
    def closeEvent(self, event):
        # print("event")
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit Application?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            event.ignore()


    #Installment
    def FN_CREATE_Bank(self):
        # self.window_two = CL_CreateBank()
        # self.window_two.FN_LOAD_CREATE()
        if self.window_CREATE_Bank == 0:
            self.window_CREATE_Bank = CL_CreateBank()
            self.window_CREATE_Bank.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CREATE_Bank, 'تعديل بنك')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_Bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_Bank.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_Bank)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_Bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_Bank.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_Bank)
#        self.window_two.MdiParent = self.ParentForm
        # self.window_two.show()
        # self.window_two.setModal(self, True)
        # self.window_two.exec()

    def FN_Modify_Bank(self):
        if self.window_Modify_Bank == 0:
            self.window_Modify_Bank = CL_CreateBank()
            self.window_Modify_Bank.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_Modify_Bank, 'تعديل بنك')
            self.ui.tabWidget.setFixedWidth(self.window_Modify_Bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_Bank.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Modify_Bank)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Modify_Bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_Bank.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Modify_Bank)


    def FN_CREATE_installment(self):
        if self.window_CREATE_installment == 0:
            self.window_CREATE_installment = CL_installment(self)
            self.window_CREATE_installment.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CREATE_installment, 'انشاء نظام تقسيط')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_installment.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_installment)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_installment.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_installment)


    def FN_Modify_installment(self):
        if self.window_Modify_installment == 0:
            self.window_Modify_installment = CL_installmentModify(self)
            self.window_Modify_installment.FN_LOAD_Modify()
            self.ui.tabWidget.addTab(self.window_Modify_installment, 'تعديل نظام التقسيط')
            self.ui.tabWidget.setFixedWidth(self.window_Modify_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_installment.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Modify_installment)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Modify_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_installment.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Modify_installment)


    #Active installment program
    def FN_Active_installment(self):

        if self.window_Active_installment == 0:
            self.window_Active_installment = CL_installment_Activation(self)
            self.window_Active_installment.FN_LOAD_Activation()
            self.ui.tabWidget.addTab(self.window_Active_installment, 'تفعيل او ايقاف نظام التقسيط')
            self.ui.tabWidget.setFixedWidth(self.window_Active_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Active_installment.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Active_installment)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_Active_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Active_installment.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_Active_installment)


    def onChange(self):
        if self.ui.tabWidget.currentWidget() == self.window_CreateCoupon:
            self.ui.tabWidget.setFixedWidth(self.window_CreateCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateCoupon.frameGeometry().height() + 20)
        elif self.ui.tabWidget.currentWidget() == self.window_ModifyCoupon:
            self.ui.tabWidget.setFixedWidth(self.window_ModifyCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ModifyCoupon.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_EditCoupon:
            self.ui.tabWidget.setFixedWidth(self.window_EditCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditCoupon.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_PrintCoupon:
            self.ui.tabWidget.setFixedWidth(self.window_PrintCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_PrintCoupon.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Active_installment :
            self.ui.tabWidget.setFixedWidth(self.window_Active_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Active_installment.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Modify_installment:
            self.ui.tabWidget.setFixedWidth(self.window_Modify_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_installment.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_installment:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_installment.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_installment.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Modify_Bank:
            self.ui.tabWidget.setFixedWidth(self.window_Modify_Bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_Bank.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_Bank:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_Bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_Bank.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Parameters:
            self.ui.tabWidget.setFixedWidth(self.window_Parameters.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Parameters.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Customer_Service:
            self.ui.tabWidget.setFixedWidth(self.window_Customer_Service.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Customer_Service.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_LOAD_CHANGE_STATUS_INACTIVE:
            self.ui.tabWidget.setFixedWidth(self.window_LOAD_CHANGE_STATUS_INACTIVE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_LOAD_CHANGE_STATUS_INACTIVE.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_LOAD_CHANGE_STATUS_ACTIVE:
            self.ui.tabWidget.setFixedWidth(self.window_LOAD_CHANGE_STATUS_ACTIVE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_LOAD_CHANGE_STATUS_ACTIVE.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_EditPromVoucher:
            self.ui.tabWidget.setFixedWidth(self.window_EditPromVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditPromVoucher.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CreatePromVoucher:
            self.ui.tabWidget.setFixedWidth(self.window_CreatePromVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreatePromVoucher.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_StoppedVoucher:
            self.ui.tabWidget.setFixedWidth(self.window_StoppedVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_StoppedVoucher.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_EditVoucher :
            self.ui.tabWidget.setFixedWidth(self.window_EditVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_EditVoucher.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CreateVoucher:
            self.ui.tabWidget.setFixedWidth(self.window_CreateVoucher.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateVoucher.frameGeometry().height() + 20)
        elif self.ui.tabWidget.currentWidget() == self.window_SerialCoupon:
            self.ui.tabWidget.setFixedWidth(self.window_SerialCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_SerialCoupon.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_search_reporting1:
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting1.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting1.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_search_reporting:
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_modify_form_item:
            self.ui.tabWidget.setFixedWidth(self.window_modify_form_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_modify_form_item.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_create_form_item:
            self.ui.tabWidget.setFixedWidth(self.window_create_form_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_form_item.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_PRIV:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_PRIV.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_PRIV.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_create_form:
            self.ui.tabWidget.setFixedWidth(self.window_create_form.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_form.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_modify_form:
            self.ui.tabWidget.setFixedWidth(self.window_modify_form.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_modify_form.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_ASSIGN:
            self.ui.tabWidget.setFixedWidth(self.window_ASSIGN.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ASSIGN.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_COPY_ROLE:
            self.ui.tabWidget.setFixedWidth(self.window_COPY_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_COPY_ROLE.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_MODIFY_ROLE:
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_ROLE.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_ROLE:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_ROLE.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_ROLE.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_MODIFY_USER:
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_USER.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_RESET_USER:
            self.ui.tabWidget.setFixedWidth(self.window_RESET_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_RESET_USER.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_COPY_USER:
            self.ui.tabWidget.setFixedWidth(self.window_COPY_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_COPY_USER.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_USER:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_USER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_USER.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_display_item:
            self.ui.tabWidget.setFixedWidth(self.window_display_item.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_display_item.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_create_branch:
            self.ui.tabWidget.setFixedWidth(self.window_create_branch.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_create_branch.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_LOYPOINTS:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_LOYPOINTS.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_LOYPOINTS.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_REDEEMTP:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDEEMTP.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDEEMTP.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_REDITEMGIFT:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEMGIFT.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEMGIFT.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_REDITEMVOUCHER:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEMVOUCHER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEMVOUCHER.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_REDITEM:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_REDITEM.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_REDITEM.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_CUSTTP:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUSTTP.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUSTTP.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_CUSTGP:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUSTGP.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUSTGP.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_UPLOAD_CUST:
            self.ui.tabWidget.setFixedWidth(self.window_UPLOAD_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UPLOAD_CUST.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_DISPLAY_CUST:
            self.ui.tabWidget.setFixedWidth(self.window_DISPLAY_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_DISPLAY_CUST.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_LOYPROG:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_LOYPROG.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_LOYPROG.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_UP_CUST_PT:
            self.ui.tabWidget.setFixedWidth(self.window_UP_CUST_PT.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UP_CUST_PT.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Cust_Card_Edit:
            self.ui.tabWidget.setFixedWidth(self.window_Cust_Card_Edit.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Cust_Card_Edit.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Cust_Card_Add:
            self.ui.tabWidget.setFixedWidth(self.window_Cust_Card_Add.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Cust_Card_Add.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_search_promotion:
            self.ui.tabWidget.setFixedWidth(self.window_search_promotion.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_promotion.frameGeometry().height() + 20)

    def onTabCloseRequested(self, index):
        li = []
        for i in range(self.ui.tabWidget.count()):
            li.append(self.ui.tabWidget.widget(i))
        if self.window_CreateCoupon not in li:
            self.window_CreateCoupon = 0
        if self.window_EditCoupon not in li:
            self.window_EditCoupon = 0
        if self.window_ModifyCoupon not in li:
            self.window_ModifyCoupon = 0
        if self.window_PrintCoupon not in li:
            self.window_PrintCoupon = 0
        if self.window_Active_installment not in li:
            self.window_Active_installment = 0
        if self.window_Modify_installment not in li:
            self.window_Modify_installment = 0
        if self.window_CREATE_installment not in li:
            self.window_CREATE_installment = 0
        if self.window_Modify_Bank not in li:
            self.window_Modify_Bank = 0
        if self.window_CREATE_Bank not in li:
            self.window_CREATE_Bank = 0
        if self.window_Parameters not in li:
            self.window_Parameters = 0
        if self.window_Customer_Service not in li:
            self.window_Customer_Service = 0
        if self.window_LOAD_CHANGE_STATUS_INACTIVE not in li:
            self.window_LOAD_CHANGE_STATUS_INACTIVE = 0
        if self.window_LOAD_CHANGE_STATUS_ACTIVE not in li:
            self.window_LOAD_CHANGE_STATUS_ACTIVE = 0
        if self.window_EditPromVoucher not in li:
            self.window_EditPromVoucher = 0
        if self.window_CreatePromVoucher not in li:
            self.window_CreatePromVoucher = 0
        if self.window_StoppedVoucher not in li:
            self.window_StoppedVoucher = 0
        if self.window_EditVoucher not in li:
            self.window_EditVoucher = 0
        if self.window_CreateVoucher not in li:
            self.window_CreateVoucher = 0
        if self.window_SerialCoupon not in li:
            self.window_SerialCoupon = 0
        if self.window_search_reporting1 not in li:
            self.window_search_reporting1 = 0
        if self.window_search_reporting not in li:
            self.window_search_reporting = 0
        if self.window_search_promotion not in li:
            self.window_search_promotion = 0
        if self.window_modify_form_item not in li:
            self.window_modify_form_item = 0
        if self.window_create_form_item not in li:
            self.window_create_form_item = 0
        if self.window_CREATE_PRIV not in li:
            self.window_CREATE_PRIV = 0
        if self.window_create_form not in li:
            self.window_create_form = 0
        if self.window_modify_form not in li:
            self.window_modify_form = 0
        if self.window_ASSIGN not in li:
            self.window_ASSIGN = 0
        if self.window_COPY_ROLE not in li:
            self.window_COPY_ROLE = 0
        if self.window_MODIFY_ROLE not in li:
            self.window_MODIFY_ROLE = 0
        if self.window_CREATE_ROLE not in li:
            self.window_CREATE_ROLE = 0
        if self.window_MODIFY_USER not in li:
            self.window_MODIFY_USER = 0
        if self.window_RESET_USER not in li:
            self.window_RESET_USER = 0
        if self.window_COPY_USER not in li:
            self.window_COPY_USER = 0
        if self.window_CREATE_USER not in li:
            self.window_CREATE_USER = 0
        if self.window_display_item not in li:
            self.window_display_item = 0
        if self.window_create_branch not in li:
            self.window_create_branch = 0
        if self.window_DISPLAY_LOYPOINTS not in li:
            self.window_DISPLAY_LOYPOINTS = 0
        if self.window_DISPLAY_REDEEMTP not in li:
            self.window_DISPLAY_REDEEMTP = 0
        if self.window_DISPLAY_REDITEMGIFT not in li:
            self.window_DISPLAY_REDITEMGIFT = 0
        if self.window_DISPLAY_REDITEMVOUCHER not in li:
            self.window_DISPLAY_REDITEMVOUCHER = 0
        if self.window_DISPLAY_REDITEM not in li:
            self.window_DISPLAY_REDITEM = 0
        if self.window_DISPLAY_CUSTTP not in li:
            self.window_DISPLAY_CUSTTP = 0
        if self.window_DISPLAY_CUSTGP not in li:
            self.window_DISPLAY_CUSTGP = 0
        if self.window_UPLOAD_CUST not in li:
            self.window_UPLOAD_CUST = 0
        if self.window_DISPLAY_CUST not in li:
            self.window_DISPLAY_CUST = 0
        if self.window_CREATE_LOYPROG not in li:
            self.window_CREATE_LOYPROG = 0
        if self.window_UP_CUST_PT not in li:
            self.window_UP_CUST_PT = 0
        if self.window_Cust_Card_Edit not in li:
            self.window_Cust_Card_Edit = 0
        if self.window_Cust_Card_Add not in li:
            self.window_Cust_Card_Add = 0
        if len(li) == 0:
            self.ui.tabWidget.setFixedWidth(1000)
            self.ui.tabWidget.setFixedHeight(650)

        # self.window_two.show()