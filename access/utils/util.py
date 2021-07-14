from PyQt5 import QtWidgets
from datetime import datetime
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

class util():

    @staticmethod
    def FN_GET_CUSTGP():
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CG_DESC ,CG_GROUP_ID FROM Hyper1_Retail.CUSTOMER_GROUP where  CG_DESC !='H1' order by CG_GROUP_ID*1   asc")
        records = mycursor.fetchall()
        mycursor.close()
        return records

    @staticmethod
    def FN_GET_STATUS_id(desc):
        if desc == 'Active':
            return "1"
        else:
            return "0"


    @staticmethod
    def FN_GET_CUSTTP():
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_DESC ,LOYCT_TYPE_ID FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID != 'H1' order by LOYCT_TYPE_ID*1 asc" )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    @staticmethod
    def FN_GET_CITIES():
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CITY_NAME ,CITY_ID FROM Hyper1_Retail.City  where CITY_STATUS = 1 order by CITY_ID asc")
        records = mycursor.fetchall()
        mycursor.close()

        return records

    @staticmethod
    def FN_GET_CITY_DESC(id):
        conn = db1.connect()
        mycursor = conn.cursor()
        sql=    "SELECT CITY_NAME  FROM Hyper1_Retail.City  where CITY_ID = %s "
        val=(id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchone()
        mycursor.close()

        return myresult[0]

    @staticmethod
    def FN_VALIDATE_CUST(id ):

            conn = db1.connect()
            mycursor11 = conn.cursor()
            sql = "SELECT * FROM Hyper1_Retail.POS_CUSTOMER where POSC_CUST_ID = '" + str(id) + "'"
            #print(sql)
            mycursor11.execute(sql)
            myresult = mycursor11.fetchone()
            mycursor11.close()
            if mycursor11.rowcount > 0:
                return True
            else:
                return False
    @staticmethod
    def FN_GET_DISTRICT_DESC(id):
        conn = db1.connect()
        mycursor = conn.cursor()
        sql = "SELECT DISTRICT_NAME  FROM Hyper1_Retail.DISTRICT  where DISTRICT_ID = %s "
        val = (id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_DISTRICT(city):
            conn = db1.connect()
            mycursor = conn.cursor()
            sql = "SELECT DISTRICT_NAME ,DISTRICT_ID FROM Hyper1_Retail.DISTRICT  where CITY_ID = %s and DISTRICT_STATUS = 1  order by DISTRICT_ID asc"
            #print(sql)
            val = (city,)
            mycursor.execute(sql,val)
            records = mycursor.fetchall()
            mycursor.close()
            return records

    @staticmethod
    def FN_GET_CUSTTP_DESC( id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]


    @staticmethod
    def FN_GET_CUSTTG_DESC(id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute(
            "SELECT CG_DESC FROM Hyper1_Retail.CUSTOMER_GROUP where CG_GROUP_ID =" + str(id) )
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]


    @staticmethod
    def FN_GET_STATUS_DESC(id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    @staticmethod
    def FN_INSERT_IN_LOG(tableName,fieldName,newValue,oldValue,pk1,pk2=None,pk3=None,pk4=None,pk5=None):
        try:
           conn = db1.connect()
           mycursor = conn.cursor()

           changeDate = str(datetime.today().strftime('%Y-%m-%d'))
           sql = "insert into Hyper1_Retail.SYS_CHANGE_LOG (TABLE_NAME,FIELD_NAME,FIELD_OLD_VALUE,FIELD_NEW_VALUE,CHANGED_ON,CHANGED_BY,ROW_KEY_ID,ROW_KEY_ID2,ROW_KEY_ID3,ROW_KEY_ID4,ROW_KEY_ID5) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
           val= (tableName,fieldName,oldValue,newValue,changeDate,CL_userModule.user_name,pk1,pk2,pk3,pk4,pk5)
           mycursor.execute(sql, val)
           mycursor.close()
           db1.connectionCommit(conn)
        except Exception as err:
          print(err)

    @staticmethod
    def FN_GET_COMP_DESC( id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT COMPANY_DESC FROM Hyper1_Retail.COMPANY where COMPANY_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_BRANCH_DESC( id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT `BRANCH_DESC_A` FROM Hyper1_Retail.BRANCH where BRANCH_NO = '" + id + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_DEPT_DESC(id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT DEPARTMENT_DESC FROM Hyper1_Retail.DEPARTMENT where DEPARTMENT_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_SEC_DESC(id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT SECTION_DESC FROM Hyper1_Retail.SECTION where SECTION_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_COMP_ID(desc):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_DESC = '" + desc + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_BRANCH_ID(desc,comp):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT BRANCH_NO FROM Hyper1_Retail.BRANCH where BRANCH_DESC_A = '" + desc + "' and COMPANY_ID = '"+comp+ "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    @staticmethod
    def FN_GET_BRANCHES(company):
        conn = db1.connect()
        mycursor = conn.cursor()

        sql_select_query = "SELECT BRANCH_DESC_A ,`BRANCH_NO`  FROM Hyper1_Retail.BRANCH where BRANCH_STATUS   = 1 and COMPANY_ID = '"+company+"'"
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    @staticmethod
    def FN_GET_COMPANIES():
        conn = db1.connect()
        mycursor = conn.cursor()

        sql_select_query = "SELECT COMPANY_DESC ,COMPANY_ID FROM Hyper1_Retail.COMPANY where COMPANY_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    @staticmethod
    def FN_GET_DEPARTMENTS():
        conn = db1.connect()
        mycursor = conn.cursor()
        sql_select_query = "SELECT DEPARTMENT_DESC ,DEPARTMENT_ID FROM Hyper1_Retail.DEPARTMENT where DEPARTMENT_STATUS   = 1 "
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    @staticmethod
    def FN_GET_SECTIONS(dept):
        conn = db1.connect()
        mycursor = conn.cursor()

        sql_select_query = "SELECT SECTION_DESC ,SECTION_ID  FROM Hyper1_Retail.SECTION where SECTION_STATUS   = 1 and `DEPARTMENT_ID`= '"+dept+"'"
        mycursor.execute( sql_select_query )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    def FN_GET_COMPLAIN_TYPE_DESC(id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CCT_DESC FROM Hyper1_Retail.CUSTOMER_COMPLAINT_TYPE where CCT_TYPE_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        mycursor.close()
        return myresult[0]

    def FN_GET_COMPAIN_STATUS_DESC(id):
        if id == "0":
            status='Created'
        elif id == "1":
            status='Finished'
        elif id == "2":
            status = 'Inprogress'
        return status