

from PyQt5 import QtWidgets
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
