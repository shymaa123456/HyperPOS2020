
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from data_connection.h1pos import db1
import mysql.connector
from datetime import datetime
from access.authorization_class.user_module import *
from access.main_login_class.main import *
from decimal import Decimal

from access.promotion_class.animation import LoginButton as anim_but





import sys

""" 
# new check-able combo box- in test
class CheckableComboBox(QComboBox):

    # constructor
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

    count = 0

    # action called when item get checked
    def do_action(self):

        CL_create_promotion.label.setText("Checked number : " + str(self.count))

        # when any item get pressed

    def handleItemPressed(self, index):

        # getting the item
        item = self.model().itemFromIndex(index)

        # checking if item is checked
        if item.checkState() == Qt.Checked:

            # making it unchecked
            item.setCheckState(Qt.Unchecked)

            # if not checked
        else:
            # making the item checked
            item.setCheckState(Qt.Checked)

            self.count += 1

            # call the action
            self.do_action()
"""


class CheckableComboBox(QComboBox):
    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()
    def hide(self):
        super().hide()
    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res

    def setChecked(self, index):
        item = self.model().item(index)
        item.setCheckState(Qt.Checked)


class CL_create_promotion(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
    dirname = ''
    query = ""

    def __init__(self):
        super(CL_create_promotion, self).__init__()

        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/promotion_ui'
        self.conn = db1.connect()
        self.prom_idd = ''


        # self.title = QLabel("My Own Bar")
        # self.title.setAlignment(Qt.AlignCenter)

    def FN_LOAD_CREATE_PROM(self):
        filename = self.dirname + '/Promotion_create.ui'
        loadUi(filename, self)
        # self.ui = uic.loadUi( filename )
        # self.ui.closeEvent = self.closeEvent
        # self.ui.show()
        # quit = QAction("Quit", self)
        # quit.triggered.connect(self.closeEvent)

        # self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        # # this will hide the title bar
        # self.setWindowFlag(Qt.FramelessWindowHint)
        #
        # # set the title
        # self.setWindowTitle("no title")
        # self.setWindowFlags(
        #     QtCore.Qt.Window |
        #     QtCore.Qt.CustomizeWindowHint |
        #     QtCore.Qt.WindowTitleHint |
        #     QtCore.Qt.WindowCloseButtonHint |
        #     QtCore.Qt.WindowStaysOnTopHint
        # )
        # Qt.MSWindowsFixedSizeDialogHint
        # Qt.X11BypassWindowManagerHint
        # Qt.FramelessWindowHint
        # Qt.WindowTitleHint
        # Qt.WindowSystemMenuHint
        # Qt.WindowMinimizeButtonHint
        # Qt.WindowMaximizeButtonHint
        # Qt.WindowCloseButtonHint
        # Qt.WindowContextHelpButtonHint
        # Qt.WindowShadeButtonHint
        # Qt.WindowStaysOnTopHint
        # Qt.WindowStaysOnBottomHint
        # Qt.CustomizeWindowHint
        # self.MyInput.textChanged.connect(self.doSomething)
        # # or:
        # self.MyInput.textChanged[str].connect(self.doSomething)

        # self.QLilne_Barcode.textChanged.connect(self.validating)
        #
        # self.QLilne_Barcode.setValidator(self.validating)
        # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        regex = QRegExp("[0-9_]+")
        # regex = QDoubleValidator(-100, 100, 0)
        input_validator = QRegExpValidator(regex)
        # self.QLilne_Barcode.maxLength = 18
        self.QLilne_Barcode.setValidator(input_validator)

        ###############################################################################
        # ### restrict date minimum  ###
        ###############################################################################
        datefrom = str(datetime.today().strftime('%Y-%m-%d'))
        xfrom = datefrom.split("-")
        d = QDate(int(xfrom[0]), int(xfrom[1]), int(xfrom[2]))
        self.Qdate_from.setMinimumDate(d)
        self.Qdate_to.setMinimumDate(d)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        # self.LE_desc_5.setEnabled(False)
        ###############################################################################
        ###############################################################################

        ###########test Qbtn_search animation#############################################################

        self.Qbtn_search = anim_but(self)
        self.Qbtn_search.setMinimumSize(60, 5)
        self.Qbtn_search.setGeometry(10, 30, 127, 23)
        self.Qbtn_search.setText('بحث')
        self.Qbtn_search.setShortcut('Ctrl+D')  # shortcut key
        # self.Qbtn_search.setToolTip("search")  # Tool tip

        self.Qbtn_add = anim_but(self)
        self.Qbtn_add.setMinimumSize(60, 5)
        self.Qbtn_add.setGeometry(10, 180, 127, 23)
        self.Qbtn_add.setText('اضافة')


        self.Qbtn_remove = anim_but(self)
        self.Qbtn_remove.setMinimumSize(60, 5)
        self.Qbtn_remove.setGeometry(10, 220, 127, 23)
        self.Qbtn_remove.setText('ازالة')



        self.Qbtn_add_list = anim_but(self)
        self.Qbtn_add_list.setMinimumSize(60, 5)
        self.Qbtn_add_list.setGeometry(10, 70, 127, 23)
        self.Qbtn_add_list.setText('تحميل اصناف')

        self.Qbtn_exit = anim_but(self)
        self.Qbtn_exit.setMinimumSize(60, 5)
        self.Qbtn_exit.setGeometry(10, 560, 131, 23)
        self.Qbtn_exit.setText('خروج')

        self.Qbtn_save = anim_but(self)
        self.Qbtn_save.setMinimumSize(60, 5)
        self.Qbtn_save.setGeometry(190, 560, 131, 23)
        self.Qbtn_save.setText('حفظ بيانات العرض')

        ###############################################################################

        """ checked combobox sample >>> Branch"""
        self.Qcombo_branch2 = CheckableComboBox(self)
        self.Qcombo_branch2.setGeometry(621, 44, 179, 18)
        self.Qcombo_branch2.setLayoutDirection(Qt.RightToLeft)
        self.Qcombo_branch2.setStyleSheet("background-color: rgb(198, 207, 199)")
        # self.Qcombo_branch.hide()


        """ checked combobox sample """
        self.Qcombo_cust_group2 = CheckableComboBox(self)
        self.Qcombo_cust_group2.setGeometry(621, 68, 179, 18)
        self.Qcombo_cust_group2.setLayoutDirection(Qt.RightToLeft)  # RightToLeft)
        # self.Qcombo_cust_group2.lineEdit().setAlignment(Qt.AlignRight)
        self.Qcombo_cust_group2.setStyleSheet("background-color: rgb(198, 207, 199)")
        # self.Qcombo_cust_group.hide()

        """ checked combobox sample >>> sponsor"""
        self.Qcombo_sponsor2 = CheckableComboBox(self)
        self.Qcombo_sponsor2.setGeometry(621, 92, 179, 18)
        self.Qcombo_sponsor2.setLayoutDirection(Qt.RightToLeft)
        self.Qcombo_sponsor2.setStyleSheet("background-color: rgb(198, 207, 199)")
        # self.Qcombo_sponsor.hide()

        # Set Style
        # self.label_num.setStyleSheet(label_num)
        # self.label_2.setStyleSheet(desc_5)
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())

        try:

            self.FN_GET_Company()
            self.FN_GET_Branch()
            self.FN_GET_CustomerGroup()
            self.FN_GET_sponser()
            self.FN_GET_promotion_type()
            self.FN_GET_department()
            self.updatestatecombo()
            self.FN_GET_MAGAZINE()

            self.Qcombo_sponsor2.activated.connect(self.handleActivated)
            # self.Qcombo_sponsor2.currentIndexChanged().connect(self.handleActivated)

            # Qcombo_promotion = self.Qcombo_promotion.itemData(self.Qcombo_promotion.currentIndex())  # promotion type id
            # self.Qcombo_promotion.activated.connect(self.Qcombo_promotion_index)
            # print(Qcombo_promotion)
            # department
            self.Qcombo_department.activated[str].connect(self.updatestatecombo)

            self.tableWidget.setRowCount(0)
            self.Qtable_promotion.setRowCount(0)

            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)

            #  SEARCH BUTTON
            self.Qbtn_search.clicked.connect(self.FN_SEARCH_BARCODES)  # search barcodes
            self.QcheckBox_all.stateChanged.connect(self.changeTitle)  # select all
            self.Qbtn_add.clicked.connect(self.add_items)  # add_items  to Qtable_promotion datatable
            self.Qbtn_remove.clicked.connect(self.remove_selected)  # remove items from Qtable_promotion datatable

            # save promotion
            self.Qbtn_save.clicked.connect(self.save_items)  # create promotion items


        except:
            print("An exception occurred")




    def save_items(self):
        if self.Qtable_promotion.rowCount() < 1:
            print("test")
            QMessageBox.information(self, 'Message', "Revise", QMessageBox.Close)
        else:
            self.prom_idd = self.get_id()  # last promotion number
            if self.prom_idd == "-10":
                QMessageBox.information(self, 'Connection', "Error Connection", QMessageBox.Close)
            else:
                # for row in range(self.Qtable_promotion.rowCount()):
                #     for column in range(self.Qtable_promotion.columnCount()):
                #         item = self.Qtable_promotion.item(row, column).text()
                #         print(f'row: {row}, column: {column}, item={item}')

                self.prom_idd += 1
                self.save_promotion()
                self.Qline_promotion.setText(str(self.prom_idd))

    def save_promotion(self):
        try:
            self.conn = db1.connect()
            self.conn.autocommit = False
            mycursor = self.conn.cursor()
            self.conn.start_transaction()

            ####   loop at table data
            # roows = self.Qtable_promotion.rowCount()
            # columns = self.Qtable_promotion.columnCount()
            # column = 1
            # rowCount() This property holds the number of rows in the table
            # print("test2")

            #  FIXED DATA
            comb_promotion = self.Qcombo_promotion.itemData(self.Qcombo_promotion.currentIndex())  # promotion type id
            creationDate = QDate.currentDate().toString(Qt.ISODate)
            # creationDate = str(datetime.today().strftime('%d-%m-%Y'))
            SPONSER_ID = self.Qcombo_sponsor2.itemData(self.Qcombo_sponsor2.currentIndex())

            #
            # # lock table for new record:
            sql0 = "  LOCK  TABLES    Hyper1_Retail.PROMOTION_HEADER   WRITE , " \
                   "    Hyper1_Retail.PROMOTION_DETAIL   WRITE  "
            mycursor.execute(sql0)

            # create promotion in header
            sql1 = "  insert into Hyper1_Retail.PROMOTION_HEADER " \
                   "  ( PROM_ID , PROM_TYPE_ID ,  PROM_START_DATE , PROM_END_DATE , " \
                   "  PROM_NO_OF_USAGE_PER_DAY , PROM_CREATED_BY , PROM_CREATED_ON ,     " \
                   "  COUPON_ID , MAGAZINE_ID , PROMV_VOUCHER_ID , PROM_MIN_RCT_VAL ,PROM_MAX_DISC_VAL ,PROM_STATUS ) " \
                   "  VALUES (  %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s )"
            # self.Qdate_from.dateTime().toString('dd-MM-yyyy'),
            # self.Qdate_to.dateTime().toString('dd-MM-yyyy'),
            val = (self.prom_idd, comb_promotion,
                   self.Qdate_from.dateTime().toString('yyyy-MM-dd'),
                   self.Qdate_to.dateTime().toString('yyyy-MM-dd'),
                   "100", CL_userModule.user_name, creationDate,
                   "0", "0", "0", "100", "100", "0")

            mycursor.execute(sql1, val)



            PROM_LINE_NO = 0
            for row in range(self.Qtable_promotion.rowCount()):
                PROM_LINE_NO += 10

                # for column in range(self.Qtable_promotion.columnCount()):
                #     _item = self.Qtable_promotion.item(row, column)
                #     if _item:
                #        item = self.Qtable_promotion.item(row, column).text()

                       # print(f'row: {row}, column: {column}, item={item}')
                # " SELECT BMC_ID ,POS_GTIN ,  POS_ITEM_NO ,  POS_UOM, POS_GTIN_DESC_A ,POS_SELL_PRICE, POS_VATRATE ,"
                # " '' , '' , 1 , 0 from Hyper1_Retail.POS_ITEM  where POS_GTIN = '" + barcode + "'")
                # self.Qtable_promotion.setHorizontalHeaderLabels(['القسم الفرعى', 'الباركود', 'رقم الصنف', 'وحدة القياس',
                #                                                  'الوصف', 'سعر الصنف قبل الخصم', 'نسبة الضريبة',
                #                                                  'نوع الخصم'
                #                                                     , 'نسبة/قيمة الخصم', 'الكمية بسعر الخصم',
                #                                                  'كمية العرض'])
                BMC_ID = self.Qtable_promotion.item(row, 0).text()
                POS_GTIN = self.Qtable_promotion.item(row, 1).text()
                POS_ITEM_NO = self.Qtable_promotion.item(row, 2).text()
                POS_UOM = self.Qtable_promotion.item(row, 3).text()
                POS_GTIN_DESC_A = self.Qtable_promotion.item(row, 4).text()
                POS_SELL_PRICE = self.Qtable_promotion.item(row, 5).text().strip()
                POS_VATRATE = self.Qtable_promotion.item(row, 6).text()
                PROM_DISCOUNT_FLAG = self.Qtable_promotion.item(row, 7).text()

                if self.Qtable_promotion.item(row, 8).text().strip() == '':
                    PROM_ITEM_DISCOUNT = '0.0'
                else:
                    PROM_ITEM_DISCOUNT = self.Qtable_promotion.item(row, 8).text().strip()

                PROM_ITEM_QTY = self.Qtable_promotion.item(row, 9).text()
                PROM_MAX_DISC_QTY = self.Qtable_promotion.item(row, 10).text()
                if PROM_ITEM_DISCOUNT is None or PROM_ITEM_DISCOUNT == '':
                    PROM_ITEM_PRICE = Decimal(POS_SELL_PRICE)
                else:
                    PROM_ITEM_PRICE = Decimal(POS_SELL_PRICE) + Decimal(PROM_ITEM_DISCOUNT)




                # create promotion in details
                sql2 = "  insert into Hyper1_Retail.PROMOTION_DETAIL " \
                       "  ( PROM_ID , PROM_LINE_NO , POS_ITEM_NO, POS_GTIN , BMC_ID , SPONSER_ID  , " \
                       "    PROM_START_DATE , PROM_END_DATE , PROM_STATUS , " \
                       "    PROM_CREATED_BY , PROM_CREATED_ON  , PROM_DISCOUNT_FLAG  , PROM_ITEM_DISCOUNT  ,    " \
                       "    PROM_GROUP_NO , PROM_ITEM_PRICE  ) " \
                       "  VALUES ( %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  )"

                val2 = (self.prom_idd, PROM_LINE_NO, POS_ITEM_NO, POS_GTIN, BMC_ID , SPONSER_ID  ,
                       self.Qdate_from.dateTime().toString('yyyy-MM-dd'),
                       self.Qdate_to.dateTime().toString('yyyy-MM-dd'), "0",
                        CL_userModule.user_name, creationDate , "egp" , PROM_ITEM_DISCOUNT , "1" , PROM_ITEM_PRICE
                        )
                mycursor.execute(sql2, val2)
            # self.Qdate_from.dateTime().toString('dd-MM-yyyy'),
            # self.Qdate_to.dateTime().toString('dd-MM-yyyy'), "0",

            #  # create promotion in details
            # sql2 = " insert into Hyper1_Retail.PROMOTION_DETAIL " \
            #       "         VALUES ( %s, %s, %s,  %s,%s)"
            #
            # val = (self.prom_idd, name, points, nextLevel1, status
            #        )
            # mycursor.execute(sql2, val)

            # # unlock table :
            sql00 = "  UNLOCK   tables    "
            mycursor.execute(sql00)
            self.conn.commit()

        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            # reverting changes because of exception
            self.conn.rollback()
        finally:
            # closing database connection.
            if self.conn.is_connected():
                mycursor.close()
                self.conn.close()
                print("connection is closed")

    def get_id(self):

        try:
            self.conn = db1.connect()
            mycursor = self.conn.cursor()
            mycursor.execute("SELECT max(PROM_ID) FROM Hyper1_Retail.PROMOTION_HEADER ")
            records = mycursor.fetchone()
            print(records)
            if records[0] == None:
                return 0
            else:
                return records[0]

        except mysql.connector.Error as error:
            print("Failed to get record from database : {}".format(error))
            return "-10"

        finally:
            # closing database connection.
            if self.conn.is_connected():
                mycursor.close()
                self.conn.close()
                print("connection is closed")
    # def Qcombo_promotion_index(self, index):
    #     print(self.Qcombo_promotion.itemText(index))
    #     print(self.Qcombo_promotion.itemData(index))
    #     Qcombo_promotion = self.Qcombo_promotion.itemData(self.Qcombo_promotion.currentIndex())
    #     print(Qcombo_promotion)
    #####################################
    # def closeEvent(self, event):
    #     """Generate 'question' dialog on clicking 'X' button in title bar.
    #
    #     Reimplement the closeEvent() event handler to include a 'Question'
    #     dialog with options on how to proceed - Save, Close, Cancel buttons
    #     """
    #     reply = QMessageBox.question(
    #         self, "Message",
    #         "Are you sure you want to quit? Any unsaved work will be lost.",
    #         QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
    #         QMessageBox.Save)
    #     # QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
    #     # QMessageBox.Save)
    #
    #     if reply == QMessageBox.Close:
    #         QCoreApplication.exit(0)
    #     else:
    #         pass
    #
    # def keyPressEvent(self, event):
    #     """Close application from escape key.
    #
    #     results in QMessageBox dialog from closeEvent, good but how/why?
    #     """
    #     if event.key() == Qt.Key_Escape:
    #         self.close()
    #####################################
    def closeEvent(self, event):
        print("event")
        reply = QMessageBox.question(self, 'Message',
                                           "Are you sure to quit promotion?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def add_items(self):     # add_items to Qtable_promotion datatable

        rowPosition = self.Qtable_promotion.rowCount()
        # Qtable_promotion.insertRow(rowPosition)
        # Qtable_promotion.setItem(rowPosition, 0, QtGui.QTableWidgetItem("text1"))
        # Qtable_promotion.setItem(rowPosition, 1, QtGui.QTableWidgetItem("text2"))
        # Qtable_promotion.setItem(rowPosition, 2, QtGui.QTableWidgetItem("text3"))

        # self.Qtable_promotion.setRowCount(0)
        self.Qtable_promotion.setColumnCount(11)
        self.Qtable_promotion.setHorizontalHeaderLabels(['القسم الفرعى', 'الباركود', 'رقم الصنف', 'وحدة القياس',
                                                         'الوصف', 'سعر الصنف قبل الخصم', 'نسبة الضريبة', 'نوع الخصم'
                                                                ,'نسبة/قيمة الخصم', 'الكمية بسعر الخصم', 'كمية العرض'])

        # self.conn = db1.connect()
        # mycursor = self.conn.cursor()
        # mycursor.execute(
        #     " SELECT BMC_ID ,POS_GTIN ,  POS_ITEM_NO ,  POS_UOM, POS_GTIN_DESC_A ,POS_SELL_PRICE, POS_VATRATE ,"
        #     " '' , '' , 1 , 0 from Hyper1_Retail.POS_ITEM   ")
        # # mycursor.execute("SELECT * from Hyper1_Retail.POS_ITEM   ")
        #
        # # print(self.query)
        # records = mycursor.fetchall()
        # # print(records)
        # headers = []
        # for row_number, row_data in enumerate(records):
        #     # self.Qtable_promotion.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #     headers.append(row_data)
        #     self.Qtable_promotion.insertRow(row_number)
        #     for column_number, data in enumerate(row_data):
        #         self.Qtable_promotion.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        #         if column_number not in {8, 9, 10}:
        #             self.Qtable_promotion.item(row_number, column_number).setFlags(QtCore.Qt.ItemFlags
        #                                                                       (~QtCore.Qt.ItemIsEditable))
        #         # else:
        #         #     self.Qtable_promotion.item(row_number, column_number).setFlags(QtCore.Qt.ItemFlags
        #         #                                                               (QtCore.Qt.ItemIsSelectable |
        #         #                                                                QtCore.Qt.ItemIsEditable |
        #         #                                                                QtCore.Qt.ItemIsEnabled))
        #
        #     self.Qtable_promotion.resizeColumnsToContents()  # item(0, 1).EditTriggers
        #     # self.Qtable_promotion.setSortingEnabled(True)
        #     # self.tableWidget.wordWrap()
        #     self.Qtable_promotion.setCornerButtonEnabled(False)
        #     mycursor.close()

        indexes = self.tableWidget.selectionModel().selectedRows()
        # print(str(indexes))
        rowcountz = self.Qtable_promotion.rowCount()
        print(rowcountz)
        if not indexes:
            print("select row first")
        else:
            for index in sorted(indexes) :
                print('Row %d is selected' % index.row())
                # rowcount = self.Qtable_promotion.rowCount()
                print(rowcountz)

                # self.Qtable_promotion.insertRow(rowcount)
                # column_number = self.Qtable_promotion.columnCount()
                row = index.row()
                print(row)
                # barcode = self.tableWidget.data(row, 1)
                barcode = index.sibling(index.row(), 0).data()
                print(barcode)

                self.conn = db1.connect()
                mycursor = self.conn.cursor()
                mycursor.execute(
                    " SELECT BMC_ID ,POS_GTIN ,  POS_ITEM_NO ,  POS_UOM, POS_GTIN_DESC_A ,POS_SELL_PRICE, POS_VATRATE ,"
                    " '' , '' , 1 , 0 from Hyper1_Retail.POS_ITEM  where POS_GTIN = '" + barcode + "'")

                records = mycursor.fetchall()
                # print(self.query)
                # print(records)
                headers = []
                for row_number, row_data in enumerate(records):
                    headers.append(row_data)
                    self.Qtable_promotion.insertRow(rowcountz)
                    for column_number, data in enumerate(row_data):
                        self.Qtable_promotion.setItem(rowcountz, column_number, QTableWidgetItem(str(data)))

                        if column_number not in {8, 9, 10}:
                            self.Qtable_promotion.item(rowcountz, column_number).setFlags(QtCore.Qt.ItemFlags
                                                                                           (~QtCore.Qt.ItemIsEditable))
                    mycursor.close()
                    rowcountz += 1

        # clear selected
        # ind = len(indexes)
        # self.delete_rows()
        # index1 = self.tableWidget.selectedRanges()
        # print(index1)
        for index in reversed(sorted(indexes)):
            # ind -= 1
            # row = index.row()
            # print(row)
            # print(ind)
            # # if ind >= 0:
            # #     pass
            # # else:
            self.tableWidget.removeRow(index.row())
            # selRanges = self.tableWidget.selectedRanges
            # self.tableWidget.removeRow(selRanges)
        self.Qtable_promotion.resizeColumnsToContents()  # item(0, 1).EditTriggers
        self.Qtable_promotion.setCornerButtonEnabled(False)
        # rowcount = self.Qtable_promotion.rowCount()
        # print(rowcountz)

        if self.QcheckBox_all.isChecked():
            self.QcheckBox_all.setChecked(False)

    # for index in sorted(self.tableView5.selectionModel().selectedRows()):
        #     row = index.row()
        #     name = self.table_model5.data(self.table_model5.index(row, 0))
        #     email = self.table_model5.data(self.table_model5.index(row, 1))
        #     identity.append((name, email))
        #     names.append(name)
        #     emails.append(email)

    def remove_selected(self):## remove barcode from promotion
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to delete barcode from promotion?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            indexes = self.Qtable_promotion.selectionModel().selectedRows()
            for index in reversed(sorted(indexes)):
                self.Qtable_promotion.removeRow(index.row())

    def iterate(self):  # delete duplicated barcodes from search
        #column = 1
        # Qtable_promotion
        for row_prom in range(self.Qtable_promotion.rowCount()):
            _item_prom = self.Qtable_promotion.item(row_prom, 1)
            if _item_prom:
                item_prom = self.Qtable_promotion.item(row_prom, 1).text()
                for index_search in reversed(range(self.tableWidget.rowCount())):
                    _item_search = self.tableWidget.item(index_search, 0)  # barcode in search
                    if _item_search:
                        item_search = self.tableWidget.item(index_search, 0).text()
                        if item_prom == item_search:
                            self.tableWidget.removeRow(index_search)#.row())

        # #        for item in self.table_widget.items():
        #
        # column = 0
        # # rowCount() This property holds the number of rows in the table
        # for row in range(self.tableWidget.rowCount()):
        #  # item(row, 0) Returns the item for the given row and column if one has been set; otherwise returns nullptr.
        #     _item = self.tableWidget.item(row, column)
        #     if _item:
        #         item = self.tableWidget.item(row, column).text()
        #         print(f'row: {row}, column: {column}, item={item}')

    # def delete_rows_duplicate(self):
    #
    #     if self.tableWidget.selectionModel().hasSelection():
    #         indexes = [QPersistentModelIndex(index) for index in self.tableWidget.selectionModel().selectedRows()]
    #         maxrow = max(indexes, key=lambda x: x.row()).row()
    #         next_ix = QPersistentModelIndex(self.QSModel.index(maxrow + 1, 0))
    #         for index in indexes:
    #             print('Deleting row %d...' % index.row())
    #             self.QSModel.removeRow(index.row())
    #         self.tableWidget.setCurrentIndex(QModelIndex(next_ix))
    #     else:
    #         print('No row selected!')
    #
    #
    # def delete_rows(self):
    #     if self.tableWidget.selectionModel().hasSelection():
    #         indexes = [QPersistentModelIndex(index) for index in self.tableWidget.selectionModel().selectedRows()]
    #         maxrow = max(indexes, key=lambda x: x.row()).row()
    #         next_ix = QPersistentModelIndex(self.QSModel.index(maxrow + 1, 0))
    #         for index in indexes:
    #             print('Deleting row %d...' % index.row())
    #             self.QSModel.removeRow(index.row())
    #         self.tableWidget.setCurrentIndex(QModelIndex(next_ix))
    #     else:
    #         print('No row selected!')
    #
    #     # if self.tableWidget.selectionModel().hasSelection():
    #     #     indexes = [QPersistentModelIndex(index) for index in self.tableWidget.selectionModel().selectedRows()]
    #     #     for index in indexes:
    #     #         print('Deleting row %d...' % index.row())
    #     #         self.QSModel.removeRow(index.row())
    #     # else:
    #     #     print('No row selected!')

    def changeTitle(self):    # select table rows
        if self.QcheckBox_all.isChecked():
            self.tableWidget.selectAll()
            self.tableWidget.setFocus()
        else:
            self.tableWidget.clearSelection()

        #     rowsCount = self.tableWidget.rowCount()
        #     # print(rowsCount)
        #     for rows in range(rowsCount):
        #         self.tableWidget.selectRow(rows)

    # SEARCH BUTTON # FILL SERCH DATA TABLE  >> tableWidget
    def FN_SEARCH_BARCODES(self):
        # self.Qbtn_search.setEnabled(False)
        self.tableWidget.clearSelection() # clear selection
        self.QcheckBox_all.setChecked(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        # self.tableWidget.setHorizontalHeaderLabels(['DEPARTMENT_ID', 'DEPARTMENT_DESC', 'DEPARTMENT_STATUS', 'test'])
        #
        self.tableWidget.setHorizontalHeaderLabels(['الباركود', 'رقم الصنف',  'القسم الفرعى', 'وحدة القياس', 'الوصف'] )

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute(
            " SELECT POS_GTIN ,  POS_ITEM_NO , BMC_ID , POS_UOM, POS_GTIN_DESC_A  from Hyper1_Retail.POS_ITEM   ")
        # mycursor.execute("SELECT * from Hyper1_Retail.POS_ITEM   ")

        # print(self.query)
        records = mycursor.fetchall()
        # print(records)
        headers = []
        for row_number, row_data in enumerate(records):
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            headers.append(row_data)
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.tableWidget.resizeColumnsToContents()  # item(0, 1).EditTriggers
            self.tableWidget.setSortingEnabled(True)
            # self.tableWidget.wordWrap()
            self.tableWidget.setCornerButtonEnabled(False)
            mycursor.close()

        self.iterate()
        # self.Qbtn_search.ff = '1'
        # self.Qbtn_search.setEnabled(True)
        # self.Qbtn_search.ff = '2'
        #


    def FN_SEARCH_BARCODES_test(self):

        # model = QStandardItemModel()
        # model.setHorizontalHeaderLabels(['DEPARTMENT_ID', 'DEPARTMENT_DESC', 'DEPARTMENT_STATUS'])
        #
        # self.Qtable_promotion.setModel(model)
        # header = self.Qtable_promotion.horizontalHeader()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        # self.tableWidget.setHorizontalHeaderLabels(['DEPARTMENT_ID', 'DEPARTMENT_DESC', 'DEPARTMENT_STATUS', 'test'])
        #
        self.tableWidget.setHorizontalHeaderLabels(['GTIN', 'ITEM_NO', 'GTIN_DESC', 'VATRATE', 'UOM'])

        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        # mycursor.execute("SELECT  DEPARTMENT_ID, DEPARTMENT_DESC , DEPARTMENT_STATUS , '1' FROM DEPARTMENT")
        #
        mycursor.execute(" SELECT POS_GTIN ,  POS_ITEM_NO , POS_GTIN_DESC_A , POS_VATRATE , POS_UOM from Hyper1_Retail.POS_ITEM   ")
        # mycursor.execute("SELECT * from Hyper1_Retail.POS_ITEM   ")
        print(self.query)
        records = mycursor.fetchall()
        print(records)
        headers = []
        for row_number, row_data in enumerate(records):
            # self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            headers.append(row_data)
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                if column_number == 0 or column_number == 1  or column_number == 2 :
                    self.tableWidget.item(row_number, column_number).setFlags(QtCore.Qt.ItemFlags
                                                                              (QtCore.Qt.ItemIsEditable))
                else:

                    self.tableWidget.item(row_number, column_number).setFlags(QtCore.Qt.ItemFlags
                                                                              (~QtCore.Qt.ItemIsSelectable |
                                                                               ~QtCore.Qt.ItemIsEditable |
                                                                               ~QtCore.Qt.ItemIsEnabled))

            self.tableWidget.resizeColumnsToContents() #item(0, 1).EditTriggers
            self.tableWidget.setSortingEnabled(True)
            # self.tableWidget.item(0, 1).setFlags(QtCore.Qt.ItemFlags)
            # self.tableWidget.item(2, 1).setFlags(Qt.NoItemFlags)
            # self.tableWidget.item(1, 1).setFlags(Qt.NoItemFlags)
            # self.tableWidget.selectRow(1)
            # self.tableWidget.wordWrap()
            self.tableWidget.setCornerButtonEnabled(False)
            # self.tableWidget.column(2).setEditTriggers(QtWidgets.QTableWidget.EditTriggers)
            # flags = self.tableWidget.QTableWidgetItem.ItemFlags
            # flags |= Qt::ItemIsSelectable | Qt::ItemIsEditable; // set the flag ItemIsEnabled
            # self.tableWidget.item(0, 1).setFlags(QtCore.Qt.ItemIsSelectable |
            #                                      QtCore.Qt.ItemIsEditable |
            #                                      QtCore.Qt.ItemIsEnabled)
        # self.tableWidget.item(0, 1).setFlags(Qt.ItemIsEditable)
        mycursor.close()
        # item = QTableWidgetItem()
        # item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        # tableName.setItem(row, column, item)


    def FN_GET_Company(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM COMPANY")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_company.addItems(row)
        mycursor.close()

    def FN_GET_Branch(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT BRANCH_DESC_A FROM BRANCH")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_branch2.addItems(row)
        mycursor.close()

    def FN_GET_CustomerGroup(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT CG_DESC FROM CUSTOMER_GROUP")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            # self.Qcombo_cust_group.addItems(row)
            self.Qcombo_cust_group2.addItems(row)
        mycursor.close()

    def FN_GET_MAGAZINE(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT MAGAZINE_DESC FROM MAGAZINE")
        records = mycursor.fetchall()
        print(records)
        for row in records:
            self.Qcombo_magazine.addItems(row)
        mycursor.close()

    def FN_GET_sponser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SPONSER_NAME , SPONSER_ID FROM SPONSER WHERE SPONSER_STATUS = '1' ")
        records = mycursor.fetchall()
        print(records)
        for row, VAL in records:
            # self.Qcombo_sponsor2.addItems(row)
            self.Qcombo_sponsor2.addItem(row, VAL)
            self.Qline_promotion.text = VAL
        mycursor.close()

        ##################################################
        # ##  test data
        # # self.Qtable_promotion.
        #
        # # data = 'Recordset back from postgis'
        # nb_row = len(records)
        # nb_col = 3
        # self.Qtable_promotion.setRowCount(nb_row)
        # self.Qtable_promotion.setColumnCount(nb_col)
        #
        # combo_box_options = ["Option", "Option 2: val", "Option 3: val"]
        # combo = QComboBox()
        # for t in combo_box_options:
        #     combo.addItem(t)
        #
        # for row in range(nb_row):
        #     for col in range(nb_col-1):
        #         item = QTableWidgetItem(str(records[row][col]))
        #         self.Qtable_promotion.setItem(row, col, item)
        #
        #     # self.Qtable_promotion.setCellWidget(row, 2, combo)
        #     # combo.setCurrentIndex(1)
        # # self.Qtable_promotion.setHorizontalHeaderLabels([u'Column1', u'Column2'])
        #
        # self.Qtable_promotion.setHorizontalHeaderLabels([u'SPONSER_NAME', u'SPONSER_ID', u'combo'])
        # self.Qtable_promotion.cellClicked.connect(self.cell_was_clicked)
        #
        # self.Qtable_promotion.resizeColumnsToContents()
        #
        # ##################################################
        #
        # # self.table = QtGui.QTableWidget()
        # # self.table.setColumnCount(3)
        # # self.setCentralWidget(self.table)
        # # data1 = ['row1', 'row2', 'row3', 'row4']
        # # data2 = ['1', '2.0', '3.00000001', '3.9999999']
        # # combo_box_options = ["Option 1", "Option 2", "Option 3"]
        #
        # # self.table.setRowCount(4)
        #
        # # for index in range(nb_row):
        # #     # item1 = QtGui.QTableWidgetItem(data1[index])
        # #     # self.table.setItem(index, 0, item1)
        # #     # item2 = QtGui.QTableWidgetItem(data2[index])
        # #     # self.table.setItem(index, 1, item2)
        # #     combo = QtGui.QComboBox()
        # #     for t in combo_box_options:
        # #         combo.addItem(t)
        # #     self.Qtable_promotion.setCellWidget(index, 2, combo)
        #
        #     ##################################################

    def handleActivated(self, index):
        print(self.Qcombo_sponsor2.itemText(index))
        print(self.Qcombo_sponsor2.itemData(index))
        QMessageBox.about(self, self.Qcombo_sponsor2.itemText(index), self.Qcombo_sponsor2.itemData(index))

    def cell_was_clicked(self, row, column):
        # index = self.Qtable_promotion.currentIndex()
        # NewIndex = self.Qtable_promotion.model().index(index.row(), 0)
        # print(NewIndex)
        # print(index)
        print("Row %d and Column %d was clicked" % (row, column))
        item = self.Qtable_promotion.item(row, column)
        print(item.text())

    def FN_GET_promotion_type(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT PROMT_NAME_AR , PROMOTION_TYPE_ID FROM PROMOTION_TYPE order by PROMOTION_TYPE_ID*1 ")
        records = mycursor.fetchall()
        print(records)
        for row, VAL in records:
            self.Qcombo_promotion.addItem(row, VAL)
        mycursor.close()

    # department
    def FN_GET_department(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        try:
            mycursor.execute("SELECT DEPARTMENT_DESC ,DEPARTMENT_ID FROM DEPARTMENT")
            records = mycursor.fetchall()
        # finally:
        #     return records
        except:
            return ''

        print(records)

        for row, val in records:
            self.Qcombo_department.addItem(row, val)
        mycursor.close()

    # section
    def FN_GET_section(self, id):
        self.Qcombo_section.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_DESC ,SECTION_ID FROM SECTION where DEPARTMENT_ID = '" + id + "'")
        records = mycursor.fetchall()
        print(records)
        for row, val in records:
            self.Qcombo_section.addItem(row, val)
        mycursor.close()

    # section update
    def updatestatecombo(self):
        indx = self.Qcombo_department.currentData()
        self.FN_GET_section(indx)
        indx = self.Qcombo_section.currentData()
        self.Qcombo_classification.clear()
        self.FN_GET_classification(indx)
        self.Qcombo_section.activated[str].connect(self.updateBMCcombo)

    # BMC
    def FN_GET_classification(self, id):
        self.Qcombo_classification.clear()
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        try:
            mycursor.execute("SELECT BMC_LEVEL4_DESC , BMC_LEVEL4 FROM BMC_LEVEL4 where SECTION_ID =" + id + "")
            records = mycursor.fetchall()


        except:
            return   ''

        print(records)
        for row, val in records:
            self.Qcombo_classification.addItem(row, val)
        mycursor.close()

    # BMC update
    def updateBMCcombo(self):
        indx = self.Qcombo_section.currentData()
        self.FN_GET_classification(indx)



    # #######  prevent Escape CHAR
    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(CL_create_promotion, self).keyPressEvent(event)
    # #######  # #######  # #######  # #######

