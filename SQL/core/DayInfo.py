import os
import sys

import numpy as np
import pandas as pd
import xlrd
sys.path.append('../')
from config import config
from HouTaiStatics import *
from lib.GetInfoFromSql import DaySqlDataget
from lib.DoctorDay import DocotorDay
from lib.StaticsDayAllDoc import DayStatic

from lib.SynthesisServers2One import synthesis

class DayInfo():
    """
    处理多个服务器的数据,一次处理一天的数据，
    1. pullFormSql 从服务器上获取一天的数据，生成一天内标注医生的名单以及以医生为单位统计一天内的工作情况
        accurateTime.xlsx
        makersNpy.npy
    2. 对每个医生每一天的标注情况进行统计，一天一个列表，一个列表中sheet代表每一天
    3. 对一天的工作情况进行统计
    4. 综合多个服务器的结果
    """
    def __init__(self,parentPath,sql=None,year=0,month=0,day=0):
        self.sql = sql
        self.year = year
        self.month = month
        self.parentPath = parentPath
        self.day = day
    def pullFromOneSql(self):
        print(f"从{self.server}服务器上获取数据")
        self.DaySqlDatageter = DaySqlDataget(self.sql,pPath=self.pPath,year=self.year,month =self.month,day=self.day)
        self.DaySqlDatageter.getUerOperation()
        self.DaySqlDatageter.getEvaluation()
        self.DaySqlDatageter.getAccurateTimeFile()
    def DayStatic(self):
        # pPath = self.pPath
        print(f"pPath is:{self.pPath}")
        DocotorDay.getList(pPath=self.pPath)
        self.DoctorList = DocotorDay.ListDoctor
        
        for idx, docId in enumerate(self.DoctorList):
            self.Docobj= DocotorDay(docId,pPath=self.pPath)
            self.Docobj.dayMesage()
            
            self.Docobj.getExcel(ifWrite=True)
    def oneServerDayStatic(self):
        self.objDayStaticer = DayStatic(pPath=self.pPath)
        self.objDayStaticer.getDayMessage()
        self.objDayStaticer.getDaystatics()

    def allServerDayInfoStatics(self):
        for server in config.serverlist:
            self.server = server
            if server==121:
                database = database121
            elif server==61:
                database = database61
            self.pPath = os.path.join(self.parentPath,f'Data{server}/{self.year}_{self.month}_{self.day}')
            
            
            self.sql = SqlOperator(logger=None, conf = database)
            self.pullFromOneSql()
            self.DayStatic()
            self.oneServerDayStatic()
    def synthsisOneDayAllServer(self):
        
        self.pPath = os.path.join(self.parentPath,f'Data/{self.year}_{self.month}_{self.day}')
        
        synthesiser = synthesis(isSingleDay=True,
            pPath = self.pPath,
            outPutPPath = '../../DataAllServer',
            year = self.year,
            month = self.month,
            day = self.day)

if __name__ =="__main__":
    
    year = config.year
    month = config.month
    day = config.day

    ObjDayInfo = DayInfo(parentPath = '../../',year=year,month=month,day=day )
    ObjDayInfo.allServerDayInfoStatics()
    ObjDayInfo.synthsisOneDayAllServer()
