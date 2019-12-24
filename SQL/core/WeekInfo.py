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
from datetime import datetime,timedelta
from core.DayInfo import DayInfo


class WeeksInfo(DayInfo):
    def __init__(self,DayInfo, year, month, beginDay,lenDay):
        self.beginDay = beginDay
        self.year = year
        self.month = month
        self.lenDay = lenDay
        self.DayInfo = DayInfo

    def getWeeksInfo(self):
        BD = datetime(self.year,self.month,self.beginDay)
        self.getDayList = [str(BD + timedelta(days = i)).split(' ')[0] for i in range(self.lenDay)]

        for getDay in self.getDayList:
            self.year,self.month,self.day = map(int,getDay.split('-'))
            print(self.year,self.month,self.day)
            self.ObjDayInfo = self.DayInfo(parentPath = '../../', year=self.year,month=self.month,day=self.day)
            self.ObjDayInfo.allServerDayInfoStatics()
            self.ObjDayInfo.synthsisOneDayAllServer()
    def synthsisAllDayofAllServer(self):
        
        pass



if __name__=='__main__':
    WeekInfoer =  WeeksInfo(DayInfo,year=2019,month=12, beginDay=19,lenDay=1)
    WeekInfoer.getWeeksInfo()

    #46 +95 +156 +410+ 119 +108 +83 +63