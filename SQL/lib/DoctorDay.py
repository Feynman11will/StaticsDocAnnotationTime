import sys
import os
import numpy as np 
sys.path.append('../')
from lib.DoctorCoarseMes import DocotorCoarseMes
import datetime

from lib.Doctor import Doctor
from  config import config
import pandas as pd 

class DocotorDay(DocotorCoarseMes):
    def __init__(self,doctorId,pPath='../../Data121'):
        self.pPath = pPath
        super(DocotorDay,self).__init__(doctorId)
        self.message()

    def dayMesage(self):
        """
        @decription:
            1. 每天标注的case Num
            2. 一天标注的列表统计
            3. 起止时间到终止时间
            4. 绘制时间轴
            5. 可视化功能实现 
        """
        self.__listDayCase()
        self.__begin2EndTime()
    
    def __listDayCase(self):
        listDay = []
        for day in self.dayTimeListOfDoc:
            listDay.append([])
            listIdx = [i for i,value in enumerate(self.dayTimeOfDoc) if value==day]
            listDay[-1].append(self.npyData[listIdx,:])
        self.listDayCase = listDay

    def __begin2EndTime(self):
        """
        @decription:
            1. 对每一天进行统计
        @return：
            self.listDayBegin2Endtime shape = dayNum x 3
         """
        self.listDayBegin2Endtime = []
        for dayIdx, day in enumerate(self.dayTimeListOfDoc): 
            self.listDayBegin2Endtime.append([day])
            listCase = self.listDayCase[dayIdx][0]
            listCase = list(listCase[:,4])

            listCase.sort(key=lambda x: x[0])
            beginTime = listCase[0][1]
            endTime = listCase[-1][0]
            d = {}
            d['begin']=beginTime
            d['end']=endTime
            self.listDayBegin2Endtime[-1]+=[beginTime,endTime]
            

    def getPlotbarMess(self):
        for dayIdx, day in enumerate(self.dayTimeListOfDoc): 
            
            listCase = self.listDayCase[dayIdx][0]
            listCase = list(listCase[:,4])
            listCase.sort(key=lambda x: x[0])
            height = []
            x = []
            for h in listCase:
                time = (h[0]-h[1])
                interTime = time/2
                centerTime = h[1]+interTime
                height.append(time)
                x.append(centerTime.time())
            
    def getExcel(self, ifWrite=False):
        allInOne = []
        for idx,res in enumerate(list(self.listDayCase)):
            res = (list(res)[0]) 
            allInOne.append(res)
        result = np.concatenate(allInOne,axis=0)
        if ifWrite:
            pPath = os.path.join(self.pPath,'Doctors')
            if not os.path.exists(pPath):
                os.makedirs(pPath)
            excel_filepath = os.path.join(pPath,f'Doc{self.id}.xlsx')
            print(excel_filepath)
            li =  list(self.listDayCase)
            
            write = pd.ExcelWriter(excel_filepath)
            
            for idx,res in enumerate(list(self.listDayCase)):
                print('----------->',idx)
                
                excel_header = ['caseid','sequenceId','doctorId','taskId','datetime','useTime/s']
                res = (list(res)[0])
                dataTime = res[0][4][0].date()
                nullList=  [['','','','','','',]]
                day, beginTime,endTime=self.listDayBegin2Endtime[idx]

                timeAll = ((endTime - beginTime).seconds)/60/60
                dayAll  = res[:,5].sum()/60/60
                
                ave = dayAll/len(res[:,5])*60
                
                oneDaytime = [[f'上班时长/Hours:{timeAll:02.4f}',f'净标注时间/Hours:{dayAll:02.4f}', f'第:{idx+1}天,共:{self.workDaysNum}天',f'日期:{dataTime}',f'平均标注时间:{ave}',f'end:{endTime} begin:{beginTime}']]
                res = np.concatenate([res,nullList],axis=0)
                res = np.concatenate([res,oneDaytime],axis=0)

                df1 = pd.DataFrame(res)
                
                df1.to_excel(write,f"Sheet{idx+1}",header=excel_header)
            write.save()
        return result
        
        
def getDoctorExcelFile():

    pPath = config.pPath
    print(f"pPath is:{pPath}")
    DocotorDay.getList(pPath=pPath)
    DoctorList = DocotorDay.ListDoctor
    
    for idx, docId in enumerate(DoctorList):
        Docobj= DocotorDay(docId,pPath=pPath)
        Docobj.dayMesage()
        Docobj.getExcel(ifWrite=True)

def allmessage():
    DoctorList = DocotorDay.ListDoctor
    DateAllInOne = []
    for idx, docId in enumerate(DoctorList):
        Docobj= DocotorDay(docId)
        Docobj.dayMesage()
        result = Docobj.getExcel()
        DateAllInOne.append(result)
    DateAllInOne = np.concatenate(DateAllInOne,axis=0)
    
    if not os.path.exists('../../AllInOne/'):
        os.makedirs('../../AllInOne/')
    excel_filepath =f'../../AllInOne/DocAllMes.xlsx'

    write = pd.ExcelWriter(excel_filepath)
    excel_header = ['caseid','sequenceId','doctorId','taskId','datetime','useTime/s']
    df1 = pd.DataFrame(DateAllInOne)
    
    df1.to_excel(write,f"Sheet{idx+1}",header=excel_header)
    write.save()





if __name__=='__main__':
    
    getDoctorExcelFile()
     #46 +95 +156