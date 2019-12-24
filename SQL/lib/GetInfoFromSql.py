import numpy as np
import pandas as pd
import csv
from datetime import datetime
import sys
sys.path.append('../')
from HouTaiStatics import *

import numpy as np
import pandas as pd
import csv
from  config import config

def readxlsx2Npy():
    excel_filepath = '../../resTime.xlsx'
    resList = getGraph(excel_filepath, 106)
    resListNpy = np.array(resList)
    np.save('../../resTimeNpyOk',resListNpy)

def readNpy():
    pass

def timetransfer(li):
    timeLi = []
    for l in li:
        l = l.strip()
        if l.endswith(")"):
            l = int(l[:-1])
        elif l.endswith("]"):
            l = int(l[:-2])
        else:
            l = int(l)
        timeLi.append(l)
    dt = datetime(*timeLi)
    return dt

def getTime(InputStr):
    
    # print(InputStr)
    time1 = InputStr[0]
    time2 = InputStr[1]
    
    deltaTime  = int((time1-time2).seconds)
    # print(deltaTime)
    return deltaTime

def getTimeList(resList):
    resTime = []
    for idx, res in enumerate(resList):
        resTime.append([])
        print(idx)
        for r in res:
            time = getTime(r[4])
            r = np.insert(r,5,time)
            resTime[-1].append(r)
    return resTime

def staticDocTime(resListNpy):
    '''
    统计单个任务的全部时间
    '''
    timeDoc = []
    for idx,Time in enumerate(resListNpy): # 医生循环
        timeDoc.append([])
            # 一个医生标注好多任务，统计每一个任务所花费的全部时间
        if Time!=[]:
            Time = np.array(Time)
            taskid = Time[:,3]
            taskList = list(set(taskid))
            print(f'-------->{idx}')
            
            MarkerInfo = []
            for task in taskList:
                taskInfo = []
                for t in Time:
                    if t[3]==task:
                        taskInfo.append(t)
                taskInfo = np.array(taskInfo)
                # print(taskInfo.shape)
                time = taskInfo[:,5].mean()
                print(f"info---------->:{Time[0,2],task,time}")
    return timeDoc

def getMarkesDateset(makers):
    markerSet = []
    for marker in makers:
        markerSet.append(list(sql.get_from_sql(table = 't_task_evaluation',key = 'marker',key_value=marker)))
    return markerSet


def getDoctorCaseTime(serieasId):
    """
    @input:
        markerCaseid: shape = nx3,
        [caseid,marker['id'],marker['marker'],marker['taskId']]
    @return:
        serieasId :shape = nx4
        [caseid,marker['id'],marker['marker'],marker['taskId'],[timeEnd,timeBegin]]
    """
    for idx, serieas in enumerate(serieasId):
        markerCase = sql.get_from_sql(table = 't_user_operation',key = 'otherId',key_value=str(serieas[1]))
        for idx1, marker in enumerate(markerCase):
            if marker['type']==1:
                time = [marker['creationTime'],markerCase[idx1-1]['creationTime']]
                serieasId[idx].append(time)
                break
    return serieasId

def getDoctorsCaseStatics(markerSet):
    """
    @param1:
        markerSet = [doc1,doc2...docn]
        doc1 = [] m*p,p为数据库中的数据
    @return：
        resTime = [doc1,doc2...docn]
        doc1 = [] shape = m*5
    @description:
        1. 按照医生编号，获取当前医生caseID集合
        2. serieasId 获取serieasId = [] m*3 列表，
            [caseid,marker['id'],marker['marker'],marker['taskId']
        3. 在 t_user_operation中使用自增ID索引时间，并添加序列对
            [[caseid,marker['id'],marker['marker'],marker['taskId'],[timeEnd,timeBegin]]
    """
    resTime = []
    for idx, markers in enumerate(markerSet):
        caseIds = []#存储一个marker每一个case的id
        if idx==1:
            print(list(markers[0].keys()))
            print(markers[0]['marker'])
        for marker in markers:
            caseIds.append(marker['caseId'])
        caseIds = list(set(caseIds))

        serieasId = []
        for marker in markers:
            for caseid in caseIds:
                if marker['caseId'] ==caseid:
                    serieasId.append([caseid,marker['id'],marker['marker'],marker['taskId']])
                    break
        print(idx,len(serieasId))
        getDoctorCaseTime(serieasId)
        resTime.append(serieasId)
    return resTime

