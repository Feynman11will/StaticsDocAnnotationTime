import sys
import os
import numpy as np 
sys.path.append('../')
from lib.Doctor import Doctor
import datetime
class DocotorCoarseMes(Doctor):
    def __init__(self,doctorId):
        super(DocotorCoarseMes,self).__init__(doctorId)

    def message(self):
        """
        @decription:
            1. 统计该医生的标注天数
            2. 标注的case数量
            3. 标注的task数目
            4. 标注的总时间
            5. 标注每一个task所使用的时间
            6. 标注一个task中的一个case的平均时间
        """
        self.__daysStatics()
        self.__caseStatics()
        self.__task()
        
    def __daysStatics(self):
        """
        @decription:
        @self.data进行处理, 获取总共的天数
        """
        self.npyData = np.array(self.data)
        
        dayTimeOfDoc = self.npyData[:,4]
        self.dayTimeListOfDoc = []
        self.dayTimeOfDoc = [li[0].date() for li in dayTimeOfDoc]
        for day in self.dayTimeOfDoc:
            if day not in self.dayTimeListOfDoc:
                self.dayTimeListOfDoc.append(day)
        self.dayTimeListOfDoc = list(set(self.dayTimeListOfDoc))
        self.workDaysNum = len(self.dayTimeListOfDoc)
        
    def __caseStatics(self):
        self.caseNum = self.npyData.shape[0]
        
    def __task(self):
        listTask = self.npyData[:,3]
        self.listTask = list(set(listTask))
        self.TaskNum  = len(self.listTask)
        self.__timeAll()
        self.__taksTime()
        self.__taskCaseTime()
    def __timeAll(self):
        self.listCaseTime = self.npyData[:,5]
        self.timeAll = self.listCaseTime.sum()
        

    def __taksTime(self):
        taskInfo = []
        for task in self.listTask:
            taskInfo.append({"taskId":task})
            ListCaseIdx = np.where(self.npyData[:,3]==task)
            lci = len(ListCaseIdx)
            taskInfo[-1]["taskLength"] = lci
            taskInfo[-1]["timeList"] = self.npyData[ListCaseIdx,5]
            taskInfo[-1]["meanTime"] = self.npyData[ListCaseIdx,5].mean()
        self.taskInfo = taskInfo

    def __taskCaseTime(self):
        self.caseTime = self.npyData[:,5]

    def __str__(self):
        listVars = vars(self)
        resString = ""
        for key, value in vars(self).items():
            resString += f":{key}\n"
        return resString

    def writeExcel(self):
        if not os.path.exists('../../DoctorsCoarse/'):
            os.makedirs('../../DoctorsCoarse/')
        excel_filepath =f'../../DoctorsCoarse/Doc{self.id}.xlsx'
        write = pd.ExcelWriter(excel_filepath)
        for idx,res in enumerate(list(self.listDayCase)):
            print('----------->',idx)
            excel_header = ['caseid','sequenceId','doctorId','taskId','datetime','useTime/s']
            
            res = (list(res)[0])
            df1 = pd.DataFrame(res)
            print(len(res))
            df1.to_excel(write,f"Sheet{idx+1}",header=excel_header)

if __name__=='__main__':
    Docobj= DocotorCoarseMes(10)
    
    print(Docobj)
    Docobj.message()
     #46 +95