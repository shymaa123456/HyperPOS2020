#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 00:35:15 2020

@author: mohamed
"""
from data_connection.h1pos import db1

class CL_userModule(object):
    user_name=''
    myList=[]
    def init(self):
        self.conn = db1.connect()

    def loadPrivilages(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        sql_select_query = "select f.FORM_ID  ,a.ACTION_DESC ,fi.ITEM_DESC " \
                           "from SYS_PRIVILEGE p inner join SYS_FORM_ITEM fi on p.FORM_ID = fi.FORM_ID  " \
                           "inner join SYS_FORM f on  p.FORM_ID= f.FORM_ID " \
                           "inner join SYS_PRINT_EXPORT_LOOKUP a on p.ACTION_ID = a.ACTION_ID " \
                           "inner join SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  and p.FORM_ID=pi.FORM_ID and pi.ITEM_ID = fi.ITEM_ID  " \
                           "inner join SYS_USER_ROLE  ur on p.ROLE_ID = ur.ROLE_ID " \
                           "inner join SYS_USER u ON u.USER_ID = ur.USER_ID" \
                           " where  u.USER_NAME = %s and u.USER_STATUS= 0 and ur.UR_STATUS = 0 "
        x = (CL_userModule.user_name,)

        # print(sql_select_query)
        mycursor.execute( sql_select_query, x )

        records = mycursor.fetchall()
        #print(records)
        CL_userModule.myList = records
        print(CL_userModule.myList)
