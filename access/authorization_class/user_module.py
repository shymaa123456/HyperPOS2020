#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 00:35:15 2020

@author: mohamed
"""
from data_connection.h1pos import db1


class CL_userModule(object):
    user_name = ''
    myList = []
    branch = []
    section = []
    item = []

    def init(self):
        self.conn = db1.connect()

    #Todo: method for get all form role ,from and from item assigned to login user
    def loadPrivilages(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        sql_select_query = "select r.ROLE_ID , f.FORM_DESC ,f.FORM_ID ,a.ACTION_ID ,pi.ITEM_ID " \
                           "from Hyper1_Retail.SYS_PRIVILEGE p " \
                           "inner join Hyper1_Retail.SYS_FORM f on  p.FORM_ID= f.FORM_ID " \
                           "inner join Hyper1_Retail.SYS_PRINT_EXPORT a on p.ACTION_ID = a.ACTION_ID " \
                           "left outer join Hyper1_Retail.SYS_PRIVILEG_ITEM pi on p.PRIV_ID= pi.PRIV_ID  and p.FORM_ID=pi.FORM_ID  " \
                           "inner join Hyper1_Retail.SYS_USER_ROLE  ur on p.ROLE_ID = ur.ROLE_ID " \
                           "inner join Hyper1_Retail.SYS_ROLE r on r.ROLE_ID = p.ROLE_ID " \
                           "inner join Hyper1_Retail.SYS_USER u ON u.USER_ID = ur.USER_ID" \
                           " where  u.USER_ID = %s and u.USER_STATUS= 1 and ur.UR_STATUS = 1 and f.form_status = 1 and r.ROLE_STATUS = 1"
        x = (CL_userModule.user_name,)
        mycursor.execute(sql_select_query, x)
        records = mycursor.fetchall()
        print(records)
        CL_userModule.myList = records

    #Todo: method for get branch assigned to login user
    def FN_AuthBranchUser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("Select BRANCH_NO from SYS_USER_BRANCH where USER_ID = '"+CL_userModule.user_name+"' and STATUS = 1")
        records = mycursor.fetchall()
        CL_userModule.branch = records
        return records

    #Todo: method for get section assigned to login user
    def FN_AuthSectionUser(self):
        self.conn = db1.connect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT SECTION_ID FROM SYS_USER_SECTION where USER_ID='" + CL_userModule.user_name + "' and STATUS = 1")
        records = mycursor.fetchall()
        CL_userModule.section = records
        return records



