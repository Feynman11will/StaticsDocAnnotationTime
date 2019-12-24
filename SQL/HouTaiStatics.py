'''
@Author: your name
@Date: 2019-12-03 12:06:19
@LastEditTime: 2019-12-13 14:24:32
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /taskStatics/SQL/SqlTest.py
'''

import sys
import os
sys.path.append('../')
import numpy as np
from dw_sql_operator import SqlOperator
database61 = {"DataBase": {
        "localhost": "127.0.0.1",
        "host": "192.168.10.61",
        "port": 3306,
        "user": "root",
        "password": "deepwise",
        "database": "deepwise_eva"
            }}


database121 = {"DataBase": {
        "localhost": "127.0.0.1",
        "host": "192.168.10.121",
        "port": 3306,
        "user": "dw_eva",
        "password": "pSrvY@dVBUw.29nB",
        "database": "deepwise_eva"
            }}

if __name__ =="__main__":
    sql = SqlOperator(logger=None, conf = database121)
    # tasks = list(sql.get_from_sql(table = 't_eva_task',key = 'status',key_value='10'))
    # lengthTasks = len(tasks)
    # print("tasks's length","-"*20+">:"+f"tasks:{len(tasks)}")
    
    listColumn = ['id','name']
    
    getIdLNameDict = list(sql.get_list_sql_by_column(table = 't_eva_task',listColumn=listColumn))
    DictName = {}
    for getIdLName in getIdLNameDict:
        DictName[getIdLName['id']] = getIdLName['name']
        
    # print(f"DictName:{DictName['595']}")
    for key,value in DictName.items():
        print(f"{key}:{value}")
    print(DictName[595])