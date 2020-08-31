from mysql.connector import Error

import mysql.connector

class db1():

    def __init__(self):
        pass

    @staticmethod
    def connect(self) :
        self.connection = mysql.connector.connect( host='localhost', database='PosDB'
                                              , user='root', password='password', port='3306' )
        self.mycursor = self.connection.cursor()
        return self.mycursor
