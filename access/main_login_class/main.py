from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from access.configuration_class.AssignGroupkey import CL_FNGroupKey
from access.configuration_class.AssignPosGroup import CL_FNGroupPos
from access.configuration_class.AssignPosGroupItem import CL_FNGroupPosItem
from access.configuration_class.Group import CL_FNGroup
from access.configuration_class.GroupItem import CL_ItemGroup
from access.configuration_class.Key import CL_FNKey
from access.configuration_class.Parameters import CL_Parameters
from access.configuration_class.PosWorkingDay import CL_WorkingDay
from access.configuration_class.Pos_Parameter import CL_Pos_Parameters
from access.configuration_class.Check_List import CL_HW_Parameter
from access.configuration_class.List import CL_List
# from access.configuration_class.Parameters import CL_Parameters
from access.configuration_class.List_POS import CL_List_POS
from access.configuration_class.Pos_Parameter_Modify import CL_Pos_Parameters_Modify

from access.coupon_class.CreateCoupon import CL_CreateCoupon
from access.coupon_class.EditCoupon import CL_EditCoupon
from access.coupon_class.StoppedSerial import CL_StoppedSerial
from access.coupon_class.printCoupon import CL_printCoupon
from access.coupon_class.stoppedCoupon import CL_modifyCoupon
#from access.customer_service_class.customer_complain import CL_CustService
from access.loyalty_class.CL_loyPoint import CL_loyPoint
from access.loyalty_class.createCustomer import CL_customer_create
from access.loyalty_class.customerCard import CL_customerCard
from access.loyalty_class.loyalityProg import CL_loyProg
from access.loyalty_class.modifyCustomer import CL_customer_modify
from access.loyalty_class.redeemGift import CL_redGift
from access.loyalty_class.redeemItem import CL_redItem
from access.loyalty_class.redeemType import CL_redeemType
from access.loyalty_class.redeemVoucher import CL_redVouch
from access.loyalty_class.uploadCustomer import CL_customer
from access.master_data_class.BMC import CL_BMC
from access.master_data_class.VAT import CL_VAT
from access.master_data_class.bank import CL_bank
from access.master_data_class.city import CL_city
from access.master_data_class.company import CL_company
from access.master_data_class.branch import CL_branch
from access.master_data_class.district import CL_district
from access.master_data_class.installmentType import CL_installmentType
from access.master_data_class.paymentType import CL_paymentType
from access.master_data_class.posAction import CL_posAction
from access.master_data_class.promotionType import CL_promotionType
from access.master_data_class.sponsor import CL_sponsor
from access.master_data_class.sponsorType import CL_sponsorType
from access.master_data_class.userType import CL_userType
from access.reports_class.customer import CL_customer_report
from access.reports_class.customerFunds import CL_customerFunds
from access.reports_class.installmentRep import CL_installmentReport
from access.reports_class.redeemTypeValue import CL_redeemTypeValue
from access.reports_class.reporting import CL_report
from access.reports_class.Coupon import CL_Coupon

from access.authorization_class.Role import CL_role
#from access.authorization_class.branch import CL_branch
from access.authorization_class.form import CL_form
from access.authorization_class.formItem import CL_formItem
from access.authorization_class.privilage import CL_privilage
from access.authorization_class.user import CL_user
from access.authorization_class.user_module import CL_userModule
# from access.main_login_class.login import  CL_login

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


