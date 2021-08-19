import sys
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from qtpy import QtCore
from Validation.Validation import CL_validation
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox


class CL_ItemGroup(QtWidgets.QDialog):
    def __init__(self):
        super(CL_ItemGroup, self).__init__()
        cwd = Path.cwd()
        mod_path = Path(__file__).parent.parent.parent
        self.dirname = mod_path.__str__() + '/presentation/configuration_ui'
        self.conn = db1.connect()

    def FN_LOAD_CREATE(self):
        filename = self.dirname + '/Pos_Group_Item.ui'
        loadUi(filename, self)
        self.setWindowTitle('Item Group')
        self.CMB_Status.addItems(["Inactive","Active"])
        css_path = Path(__file__).parent.parent.parent
        path = css_path.__str__() + '/presentation/Themes/Style.css'
        self.setStyleSheet(open(path).read())
        self.pushButton.clicked.connect(self.FN_Create)


    def FN_Create(self):
        self.conn = db1.connect()
        self.conn.autocommit = False
        mycursor = self.conn.cursor()
        self.conn.start_transaction()
        indx = self.group_name.text().strip()
        sql_select_Query = "select * from POS_QUICK_GROUP where GROUP_NAME = %s "
        x = (indx,)
        mycursor.execute(sql_select_Query, x)
        record = mycursor.fetchone()
        if mycursor.rowcount > 0:
            QtWidgets.QMessageBox.warning(self, "خطا", "الاسم موجود بالفعل")
        else:
            if len(self.group_name.text()) == 0:
                QtWidgets.QMessageBox.warning(self, "خطا", "اكمل العناصر الفارغه")
            else:
                try:
                    sql0 = "  LOCK TABLES Hyper1_Retail.POS_QUICK_GROUP WRITE  "
                    mycursor.execute(sql0)
                    sql = "INSERT INTO POS_QUICK_GROUP (GROUP_NAME,NOTES,STATUS)" \
                          " VALUES (%s, %s, %s) "
                    val = (
                        self.group_name.text().strip(), self.notes.toPlainText().strip(),
                        self.CMB_Status.currentIndex())
                    mycursor.execute(sql, val)
                    mycursor.execute("SELECT * FROM POS_QUICK_GROUP Where GROUP_NAME = '" + indx + "'")
                    c = mycursor.fetchone()
                    id = c[0]
                    sql00 = "  UNLOCK   tables    "
                    mycursor.execute(sql00)
                    db1.connectionCommit(self.conn)
                    mycursor.close()
                    QtWidgets.QMessageBox.warning(self, "Done", "تم الانشاء")
                    self.label_num.setText(str(id))

                except:
                    print(sys.exc_info())
                    self.conn.rollback()
                finally:
                    if self.conn.is_connected():
                        mycursor.close()
                        self.conn.close()
                        print("connection is closed")
