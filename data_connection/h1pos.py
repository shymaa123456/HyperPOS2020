from mysql.connector import Error

import mysql.connector

class db1():

    def __init__(self):
        pass

    @staticmethod
    def connect() :
       connection = mysql.connector.connect( host='10.2.1.190', database='Hyper1_Retail'
                                              , user='shelal',password='123P@ssword', port='3306' ,auth_plugin='mysql_native_password' )
       return connection

    @staticmethod
    def connectionClose(conn):
        conn.close()

    @staticmethod
    def connectionCommit(conn):
        conn.commit()