def getGraph(resTime):
    '''
    @param:resTime shape = docNum*ni*6
        where 6 is [[caseid,marker['id'],marker['marker'],marker['taskId'][timeEnd,timeBegin]]
    @decription:去除nan
    '''
    resList  = []
    for idx, singleRes in enumerate(resTime):
        
        # if idx==1:
        listOfl = singleRes

        listOfl = [li for li in listOfl if len(li)==5 and isinstance(li[4],list)]
        resList.append(listOfl)    
    return resList
def getSql(ppath = '../../Data121',stage1=False,stage2 = False,stage3 = False,stage4 = False,stage5=False,stage6 = True,stage7=False):
    '''
    :1. stage1 :
        1. 从t_task_evaluation 表获取任务列表
        2. 将标注人员列表写入 ../../makersNpy.npy文件
    :2. stage2：
        1. 读取../../makersNpy.npy文件，得到标注人员名单
        2. 分别从数据库中获取得到每一个标注人员所标注的信息
        3. table = 't_task_evaluation',key = 'marker',key_value=marker)
        4. 将每一个医生标注原始数据保存在'../../markerSet.npy'文件中
    :3. stage3：
        1. 加载'../../markerSet.npy'文件
        2. 获取时间序列
    :4. stage4:
        1. 加载'../../resTimeNpyOk.npy'文件
        2. 将时间序列按照医生列表顺序，依次写入excel文件中
    :5. stage5:
        1. 加载'../../resTimeNpyOk.npy'文件
        2. 去除没有时间的序列
        3. 写入'../../resTimeWithoutNan.npy'文件中
        3. 写入'../../resTimeWithoutNan.xlsx'文件中
    :6. stage6：
        1. 加载'../../resTimeWithoutNan.npy'文件为resTime2数组
        2. 处理[[caseid,marker['id'],marker['marker'],marker['taskId'],[timeEnd,timeBegin]]
            [[caseid,marker['id'],marker['marker'],marker['taskId'],[timeEnd,timeBegin]，timeEnd-timeBegin]
        3. 写入'../../accurateTime.npy'文件
        4. 写入'../../accurateTime.xlsx'文件
    '''
    if not os.path.exists(ppath):
        os.makedirs(ppath)
    if stage1:
        print(f'stage1---------')
        ergou  = sql.get_list_from_sql(table = "t_task_evaluation")
        ergou = list(ergou)
        makers = []
        for e in ergou:
            doctor = e['marker']
            makers.append(doctor)
        makers = list(set(makers))

        makersNpy = np.array(makers)
        makersNpySaveName = os.path.join(ppath,'makersNpy')
        
        np.save(makersNpySaveName,makersNpy)
    if stage2:
        print(f'stage2---------')
        loadPath = os.path.join(ppath,'makersNpy.npy')
        makers = np.load(loadPath,allow_pickle=True)
        markerSet = getMarkesDateset(makers)
        savePath = os.path.join(ppath,'markerSet')
        np.save(savePath,markerSet)
    if stage3:
        '''
        resTimeNpyOk.npy中保存 医生的每一个标注任务分开管理的数据
        '''
        print(f'stage3---------')
        loadPath = os.path.join(ppath,'markerSet.npy')
        markerSet = np.load(loadPath,allow_pickle=True)
        resTime = getDoctorsCaseStatics(markerSet)
        savePath = os.path.join(ppath,'resTimeNpyOk')
        np.save(savePath,resTime)
    if stage4:
        print(f'stage4---------')
        loadPath = os.path.join(ppath,'resTimeNpyOk.npy')
        resTime = np.load(loadPath,allow_pickle=True)
        excel_filepath = os.path.join(ppath,'resTime.xlsx')
        # excel_filepath ='../../resTime.xlsx'
        write = pd.ExcelWriter(excel_filepath)
        for idx,res in enumerate(resTime):
            print('----------->',idx)
            df1 = pd.DataFrame(res)
            print(len(res))
            df1.to_excel(write,f"Sheet{idx+1}")
        write.save()
    if stage5:
        print(f'stage5---------')
        loadPath = os.path.join(ppath,'resTimeNpyOk.npy')
        resTime = np.load(loadPath,allow_pickle=True)
        resTime2 = getGraph(resTime)
        savePath = os.path.join(ppath,'resTimeWithoutNan')
        np.save(savePath,resTime2)
        
        excel_filepath = os.path.join(ppath,'resTimeWithoutNan.xlsx')
        write = pd.ExcelWriter(excel_filepath)
        for idx,res in enumerate(resTime2):
            print('----------->',idx)
            df1 = pd.DataFrame(res)
            print(len(res))
            df1.to_excel(write,f"Sheet{idx+1}")
        write.save()

    if stage6:
        print(f'stage6---------')
        loadPath = os.path.join(ppath,'resTimeWithoutNan.npy')
        resTime2 = np.load(loadPath,allow_pickle=True)
        resList2 = getTimeList(resTime2)
        savePath = os.path.join(ppath,'accurateTime.npy')
        np.save(savePath,resList2)
        excel_filepath = os.path.join(ppath,'accurateTime.xlsx')
        
        write = pd.ExcelWriter(excel_filepath)
        for idx,res in enumerate(resList2):
            print('----------->',idx)
            df1 = pd.DataFrame(res)
            print(len(res))
            df1.to_excel(write,f"Sheet{idx+1}")
        write.save()

    
    if stage7:
        resTime = np.load('../../accurateTime.npy',allow_pickle=True)
        timeDoc = staticDocTime(resTime)
        np.save('../../TimeOfEveryDoc',np.array(timeDoc))


