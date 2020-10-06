from mysql.connector import Error

import mysql.connector

class db1():

    def __init__(self):
        pass

    @staticmethod
    def connect() :
       connection = mysql.connector.connect( host='localhost', database='Hyper1_Retail'
                                              , user='root', password='password', port='3306' )
       return connection

    @staticmethod
    def connectionClose(conn):
        conn.close()

    @staticmethod
    def connectionCommit(conn):
        conn.commit()