from access.customer_service_class.modifyCustomerComplain import CL_CustService_modify
from access.customer_service_class.createCustomerComplain import CL_CustService_create

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
            #self.toolBox.setAlignment(QtCore.Qt.AlignRight)
            #self.toolBox.setTextAlignment(QtCore.Qt.AlignCenter)
            #self.toolBox.setTextAlignment(QtCore.Qt.RightToLeft)

            #self.QM_Promotion.setTextAlignment(QtCore.Qt.AlignCenter)
            #self.QM_Promotion.setTextAlignment(QtCore.Qt.AlignRight)


            #self.QM_Promotion.setAlignment(QtCore.Qt.AlignRight)

            # print (CL_userModule.user_name)
            CL_userModule.loadPrivilages(self)
            CL_userModule.FN_AuthBranchUser(self)
            CL_userModule.FN_AuthSectionUser(self)
            CL_userModule.FN_FuncKey(self)
            CL_userModule.FN_userlogin(self)
            for row_number, row_data in enumerate(CL_userModule.myList):
                forms.append(row_data[1])

            forms = list(dict.fromkeys(forms))

            #print(forms)
            for row in forms:
                #print(row)
                but_name = 'QAct_' + row
                self.findChild(QObject, but_name).setEnabled(True)

            self.QAct_Create_User.clicked.connect(self.FN_CREATE_USER)
            self.QAct_Modify_User.clicked.connect(self.FN_MODIFY_USER)
            self.QAct_Copy_User.clicked.connect(self.FN_COPY_USER)
            self.QAct_Reset_User_Password.clicked.connect(self.FN_RESET_USER)
            self.QAct_Assign_User_to_Roles.clicked.connect(self.FN_ASSIGN)
            # print("hi")
            self.QAct_Create_Role.clicked.connect(self.FN_CREATE_ROLE)
            self.QAct_Modify_Role.clicked.connect(self.FN_MODIFY_ROLE)
            self.QAct_Copy_Role.clicked.connect(self.FN_COPY_ROLE)

            self.QAct_Create_Customer.clicked.connect(self.FN_CREATE_CUST)
            self.QAct_Modify_Customer.clicked.connect(self.FN_MODIFY_CUST)
            self.QAct_Upload_Customer.clicked.connect(self.FN_UPLOAD_CUSTOMER)
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
            self.QAct_Report_Promotion_2.triggered.connect(self.FN_search_Coupon)

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

           # self.QAct_Customer_Service.clicked.connect(self.FN_Customer_Service)

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
            self.QAct_HW_Parameter.clicked.connect(self.FN_HW_Parameters)
            self.QAct_List_POS.clicked.connect(self.FN_List_POS)
            self.QAct_List.clicked.connect(self.FN_List)

            self.QAct_Create_Complain.clicked.connect(self.FN_CreateCustomerService)
            self.QAct_Modify_Complain.clicked.connect(self.FN_ModifyCustomerService)

            self.QAct_company.clicked.connect(self.FN_company)
            self.QAct_branch.clicked.connect(self.FN_branch)
            self.QAct_promotionType.clicked.connect(self.FN_promotionType)
            self.QAct_installmentType.clicked.connect(self.FN_installmentType)
            self.QAct_userType.clicked.connect(self.FN_userType)
            self.QAct_paymentType.clicked.connect(self.FN_paymentType)
            self.QAct_sponsorType.clicked.connect(self.FN_sponsorType)
            self.QAct_posAction.clicked.connect(self.FN_posAction)
            self.QAct_VAT.clicked.connect(self.FN_VAT)
            self.QAct_bank.clicked.connect(self.FN_bank)
            self.QAct_city.clicked.connect(self.FN_city)
            self.QAct_district.clicked.connect(self.FN_district)
            self.QAct_BMC.clicked.connect(self.FN_BMC)

            self.QAct_Pos_Parameter.clicked.connect(self.FN_Pos_Parameter)
            self.QAct_Pos_Parameter_Modify.clicked.connect(self.FN_Pos_Parameter_Modify)
            self.QAct_FN_Group.clicked.connect(self.FN_FNGroup)
            self.QAct_FN_Key.clicked.connect(self.FN_FNKey)
            self.QAct_group_key.clicked.connect(self.FN_FNGrouptokey)
            self.QAct_assign_pos.clicked.connect(self.FN_FNGroupPos)
            self.QAct_item_Group.clicked.connect(self.FN_ItemGroup)
            self.QAct_assign_pos_groupitem.clicked.connect(self.FN_FNGroupPositem)
            self.QAct_workingDay.clicked.connect(self.FN_PosWorkingDay)
            self.QAct_copypos.clicked.connect(self.FN_PosWorkingDay)


            self.QAct_sponsor.clicked.connect(self.FN_sponsor)
            #customer reports
            self.QAct_Customer_Details.triggered.connect(self.FN_customer_details_report)
            self.QAct_Customer_Funds.triggered.connect(self.FN_customer_funds_report)
            self.QAct_Redeem_Type_Values.triggered.connect(self.FN_redeem_type_value_rep)
            self.QAct_Installment.triggered.connect(self.FN_installment_rep)
            self.QAct_Exit.clicked.connect(self.FN_exit)

            # self.ui.tabWidget.setTabsClosable(True)
            self.ui.tabWidget.tabCloseRequested.connect(lambda index: self.ui.tabWidget.removeTab(index))

            self.window_Active_installment = 0
            self.window_Modify_installment = 0
            self.window_CREATE_installment = 0
            self.window_Modify_Bank = 0
            self.window_CREATE_Bank = 0
            self.window_Parameters = 0
            #self.window_Customer_Service = 0
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
            self.window_search_cust_rep = 0
            self.window_cust_funds_rep = 0
            self.window_redeem_type_value_rep= 0
            self.window_installment_rep = 0

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
            self.window_CREATE_CUST = 0
            self.window_MODIFY_CUST = 0
            self.window_UPLOAD_CUSTOMER = 0
            self.window_CREATE_LOYPROG = 0
            self.window_UP_CUST_PT = 0
            self.window_Cust_Card_Edit = 0
            self.window_Cust_Card_Add = 0
            self.window_HW_Parameters = 0
            self.window_List_POS = 0
            self.window_List = 0
            self.window_Create_Customer_Service = 0
            self.window_Modify_Customer_Service = 0

            self.window_company = 0
            self.window_branch = 0
            self.window_promotionType =0
            self.window_installmentType = 0
            self.window_userType = 0
            self.window_sponsorType = 0
            self.window_paymentType = 0
            self.window_posAction = 0
            self.window_VAT = 0
            self.window_bank = 0
            self.window_city = 0
            self.window_district = 0
            self.window_BMC = 0
            self.window_posparameter=0
            self.window_FnGroup=0
            self.window_FnKey=0
            self.window_copypos=0

            self.window_FNGroupPos=0
            self.window_posparameter_modify=0
            self.window_ItemGroup=0
            self.window_ItemGrouppos=0
            self.window_PosWorkingDay=0

            self.window_sponsor = 0
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
    def FN_city(self):
        try:
            if self.window_city == 0:
                self.window_city = CL_city()
                self.window_city.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_city, 'المحافطات')
                self.ui.tabWidget.setFixedWidth(self.window_city.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_city.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_city)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_city.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_city.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_city)
        except Exception as err:
         print(err)
    def FN_district(self):
        try:
            if self.window_district == 0:
                self.window_district = CL_district()
                self.window_district.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_district, 'المناطق')
                self.ui.tabWidget.setFixedWidth(self.window_district.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_district.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_district)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_district.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_district.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_district)
        except Exception as err:
         print(err)
    def FN_BMC(self):
        try:
            if self.window_BMC == 0:
                self.window_BMC = CL_BMC()
                self.window_BMC.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_BMC, 'شجره الأصناف')
                self.ui.tabWidget.setFixedWidth(self.window_BMC.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_BMC.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_BMC)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_BMC.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_BMC.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_BMC)
        except Exception as err:
         print(err)
    def FN_company(self):
        try:
            if self.window_company == 0:
                self.window_company = CL_company()
                self.window_company.FN_LOAD_DISPlAY()
                self.ui.tabWidget.addTab(self.window_company, 'الشركات')
                self.ui.tabWidget.setFixedWidth(self.window_company.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_company.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_company)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_company.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_company.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_company)
        except Exception as err:
         print(err)
    def FN_branch(self):
        if self.window_branch == 0:
            self.window_branch = CL_branch()
            self.window_branch.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_branch, 'الفروع')
            self.ui.tabWidget.setFixedWidth(self.window_branch.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_branch.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_branch)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_branch.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_branch.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_branch)

    def FN_promotionType(self):
        if self.window_promotionType == 0:
            self.window_promotionType = CL_promotionType()
            self.window_promotionType.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_promotionType, 'أنواع العروض')
            self.ui.tabWidget.setFixedWidth(self.window_promotionType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_promotionType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_promotionType)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_promotionType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_promotionType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_promotionType)
    def FN_paymentType(self):
        if self.window_paymentType == 0:
            self.window_paymentType = CL_paymentType()
            self.window_paymentType.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_paymentType, 'طرق الدفع')
            self.ui.tabWidget.setFixedWidth(self.window_paymentType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_paymentType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_paymentType)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_paymentType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_paymentType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_paymentType)
    def FN_sponsorType(self):
        if self.window_sponsorType == 0:
            self.window_sponsorType = CL_sponsorType()
            self.window_sponsorType.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_sponsorType, 'أنواع الموردين')
            self.ui.tabWidget.setFixedWidth(self.window_sponsorType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_sponsorType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_sponsorType)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_sponsorType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_sponsorType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_sponsorType)

    def FN_sponsor(self):
        if self.window_sponsor == 0:
            self.window_sponsor = CL_sponsor()
            self.window_sponsor.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_sponsor, 'الموردين')
            self.ui.tabWidget.setFixedWidth(self.window_sponsor.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_sponsor.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_sponsor)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_sponsor.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_sponsor.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_sponsor)