def getDoctorsListName():
    database = database121
    sql = SqlOperator(logger=None, conf = database)
    caseInfo = list(sql. get_list_from_sql('user'))
    dictIdName = {}
    for idx, Doc in enumerate(caseInfo):
        dictIdName[Doc['id']] = Doc['username']
    return dictIdName

class DaySqlDataget():
    '''按天获取信息
    1. 对服务器中的user_operation 获取一天的标注过的数据 3,1 
    2. 使用otherid 索引evaluation 中的id，并索引case id， 缩减数据
    '''
    def __init__(self,sql, pPath ='../../Date61',year=2019, month=12,day=9):
        self.pPath = pPath
        self.year = year
        self.month = month
        self.day = day
        self.sql = sql
        self.getDictTaskName()
        self.dictIdName=getDoctorsListName()
        self.getDatetime()
    def getDictTaskName(self):
        listColumn = ['id','name']
        getIdLNameDict = list(self.sql.get_list_sql_by_column(table = 't_eva_task',listColumn=listColumn))
        self.DictName = {}
        for getIdLName in getIdLNameDict:
            self.DictName[getIdLName['id']] = getIdLName['name']

    def getDatetime(self):
        self.date = str(datetime(self.year,self.month,self.day)).split(' ')[0]
        print('-'*20+'>')
        print("data is:",self.date)
    def getUerOperation(self):
        """
        : 1. 从t_user_operation ，对关键字creationTime 进行模糊搜索，提取出1天的数据
        : 2. 按照序列id，对样本标注的结束时间和开始时间进行统计，并添加到原始的存储字典中
        : 3. 保存该字典oneDayAllInfo.npy
        """
        # [[caseid,marker['id'],marker['marker'],marker['taskId'],[timeEnd,timeBegin]]
        #{'id': 210086, 'userId': 59, 'otherId': 515287, 'type': 5, 'comment': '', 'creationTime': datetime.datetime(2019, 12, 15, 18, 48, 27)}
        self.dayDate = list(self.sql.get_list_from_sql_by_regular(table = 't_user_operation',key = 'creationTime',key_value=self.date))
   
        self.serieses = {}
        for dayInfo in self.dayDate:
            if dayInfo['otherId'] not in self.serieses:
                self.serieses[dayInfo['otherId']] = []
            
            self.serieses[dayInfo['otherId']].append(dayInfo)

        
        for series, listValue in self.serieses.items():
            listValue.sort(key=lambda x: x['creationTime'])
            # self.serieses[series] = listValue

            for idx, value in enumerate(listValue):
                if value['type']==1:
                    resTime = [value['creationTime'],listValue[idx-1]['creationTime']]
                    value['end_begin'] = resTime
                    self.serieses[series] = value
                    break
                self.serieses[series] = [] 
        
        self.listResTime = [listValue for series, listValue in self.serieses.items() if listValue !=[]] 

        if not os.path.exists(self.pPath):
            os.makedirs(self.pPath)
        savePath = os.path.join(self.pPath,'oneDayAllInfo')
        np.save(savePath,self.listResTime)


    def getEvaluation(self):
        """
        使用self.listResTime中的otherId所以evaluation 中的 自增id，获取，caseId,taskId,然后按照医生分别进行存去
        
        1. 读取oneDayAllInfo.npy
        2. 对t_task_evaluation数据库中的 id号使用ResTime['otherId']索引
        3. 添加关键字[[caseid,marker['id'],marker['marker'],marker['taskId'],'isReview']到self.listResTime
        4. 保存当天的标注人员列表到makersNpy.npy文件中
        """
        loadPath = os.path.join(self.pPath,'oneDayAllInfo.npy')
        self.listResTime = np.load(loadPath, allow_pickle=True)
        for idx, ResTime in enumerate(self.listResTime):
            caseInfo = list(self.sql.get_from_sql(table = 't_task_evaluation',key = 'id',key_value=ResTime['otherId']))[0]
            
            self.listResTime[idx]['caseId'] = caseInfo['caseId']
            self.listResTime[idx]['marker'] = caseInfo['marker']
            self.listResTime[idx]['taskId'] = caseInfo['taskId']
            self.listResTime[idx]['isReview'] = caseInfo['isReview']
        
        self.ListOneDayDoctor = []

        for idx, ResTime in enumerate(self.listResTime):
            self.ListOneDayDoctor.append(ResTime['marker'])
        self.ListOneDayDoctor = list(set(self.ListOneDayDoctor))
        self.ListOneDayDoctor.sort()
        savePath = os.path.join(self.pPath,'makersNpy.npy')
        np.save(savePath,self.ListOneDayDoctor)

    def getAccurateTimeFile(self):
        """
        1. 加载当天的标注医生列表
        2. 对医生单独进行统计，医生id为key，[ResTime['caseId'],列表
        【ResTime['otherId'],ResTime['marker'],TaskIdlist,ResTime['end_begin'],sec,ResTime['isReview']] 】
        为存储的内容，保存每一个case
        3. 保存到accurateTime.xlsx文件中。
        """
        savePath = os.path.join(self.pPath,'makersNpy.npy')
        ListOneDayDoctor = np.load(savePath)
        print(ListOneDayDoctor)
        self.dictOneDayDoctorInfo = {}
        for OneDayDoctor in ListOneDayDoctor:
            print(f"OneDayDoctor:------>{OneDayDoctor}")
            if OneDayDoctor not in self.dictOneDayDoctorInfo:
                self.dictOneDayDoctorInfo[OneDayDoctor] = []
            for ResTime in self.listResTime:
                if ResTime['marker'] == OneDayDoctor:
                    sec = (ResTime['end_begin'][0]-ResTime['end_begin'][1]).seconds
                    TaskIdlist = self.DictName[ResTime['taskId']]
                    appender =[ResTime['caseId'],ResTime['otherId'],ResTime['marker'],TaskIdlist,ResTime['end_begin'],sec,ResTime['isReview']] 
                    self.dictOneDayDoctorInfo[OneDayDoctor].append(appender)
        excel_filepath = os.path.join(self.pPath,'accurateTime.xlsx')

        self.writeDictToExcelInDiffSheet(excel_filepath, self.dictOneDayDoctorInfo)
        accurateTimeNpy = []
        for key, OneDayDoctorInfo in self.dictOneDayDoctorInfo.items():
            accurateTimeNpy.append(OneDayDoctorInfo)
        savPath = os.path.join(self.pPath,'accurateTime.npy')
        np.save(savPath,accurateTimeNpy)

    def writeDictToExcelInDiffSheet(self,excel_filepath,inputDict):
        
        write = pd.ExcelWriter(excel_filepath)
        li = list(inputDict.keys())
        li.sort()
        print(f"wo shi li:{li}")
        excel_header = ['caseid','serieasId','markerId','taskId','timeEnd_Begin','time','isReview']
        if li==[]:
            
            inputD = [['']*len(excel_header)]
            df1 = pd.DataFrame(inputD)
            df1.to_excel(write,f"Sheet{1}",header=excel_header)
        for idx, day in enumerate(li):
            print('----------->',idx)
            # excel_header = ['caseid','serieasId','markerId','taskId','timeEnd_Begin','time']
            df1 = pd.DataFrame(inputDict[day])
            df1.to_excel(write,f"Sheet{idx+1}",header=excel_header)
        write.save()
       

def getDayTest(pPath):
    savePath = os.path.join(pPath,'makersNpy.npy')
    ListOneDayDoctor = np.load(savePath)
    print(ListOneDayDoctor)
if __name__ == '__main__':
    server = 61
    if server==121:
        database = database121
    elif server==61:
        database = database61
    
    sql = SqlOperator(logger=None, conf = database)
    print(f"从{server}服务器上获取数据")
    # getSql(ppath=f'../../Data{server}' ,stage1=False,stage2 = False,stage3 = True,stage4 = True,stage5=True,stage6 = True,stage7=False)
    year=2019   
    month =11
    day=2
    DaySqlDatageter = DaySqlDataget(sql,pPath=config.pPath,year=year,month =month,day=day)
    DaySqlDatageter.getUerOperation()
    DaySqlDatageter.getEvaluation()
    DaySqlDatageter.getAccurateTimeFile()

    