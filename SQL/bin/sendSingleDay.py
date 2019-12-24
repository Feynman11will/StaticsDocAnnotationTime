
import os
import sys

import numpy as np
import pandas as pd
sys.path.append('../')

from core.sendEmail import SendEmail
from core.WeekInfo import WeeksInfo
from core.DayInfo import DayInfo
from config import safeMessConf as safeConf
from datetime import datetime,timedelta

class SendingDay():
    def __init__(self,date):
        self.date = date
        print(self.date)
        self.year,self.month,self.day= map(int,self.date.split('-'))

    def staticsSingleDay(self):
        self.WeekInfoer =  WeeksInfo(DayInfo,year=self.year,month=self.month, beginDay=self.day,lenDay=1)
        self.WeekInfoer.getWeeksInfo()
    def sendSingleDay(self):
        self.staticsSingleDay()
        print('统计完成,开始发送邮件')
        self.sender = safeConf.AliSender
        self.myPass = safeConf.AliPass
        self.receivers = safeConf.receivers
        self.objSender = SendEmail(day = self.date,
                        sender=self.sender,
                        myPass=self.myPass,
                        receivers = self.receivers,
                        dstPPath='../../testZip')
        self.objSender.emailSend()

if __name__=='__main__':

    lastDay = datetime.now() + timedelta(days = -1)
    date = str(str(lastDay)).split(' ')[0]
    # date = str(str(datetime(2019,11,2))).split(' ')[0]
    Sender = SendingDay(date=date)
    Sender.sendSingleDay()
    print(f'昨天的统计结果已经发送完成')
    