#sdfds
    def FN_VAT(self):
        if self.window_VAT == 0:
            self.window_VAT = CL_VAT()
            self.window_VAT.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_VAT, 'الضريبه')
            self.ui.tabWidget.setFixedWidth(self.window_VAT.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_VAT.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_VAT)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_VAT.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_VAT.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_VAT)

    def FN_bank(self):
        if self.window_bank == 0:
            self.window_bank = CL_bank()
            self.window_bank.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_bank, 'البنوك')
            self.ui.tabWidget.setFixedWidth(self.window_bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_bank.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_bank)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_bank.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_bank)


    def FN_Pos_Parameter(self):
        if self.window_posparameter == 0:
            self.window_posparameter = CL_Pos_Parameters()
            self.window_posparameter.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_posparameter, 'Pos Parameter')
            self.ui.tabWidget.setFixedWidth(self.window_posparameter.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posparameter.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_posparameter)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_posparameter.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posparameter.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_posparameter)


    def FN_FNGroup(self):
        if self.window_FnGroup == 0:
            self.window_FnGroup = CL_FNGroup()
            self.window_FnGroup.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_FnGroup, 'Pos Function Group')
            self.ui.tabWidget.setFixedWidth(self.window_FnGroup.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FnGroup.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FnGroup)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_FnGroup.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FnGroup.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FnGroup)

    def FN_ItemGroup(self):
        if self.window_ItemGroup == 0:
            self.window_ItemGroup = CL_ItemGroup()
            self.window_ItemGroup.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_ItemGroup, 'Pos Item Group')
            self.ui.tabWidget.setFixedWidth(self.window_ItemGroup.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ItemGroup.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_ItemGroup)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_ItemGroup.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_ItemGroup.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_ItemGroup)

    def FN_FNKey(self):
        if self.window_FnKey == 0:
            self.window_FnKey = CL_FNKey()
            self.window_FnKey.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_FnKey, 'Pos Function Key')
            self.ui.tabWidget.setFixedWidth(self.window_FnKey.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FnKey.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FnKey)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_FnKey.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FnKey.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FnKey)

    def FN_FNGroupPos(self):
        if self.window_FNGroupPos == 0:
            self.window_FNGroupPos = CL_FNGroupPos()
            self.window_FNGroupPos.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_FNGroupPos, 'Assign Group to Pos')
            self.ui.tabWidget.setFixedWidth(self.window_FNGroupPos.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FNGroupPos.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FNGroupPos)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_FNGroupPos.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FNGroupPos.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FNGroupPos)

    def FN_FNGroupPositem(self):
        if self.window_FNGroupPos == 0:
            self.window_FNGroupPos = CL_FNGroupPosItem()
            self.window_FNGroupPos.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_FNGroupPos, 'Assign Group to Pos item')
            self.ui.tabWidget.setFixedWidth(self.window_FNGroupPos.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FNGroupPos.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FNGroupPos)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_FNGroupPos.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FNGroupPos.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FNGroupPos)



    def FN_PosWorkingDay(self):
        if self.window_PosWorkingDay == 0:
            self.window_PosWorkingDay = CL_WorkingDay()
            self.window_PosWorkingDay.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_PosWorkingDay, 'Pos Working Day')
            self.ui.tabWidget.setFixedWidth(self.window_PosWorkingDay.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_PosWorkingDay.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_PosWorkingDay)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_PosWorkingDay.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_PosWorkingDay.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_PosWorkingDay)

    def FN_Copypos(self):
        if self.window_copypos == 0:
            self.window_copypos = CL_WorkingDay()
            self.window_copypos.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_copypos, 'Pos Working Day')
            self.ui.tabWidget.setFixedWidth(self.window_copypos.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_copypos.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_copypos)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_copypos.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_copypos.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_copypos)

    def FN_FNGrouptokey(self):
        if self.window_FnKey == 0:
            self.window_FnKey = CL_FNGroupKey()
            self.window_FnKey.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_FnKey, 'Assign Group to key')
            self.ui.tabWidget.setFixedWidth(self.window_FnKey.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FnKey.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FnKey)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_FnKey.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_FnKey.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_FnKey)



    def FN_Pos_Parameter_Modify(self):
        if self.window_posparameter_modify == 0:
            self.window_posparameter_modify = CL_Pos_Parameters_Modify()
            self.window_posparameter_modify.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_posparameter_modify, 'Pos Parameter Modify')
            self.ui.tabWidget.setFixedWidth(self.window_posparameter_modify.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posparameter_modify.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_posparameter_modify)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_posparameter_modify.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posparameter_modify.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_posparameter_modify)

    def FN_posAction(self):
        if self.window_posAction == 0:
            self.window_posAction = CL_posAction()
            self.window_posAction.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_posAction, 'POS Action')
            self.ui.tabWidget.setFixedWidth(self.window_posAction.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posAction.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_posAction)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_posAction.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posAction.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_posAction)

    def FN_installmentType(self):
        if self.window_installmentType == 0:
            self.window_installmentType = CL_installmentType()
            self.window_installmentType.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_installmentType, 'أنواع التقسيط')
            self.ui.tabWidget.setFixedWidth(self.window_installmentType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_installmentType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_installmentType)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_installmentType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_installmentType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_installmentType)

    def FN_userType(self):
        if self.window_userType == 0:
            self.window_userType = CL_userType()
            self.window_userType.FN_LOAD_DISPlAY()
            self.ui.tabWidget.addTab(self.window_userType, 'أنواع المستخدمين')
            self.ui.tabWidget.setFixedWidth(self.window_userType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_userType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_userType)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_userType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_userType.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_userType)

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
            self.window_CREATE_LOYPROG = CL_loyProg()
            self.window_CREATE_LOYPROG.FN_LOAD_DISPLAY()
            self.ui.tabWidget.addTab(self.window_CREATE_LOYPROG, 'انشاء برنامج عضوية')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_LOYPROG.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_LOYPROG.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_LOYPROG)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_LOYPROG.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_LOYPROG.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_LOYPROG)



    def  FN_CREATE_CUST(self):
        # self.onTabCloseRequested_DISPLAY_CUST()
        if self.window_CREATE_CUST == 0:
            self.window_CREATE_CUST = CL_customer_create()
            self.window_CREATE_CUST.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_CREATE_CUST, 'إنشاءعميل')
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_CUST.frameGeometry().height())
            # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested_DISPLAY_CUST)
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_CUST)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_CUST.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_CREATE_CUST)

    def FN_MODIFY_CUST(self):
    # self.onTabCloseRequested_DISPLAY_CUST()
        if self.window_MODIFY_CUST == 0:
            self.window_MODIFY_CUST = CL_customer_modify()
            self.window_MODIFY_CUST.FN_LOAD_MODIFY()
            self.ui.tabWidget.addTab(self.window_MODIFY_CUST, 'تعديل عميل')
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_CUST.frameGeometry().height())
            # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested_DISPLAY_CUST)
            self.ui.tabWidget.setCurrentWidget(self.window_MODIFY_CUST)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_CUST.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_MODIFY_CUST)

    def  FN_UPLOAD_CUSTOMER(self):
        # self.onTabCloseRequested_DISPLAY_CUST()
        if self.window_UPLOAD_CUSTOMER == 0:
            self.window_UPLOAD_CUSTOMER = CL_customer()
            self.window_UPLOAD_CUSTOMER.FN_LOAD_UPLOAD()
            self.ui.tabWidget.addTab(self.window_UPLOAD_CUSTOMER, 'تحميل عملاء')
            self.ui.tabWidget.setFixedWidth(self.window_UPLOAD_CUSTOMER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UPLOAD_CUSTOMER.frameGeometry().height())
            # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested_DISPLAY_CUST)
            self.ui.tabWidget.setCurrentWidget(self.window_UPLOAD_CUSTOMER)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_UPLOAD_CUSTOMER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UPLOAD_CUSTOMER.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_UPLOAD_CUSTOMER)



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


    def FN_search_Coupon(self):
        if self.window_search_reporting1 == 0:
            self.window_search_reporting1 = CL_Coupon()
            self.ui.tabWidget.addTab(self.window_search_reporting1, 'الاستعلام عن كوبونات الخصم')
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting1.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting1.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_search_reporting1)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_search_reporting1.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_reporting1.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_search_reporting1)



    def FN_customer_details_report(self):
        try:
            if self.window_search_cust_rep == 0:
                self.window_search_cust_rep = CL_customer_report()
                self.window_search_cust_rep.FN_LOAD_DISPLAY()
                self.ui.tabWidget.addTab(self.window_search_cust_rep, 'الاستعلام عن بيانات العملاء')
                self.ui.tabWidget.setFixedWidth(self.window_search_cust_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_search_cust_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_search_cust_rep)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_search_cust_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_search_cust_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_search_cust_rep)

        except Exception as err:
             print(err)

    def FN_customer_funds_report(self):
        try:
            if self.window_cust_funds_rep == 0:
                self.window_cust_funds_rep = CL_customerFunds()
                self.window_cust_funds_rep.FN_LOAD_DISPLAY()
                self.ui.tabWidget.addTab(self.window_cust_funds_rep, 'الاستعلام عن أرصده العملاء')
                self.ui.tabWidget.setFixedWidth(self.window_cust_funds_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_cust_funds_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_cust_funds_rep)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_cust_funds_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_cust_funds_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget (self.window_cust_funds_rep )
        except Exception as err:
             print(err)

    def FN_redeem_type_value_rep(self):
        try:
            if self.window_redeem_type_value_rep == 0:
                self.window_redeem_type_value_rep = CL_redeemTypeValue()
                self. window_redeem_type_value_rep.FN_LOAD_DISPLAY()
                self.ui.tabWidget.addTab(self. window_redeem_type_value_rep, 'اعداد و قيم طرق استبدال النقاط')
                self.ui.tabWidget.setFixedWidth(self. window_redeem_type_value_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self. window_redeem_type_value_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self. window_redeem_type_value_rep)
            else:
                self.ui.tabWidget.setFixedWidth(self. window_redeem_type_value_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self. window_redeem_type_value_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self. window_redeem_type_value_rep)
        except Exception as err:
            print(err)


    def FN_installment_rep(self):
        try:
            if self.window_installment_rep == 0:
                self.window_installment_rep = CL_installmentReport()
                self. window_installment_rep.FN_LOAD_DISPLAY()
                self.ui.tabWidget.addTab(self. window_installment_rep, 'اعداد و قيم طرق استبدال النقاط')
                self.ui.tabWidget.setFixedWidth(self. window_installment_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self. window_installment_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self. window_installment_rep)
            else:
                self.ui.tabWidget.setFixedWidth(self. window_installment_rep.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self. window_installment_rep.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self. window_installment_rep)
        except Exception as err:
            print(err)
    def FN_CreateCoupon(self):
        if self.window_CreateCoupon == 0:
            self.window_CreateCoupon = CL_CreateCoupon()
            self.window_CreateCoupon.FN_LOADUI()
            self.ui.tabWidget.addTab(self.window_CreateCoupon, 'انشاء كوبون')
            self.ui.tabWidget.setFixedWidth(self.window_CreateCoupon.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CreateCoupon.frameGeometry().height()+20)
            # self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested_CreateCoupon)
            self.ui.tabWidget.setCurrentWidget(self.window_CreateCoupon)
            # self.n
            # ame = self.ui.tabWidget.currentWidget().objectName()
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

    def FN_CreateCustomerService(self):
        try:
            if self.window_Create_Customer_Service == 0:
                self.window_Create_Customer_Service = CL_CustService_create()
                self.window_Create_Customer_Service.FN_LOAD_CREATE()
                self.ui.tabWidget.addTab(self.window_Create_Customer_Service, 'إنشاء شكوى')
                self.ui.tabWidget.setFixedWidth(self.window_Create_Customer_Service.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_Create_Customer_Service.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_Create_Customer_Service)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_Create_Customer_Service.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_Create_Customer_Service.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_Create_Customer_Service)
        except Exception as err:
            print(err)

    def FN_ModifyCustomerService(self):
        try:
            if self.window_Modify_Customer_Service == 0:
                self.window_Modify_Customer_Service = CL_CustService_modify()
                self.window_Modify_Customer_Service.FN_LOAD_MODIFY()
                self.ui.tabWidget.addTab(self.window_Modify_Customer_Service, 'تعديل شكوى')
                self.ui.tabWidget.setFixedWidth(self.window_Modify_Customer_Service.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_Modify_Customer_Service.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_Modify_Customer_Service)
            else:
                self.ui.tabWidget.setFixedWidth(self.window_Modify_Customer_Service.frameGeometry().width())
                self.ui.tabWidget.setFixedHeight(self.window_Modify_Customer_Service.frameGeometry().height())
                self.ui.tabWidget.setCurrentWidget(self.window_Modify_Customer_Service)
        except Exception as err:
            print(err)
    # Configurations
    def FN_HW_Parameters(self):
        # self.window_two = CL_HW_Parameter()
        # self.window_two.FN_LOAD_CREATE()
        if self.window_HW_Parameters == 0:
            self.window_HW_Parameters = CL_HW_Parameter()
            self.window_HW_Parameters.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_HW_Parameters, 'HW Parameters')
            self.ui.tabWidget.setFixedWidth(self.window_HW_Parameters.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_HW_Parameters.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_HW_Parameters)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_HW_Parameters.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_HW_Parameters.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_HW_Parameters)

    def FN_List(self):
        # self.window_two = CL_List()
        # self.window_two.FN_LOAD_CREATE()
        if self.window_List == 0:
            self.window_List = CL_List()
            self.window_List.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_List, 'List')
            self.ui.tabWidget.setFixedWidth(self.window_List.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_List.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_List)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_List.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_List.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_List)


    def FN_List_POS(self):
        # self.window_two = CL_List_POS()
        # self.window_two.FN_LOAD_CREATE()
        if self.window_List_POS == 0:
            self.window_List_POS = CL_List_POS()
            self.window_List_POS.FN_LOAD_CREATE()
            self.ui.tabWidget.addTab(self.window_List_POS, 'List POS')
            self.ui.tabWidget.setFixedWidth(self.window_List_POS.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_List_POS.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_List_POS)
        else:
            self.ui.tabWidget.setFixedWidth(self.window_List_POS.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_List_POS.frameGeometry().height())
            self.ui.tabWidget.setCurrentWidget(self.window_List_POS)


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
        elif self.ui.tabWidget.currentWidget() == self.window_search_cust_rep:
            self.ui.tabWidget.setFixedWidth(self.window_search_cust_rep.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_search_cust_rep.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_cust_funds_rep:
            self.ui.tabWidget.setFixedWidth(self.window_cust_funds_rep.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_cust_funds_rep.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_installment_rep:
            self.ui.tabWidget.setFixedWidth(self.window_installment_rep.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_installment_rep.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_redeem_type_value_rep:
            self.ui.tabWidget.setFixedWidth(self.window_redeem_type_value_rep.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_redeem_type_value_rep.frameGeometry().height())

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
        elif self.ui.tabWidget.currentWidget() == self.window_CREATE_CUST:
            self.ui.tabWidget.setFixedWidth(self.window_CREATE_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_CREATE_CUST.frameGeometry().height())

        elif self.ui.tabWidget.currentWidget() == self.window_MODIFY_CUST:
            self.ui.tabWidget.setFixedWidth(self.window_MODIFY_CUST.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_MODIFY_CUST.frameGeometry().height())

        elif self.ui.tabWidget.currentWidget() == self.window_UPLOAD_CUSTOMER:
            self.ui.tabWidget.setFixedWidth(self.window_UPLOAD_CUSTOMER.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_UPLOAD_CUSTOMER.frameGeometry().height())

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

        elif self.ui.tabWidget.currentWidget() == self.window_HW_Parameters:
            self.ui.tabWidget.setFixedWidth(self.window_HW_Parameters.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_HW_Parameters.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_List_POS:
            self.ui.tabWidget.setFixedWidth(self.window_List_POS.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_List_POS.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_List:
            self.ui.tabWidget.setFixedWidth(self.window_List.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_List.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Create_Customer_Service:
            self.ui.tabWidget.setFixedWidth(self.window_Create_Customer_Service.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Create_Customer_Service.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_Modify_Customer_Service:
            self.ui.tabWidget.setFixedWidth(self.window_Modify_Customer_Service.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_Modify_Customer_Service.frameGeometry().height())

        elif self.ui.tabWidget.currentWidget() == self.window_company:
            self.ui.tabWidget.setFixedWidth(self.window_company.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_company.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_branch:
            self.ui.tabWidget.setFixedWidth(self.window_branch.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_branch.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_promotionType:
            self.ui.tabWidget.setFixedWidth(self.window_promotionType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_promotionType.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_installmentType:
            self.ui.tabWidget.setFixedWidth(self.window_installmentType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_installmentType.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_userType:
            self.ui.tabWidget.setFixedWidth(self.window_userType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_userType.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_posAction:
            self.ui.tabWidget.setFixedWidth(self.window_posAction.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_posAction.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_paymentType:
            self.ui.tabWidget.setFixedWidth(self.window_paymentType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_paymentType.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_sponsorType:
            self.ui.tabWidget.setFixedWidth(self.window_sponsorType.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_sponsorType.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_VAT:
            self.ui.tabWidget.setFixedWidth(self.window_VAT.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_VAT.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_bank:
            self.ui.tabWidget.setFixedWidth(self.window_bank.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_bank.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_city:
            self.ui.tabWidget.setFixedWidth(self.window_city.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_city.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_district:
            self.ui.tabWidget.setFixedWidth(self.window_district.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_district.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_BMC:
            self.ui.tabWidget.setFixedWidth(self.window_BMC.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_BMC.frameGeometry().height())
        elif self.ui.tabWidget.currentWidget() == self.window_sponsor:
            self.ui.tabWidget.setFixedWidth(self.window_sponsor.frameGeometry().width())
            self.ui.tabWidget.setFixedHeight(self.window_sponsor.frameGeometry().height())
    def onTabCloseRequested(self, index):
        li = []
        for i in range(self.ui.tabWidget.count()):
            li.append(self.ui.tabWidget.widget(i))
        if self.window_CreateCoupon not in li:
            self.window_CreateCoupon = 0
        if self.window_posparameter not in li:
            self.window_posparameter = 0
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
        if self.window_search_cust_rep not in li:
            self.window_search_cust_rep = 0
        if self.window_cust_funds_rep not in li:
            self.window_cust_funds_rep = 0
        if self.window_installment_rep not in li:
                self.window_installment_rep = 0

        if self.window_redeem_type_value_rep not in li:
           self.window_redeem_type_value_rep = 0
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
        if self.window_CREATE_CUST not in li:
            self.window_CREATE_CUST = 0
        if self.window_MODIFY_CUST not in li:
            self.window_MODIFY_CUST = 0
        if self.window_UPLOAD_CUSTOMER not in li:
            self.window_UPLOAD_CUSTOMER = 0
        if self.window_CREATE_LOYPROG not in li:
            self.window_CREATE_LOYPROG = 0
        if self.window_UP_CUST_PT not in li:
            self.window_UP_CUST_PT = 0
        if self.window_Cust_Card_Edit not in li:
            self.window_Cust_Card_Edit = 0
        if self.window_Cust_Card_Add not in li:
            self.window_Cust_Card_Add = 0
        if self.window_Create_Customer_Service not in li:
            self.window_Create_Customer_Service = 0

        if self.window_Modify_Customer_Service not in li:
            self.window_Modify_Customer_Service = 0

        if self.window_company not in li:
            self.window_company = 0
        if self.window_branch not in li:
            self.window_branch = 0
        if self.window_promotionType not in li:
            self.window_promotionType = 0
        if self.window_installmentType not in li:
            self.window_installmentType = 0
        if self.window_userType not in li:
            self.window_userType = 0
        if self.window_sponsorType not in li:
            self.window_sponsorType = 0
        if self.window_VAT not in li:
            self.window_VAT = 0
        if self.window_bank not in li:
            self.window_bank = 0
        if self.window_city not in li:
            self.window_city = 0

        if self.window_BMC not in li:
            self.window_BMC = 0
        if self.window_district not in li:
            self.window_district = 0
        if self.window_paymentType not in li:
            self.window_paymentType = 0
        if self.window_posAction not in li:
            self.window_posAction = 0
        if self.window_sponsor not in li:
            self.window_sponsor = 0
        if self.window_HW_Parameters not in li:
            self.window_HW_Parameters = 0
        if self.window_List_POS not in li:
            self.window_List_POS = 0
        if self.window_List not in li:
            self.window_List = 0
        if self.window_FnGroup not in li:
            self.window_FnGroup = 0
        if self.window_FnKey not in li:
            self.window_FnKey = 0
        if self.window_posparameter_modify not in li:
            self.window_posparameter_modify = 0
        if self.window_ItemGrouppos not in li:
            self.window_posparameter_modify = 0

        if len(li) == 0:
            self.ui.tabWidget.setFixedWidth(1000)
            self.ui.tabWidget.setFixedHeight(650)

        # self.window_two.show()