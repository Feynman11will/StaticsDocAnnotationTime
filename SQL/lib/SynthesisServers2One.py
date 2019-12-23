import os
import sys

import numpy as np 
import pandas as pd
sys.path.append('../')

from config import config
import xlrd
serverlist = config.serverlist

class synthesis():
    listServer = serverlist
    def __init__(self,
        isSingleDay=True,
        pPath = '../../Data61',
        outPutPPath = '../../DataAllServer',
        year=0,
        month=0,
        day=0):
        self.serversInfo = {}
        self.isSingleDay = isSingleDay
        self.pPath = pPath
        self.year = year
        self.month = month
        self.day = day
        self.outPutPPath = outPutPPath
        self.getServersBasicInfo()

        
    def getServersBasicInfo(self):
        """
        :param: synthesis.listServer
        :decription:
            获取每一个服务器的统计信息路径
            读取每个服务器统计信息
            读取每一个sheet到    
        """
        self.serversInfo = {}
        self.listDayOfAllServer = []
        for server in synthesis.listServer:
            if self.isSingleDay:
                listpPathToken = self.pPath.split('/')
                listpPathToken[-2] = f"Data{server}"
                self.pPath = '/'.join(listpPathToken)
            else:
                self.pPath = f'../../Data{server}'
            
            sheetNamePath =  os.path.join(self.pPath,'allInOneSheetStatics.xlsx')
            sheeter =  pd.read_excel(sheetNamePath,sheet_name='Sheet1')
            sheetnames = sheeter['day']
            sheetnames = list(set(sheetnames))
            
            excelPath = os.path.join(self.pPath,'allInday.xlsx')
            
            for sheetname in sheetnames:
                if not isinstance(sheetname,str):
                    break
                sheetname = "Sheet"+sheetname
                print(f"sheetname:{sheetname}")
                self.listDayOfAllServer.append(sheetname)
                sheetFile = pd.read_excel(excelPath,sheet_name=sheetname)
                sheetInfo = np.array(sheetFile)
                
                tmp = np.full([len(sheetInfo),1],server)
 
                eatingTime = (sheetInfo[:,8]/60 - sheetInfo[:,7]/60)
                noeatingTime =  (sheetInfo[:,5] - eatingTime)
                noeatingTime = np.squeeze(noeatingTime)[:,None]
                eatingTime = np.squeeze(eatingTime)[:,None]
                
                sheetInfo = np.concatenate((sheetInfo,tmp,eatingTime,noeatingTime),axis=1)
                if sheetname not in self.serversInfo:
                    self.serversInfo[sheetname] = []
                self.serversInfo[sheetname].append(sheetInfo)

        self.listDayOfAllServer = list(set(self.listDayOfAllServer))
        self.listDayOfAllServer.sort()
        self.listStaticAllServer = []
        if self.listDayOfAllServer==[]:
            print('今天没有标注结果')
            return 
        for day in self.listDayOfAllServer:
            dayInfo = np.concatenate(self.serversInfo[day],axis=0)
            self.listStaticAllServer.append(dayInfo)
        self.write2excel = np.concatenate(self.listStaticAllServer,axis=0)

        if self.isSingleDay:
            
            excel_filepath = os.path.join(self.outPutPPath,f'{self.year}_{self.month}_{self.day}/synthesisAllOfServer.xlsx')
            npy_filepath = os.path.join(self.outPutPPath,f'{self.year}_{self.month}_{self.day}/synthesisAllOfServer.npy')
        else:
            excel_filepath = os.path.join(self.outPutPPath,'synthesisAllOfServer.xlsx')
            npy_filepath = os.path.join(self.outPutPPath,'synthesisAllOfServer.npy')
        pexcel_filepath = os.path.dirname(excel_filepath)
        pnpy_filepath = os.path.dirname(npy_filepath)
        if not os.path.exists(pexcel_filepath):
            os.makedirs(pexcel_filepath)
        if not os.path.exists(pnpy_filepath):
            os.makedirs(pnpy_filepath)

        np.save(npy_filepath,self.write2excel)
        
        write = pd.ExcelWriter(excel_filepath)
        excel_header = ['day','docId/taskListName','End_begin', 'workTime/hours','biaozhuTime/hours', 'caseNum', 'meantime/min', 'maxtime/min','server','eatingTime/Hours','biaozhuWithoutEatTime/Hours']
        dfDict = {}
        for idx, h in enumerate(excel_header):
            dfDict[h] = self.write2excel[:,idx+1]
        df1 = pd.DataFrame(dfDict)
        excel_headerorder = ['day','docId/taskListName','End_begin', 'workTime/hours','eatingTime/Hours','biaozhuWithoutEatTime/Hours','biaozhuTime/hours', 'caseNum', 'meantime/min', 'maxtime/min','server']
        df1 = df1.loc[:,excel_headerorder]
        df1.to_excel(write,f"Sheet1",float_format='%.3f')
        
        write.save()
            
    def synthesis2One(self):
        """
        将信息合成到一个xlsx文件中
        """
        pass

if __name__=='__main__':
    synthesiser =  synthesis()
    