

from PyQt5 import QtWidgets
from datetime import datetime
from access.authorization_class.user_module import CL_userModule
from data_connection.h1pos import db1

class util():

    @staticmethod
    def FN_GET_CUSTGP():
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CG_DESC FROM Hyper1_Retail.CUSTOMER_GROUP order by CG_GROUP_ID asc")
        records = mycursor.fetchall()
        mycursor.close()

        return records

    @staticmethod
    def FN_GET_STATUS_id(desc):
        if id == 'Active':
            return "1"
        else:
            return "0"


    def FN_GET_CUSTTP():

        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute( "SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE order by LOYCT_TYPE_ID asc" )
        records = mycursor.fetchall()
        mycursor.close()
        return records

    @staticmethod
    def FN_GET_CITIES():
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT CITY_NAME FROM Hyper1_Retail.City  where CITY_STATUS = 1 order by CITY_ID asc")
        records = mycursor.fetchall()
        mycursor.close()

        return records
    @staticmethod
    def FN_GET_DISTRICT(city):
            conn = db1.connect()
            mycursor = conn.cursor()
            mycursor.execute("SELECT DISTRICT_NAME FROM Hyper1_Retail.DISTRICT d inner join Hyper1_Retail.City c on d.CITY_ID = c.CITY_ID where CITY_NAME = '"+city+"' and DISTRICT_STATUS = 1  order by DISTRICT_ID asc")
            records = mycursor.fetchall()
            mycursor.close()
            return records

    @staticmethod
    def FN_GET_CUSTTP_DESC( id):
        conn = db1.connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT LOYCT_DESC FROM Hyper1_Retail.LOYALITY_CUSTOMER_TYPE where LOYCT_TYPE_ID = '" + id + "'")
        myresult = mycursor.fetchone()
        return myresult[0]

    @staticmethod
    def FN_GET_STATUS_DESC(id):
        if id == '1':
            return "Active"
        else:
            return "Inactive"

    @staticmethod
    def FN_INSERT_IN_LOG(tableName,fieldName,newValue,oldValue):
        try:
           conn = db1.connect()
           mycursor = conn.cursor()
           # get max id
           mycursor.execute("SELECT max(cast(ROW_ID  AS UNSIGNED)) FROM  Hyper1_Retail.SYS_CHANGE_LOG")
           myresult = mycursor.fetchone()

           if myresult[0] == None:
               id = "1"
           else:
              id = int(myresult[0]) + 1
           changeDate = str(datetime.today().strftime('%Y-%m-%d'))
           sql = "insert into Hyper1_Retail.SYS_CHANGE_LOG values(%s,%s,%s,%s,%s,%s,%s)"
           val= (id,tableName,fieldName,oldValue,newValue,changeDate,CL_userModule.user_name)
           mycursor.execute(sql, val)
           mycursor.close()
           db1.connectionCommit(conn)
        except Exception as err:
          print(err)