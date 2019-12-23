import os
import sys

import numpy as np 
import pandas as pd
sys.path.append('../')
from lib.DoctorCoarseMes import DocotorCoarseMes

from  config import config

def writeDictToExcelInDiffSheet(excel_filepath,inputDict):
    write = pd.ExcelWriter(excel_filepath)
    li = list(inputDict.keys())
    li.sort()
    if li==[]:
        excel_header = ['day','docId','End_begin', 'workTime/hour','biaozhuTime/hour', 'caseNum', 'meantime/min', 'maxtime/min']
        inputD = [['']*8]
        df1 = pd.DataFrame(inputD)
        df1.to_excel(write,f"Sheet{1}",header=excel_header)
    else :
        for idx, day in enumerate(li):
            print('----------->',idx)
            excel_header = ['day','docId','End_begin', 'workTime/hour','biaozhuTime/hour', 'caseNum', 'meantime/min', 'maxtime/min']
            df1 = pd.DataFrame(inputDict[day])
            df1.to_excel(write,f"Sheet{day}",header=excel_header)
    write.save()

def writeDictToExcelInOneSheet(excel_filepath,inputDict):
    write = pd.ExcelWriter(excel_filepath)
    li = list(inputDict.keys())
    li.sort()
    excel_header = ['day','docId','End_begin', 'workTime/min','biaozhuTime/min', 'caseNum', 'meantime/min', 'maxtime/min']
    listMesInSheet1=[]
    if li==[]:
        inputD = [['']*8]
        df1 = pd.DataFrame(inputD)
        df1.to_excel(write,f"Sheet{1}",header=excel_header)
    else:
        for idx, day in enumerate(li):
            listMesInSheet1+= inputDict[day]
        df1 = pd.DataFrame(listMesInSheet1)
        df1.to_excel(write,f"Sheet1",header=excel_header)
    write.save()

class DayStatic():
    def __init__(self,pPath = f'../../Data{config.server}'):
        self.pPath = pPath
        self.getAllDay()
        
        
    def getAllDay(self):
        '''获取天的列表
        '''
        DocotorCoarseMes.getList(pPath=self.pPath)
        self.DoctorList = DocotorCoarseMes.ListDoctor
        self.Daydict={}
        listDay = []
        for index, docId in enumerate(self.DoctorList) :
            ObjDoc = DocotorCoarseMes(docId)
            ObjDoc.message()
            self.Daydict[docId] = ObjDoc.dayTimeListOfDoc
            ObjDoc.message()
            listDay+= ObjDoc.dayTimeListOfDoc
        self.listDay = list(set(listDay))

    def getDayMessage(self):
        """获取到天的列表后
                对每一个医生for
                    每一个sheet进行for，
                        日期相同，则输出先关信息到一天一行
                        输出的信息为[docId,经标注时间，begin-end，标注时长，标注case数量，平均时间，最大标注时间]
        :param
        """
        self.listDayMess = [] #存储一天中的事情
        
        for dociD,daylist in self.Daydict.items():
            ExcelPath = os.path.join(self.pPath,f"Doctors/Doc{dociD}.xlsx")
            print(f"ExcelPath:{ExcelPath}")
            lenDocDay = len(daylist)

            for l in range(lenDocDay):
                sheetName = f'Sheet{l+1}'
                sheetFile = pd.read_excel(ExcelPath,sheet_name=sheetName)
                taskList  =list(set(sheetFile['taskId'][:-2]))
                strTask = ''
                for task in taskList:
                    strTask+= '/'+str(task)

                caseNum = len(sheetFile)-2
                rowsNum = len(sheetFile)
                info = list(sheetFile.loc[rowsNum-1])
                info = info[1:]
                
                
                ListTime = list(sheetFile['useTime/s'])[0:-1]
                # print(ListTime)
                ListTime = [float(time)/60 for time in ListTime]
                maxtime = max(ListTime)
                maxtime = f"{maxtime:02.2f}"
                
                docId = sheetFile.loc[0][3]
                docId = str(docId) + str(strTask)
                workTime = info[0].split(':')[1][0:5]
                End_begin = info[-1]
                meantime= info[4].split(':')[1][0:5]
                day = info[3].split(':')[1]
                biaozhuTime = info[1].split(':')[1][0:5]
                docOneDayInfo = [day,docId,End_begin, workTime,biaozhuTime, caseNum, meantime, maxtime]
                self.listDayMess.append(docOneDayInfo)
                print(docOneDayInfo)
        savepath = os.path.join(self.pPath,"allInday.npy")

        np.save(savepath,self.listDayMess)

    def getDaystatics(self):
        loadPath = os.path.join(self.pPath,'allInday.npy')

        listInfo = np.load(loadPath)
        dictDayInfo = {}
        for idx, Day in enumerate(self.listDay) :
            dictDayInfo[str(Day)] = []
        
        for Info in listInfo:
            dictDayInfo[Info[0]].append(Info)

        excel_filepath = os.path.join(self.pPath,'allInOneSheetStatics.xlsx')
        writeDictToExcelInOneSheet(excel_filepath,dictDayInfo)
        excel_filepath = os.path.join(self.pPath,'allInday.xlsx')
        writeDictToExcelInDiffSheet(excel_filepath,dictDayInfo)

if __name__=='__main__':
    pPath = config.pPath
    objDayStaticer = DayStatic(pPath=pPath)
    objDayStaticer.getDayMessage()
    objDayStaticer.getDaystatics()

     #46 +95 +156 +410+ 119 