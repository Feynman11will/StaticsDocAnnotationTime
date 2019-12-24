'''
@Author: your name
@Date: 2019-12-03 12:06:19
@LastEditTime: 2019-12-13 14:22:56
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /taskStatics/SQL/SqlTest.py
'''

import sys 
import os 
sys.path.append('../')
import numpy as np 
from dw_sql_operator import SqlOperator 
database = {"DataBase": {
        "localhost": "127.0.0.1",
        "host": "192.168.10.61",
        "port": 3306,
        "user": "root",
        "password": "deepwise",
        "database": "deepwise_eva"
            }}



def getTasks(lNameSet,print2Screen = False):
    FeiQuanKe       = []
    FeiJieJie       = []
    Brain           = []
    ZongGe          = []
    NaoChuxie       = []
    XiongBuGuzhe    = []
    LeiGuGuZhe      = []
    LeiGuLunKuo     = []
    XueGuan         = []
    elseList        = []
    for task in lNameSet:
        if "肺全科" in str(task.values()):
            FeiQuanKe.append(task)
        elif "肺结节" in str(task.values()):
            FeiJieJie.append(task)
        elif "脑梗" in str(task.values()):
            Brain.append(task)
        
        elif "胸部骨折" in str(task.values()):
            XiongBuGuzhe.append(task)
        elif "肋骨骨折" in str(task.values()):
            LeiGuGuZhe.append(task)
        elif "脑出血" in str(task.values()):
            NaoChuxie.append(task)
        elif "肋骨轮廓" in str(task.values()):
            LeiGuLunKuo.append(task)
        elif "血管" in str(task.values()):
            XueGuan.append(task)
            
        elif "纵膈" in str(task.values()) or '纵隔' in str(task.values()):
            ZongGe.append(task)
        else :
            elseList.append(task)
            
    if print2Screen:
        allLengh =  f"""
           {len(FeiQuanKe   )+
            len(FeiJieJie   )+ 
            len(Brain       )+
            len(ZongGe      )+    
            len(NaoChuxie   )+
            len(XiongBuGuzhe)+     
            len(LeiGuGuZhe  )+
            len(LeiGuLunKuo )+    
            len(XueGuan     )}
        """
        print('allLengh'+">>"*20,allLengh)
        
        print('肺全科:'+"#"*30)
        print(">>"*20)
        print("FeiQuanKe 的长度","-"*20+">:"+f"{len(FeiQuanKe)}")
        for i,name in enumerate(FeiQuanKe):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")
        
        print('肺结节:'+"#"*30)
        print(">>"*20)
        print("FeiJieJie 的长度","-"*20+">:"+f"{len(FeiJieJie)}")
        for i,name in enumerate(FeiJieJie):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")


        print('脑梗:'+"#"*30)
        print(">>"*20)
        print("Brain 的长度","-"*20+">:"+f"{len(Brain)}")
        for i,name in enumerate(Brain):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")

        print('胸部骨折:'+"#"*30)
        print(">>"*20)
        print("XiongBuGuzhe 的长度","-"*20+">:"+f"{len(XiongBuGuzhe)}")
        for i,name in enumerate(XiongBuGuzhe):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")

        print('肋骨骨折:'+"#"*30)
        print(">>"*20)
        print("LeiGuGuZhe 的长度","-"*20+">:"+f"{len(LeiGuGuZhe)}")
        for i,name in enumerate(LeiGuGuZhe):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")

        print('肋骨轮廓:'+"#"*30)
        print(">>"*20)
        print("LeiGuLunKuo 的长度","-"*20+">:"+f"{len(LeiGuLunKuo)}")
        for i,name in enumerate(LeiGuLunKuo):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")
            
        print('脑出血:'+"#"*30)
        print(">>"*20)
        print("NaoChuxie 的长度","-"*20+">:"+f"{len(NaoChuxie)}")
        for i,name in enumerate(NaoChuxie):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")

        print('血管:'+"#"*30)
        print(">>"*20)
        print("XueGuan 的长度","-"*20+">:"+f"{len(XueGuan)}")
        for i,name in enumerate(XueGuan):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")
            
        print('纵膈:'+"#"*30)
        print(">>"*20)
        print("ZongGe 的长度","-"*20+">:"+f"{len(ZongGe)}")
        for i,name in enumerate(ZongGe):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")
        print()
        print()
        print()
        print('elseList:'+"#"*30)
        print(">>"*20)
        print("elseList 的长度","-"*20+">:"+f"{len(elseList)}")
        for i,name in enumerate(elseList):
            print("{:3d}".format(i),"-"*20+">:"+f"task:{name}")

    return [FeiQuanKe, FeiJieJie, Brain, ZongGe, NaoChuxie, XiongBuGuzhe, LeiGuGuZhe, LeiGuLunKuo, XueGuan]


def getSamples(taskList,saveNpy = False):
    for idx , tasks in enumerate(taskList):
        if idx==3:
            for task in  tasks :
                keys = list(task.keys())# id号码
                values = list(task.values())
                assert(len(keys)==1)
                getTaskIdSamples = list(sql.get_from_sql(table = 't_eva_case',key = 'taskId',key_value=keys[0]))
                for i ,sample in enumerate(getTaskIdSamples) :
                    if i<200:
                        if sample['status']==3:
                            if f"{values[0]}Pending" not in list(statics[idx].keys()):
                                statics[idx][f"{values[0]}Pending"] =0
                                statics[idx][f"{values[0]}PendingId"] = [sample['id']]
                            else : 
                                statics[idx][f"{values[0]}Pending"] +=1
                                statics[idx][f"{values[0]}PendingId"].append([sample['id']])
                                
                        elif sample['status']==7:
                            if f"{values[0]}sampleCase" not in list(statics[idx].keys()):
                                statics[idx][f"{values[0]}sampleCase"] =0
                                statics[idx][f"{values[0]}sampleCaseId"] = [sample['id']]
                            else : 
                                statics[idx][f"{values[0]}sampleCase"] +=1
                                statics[idx][f"{values[0]}sampleCaseId"].append([sample['id']])
                print('taskId:',keys[0],f"{values[0]}--->getTaskIdSamples:{len(getTaskIdSamples)}")
            print()
            print('saving statics-------->')

            staticstmp = np.array(statics[idx])
            if not  os.path.exists("./data"):
                os.mkdir("./data") 
            np.save(f"./data/statics_{idx}.npy", staticstmp)
            
def getDataFromNpy(npyPath):
    liNpy = os.listdir(npyPath)
    for npy in liNpy:
        fullNpy = os.path.join(npyPath,npy)
        data = np.load(fullNpy,allow_pickle=True)
        yield data
        
    def printFalse():
        print('数据迭代完成----->')
    return printFalse()
    
if __name__ =="__main__":
    sql = SqlOperator(logger=None, conf = database)
    tasks = list(sql.get_from_sql(table = 't_eva_task',key = 'status',key_value='10'))
    lengthTasks = len(tasks)
    print("tasks's length","-"*20+">:"+f"tasks:{len(tasks)}")
    
    nameList = []
    # for task in tasks:
    #     if "钼靶" not in task['name'] or '乳腺' not in task['name'] or "乳腺" not in task['name'] or '钼靶' not in task['name']:
    #         nameList.append({task['id']:task['name']})

    lNameSet= nameList
    print("lNameSet 的长度","-"*20+">:"+f"tasks:{len(lNameSet)}")
    
    taskList = \
        [FeiQuanKe, FeiJieJie, Brain, ZongGe, NaoChuxie, XiongBuGuzhe, LeiGuGuZhe, LeiGuLunKuo, XueGuan ]= \
            getTasks(lNameSet,print2Screen=False)
    statics = []
    ltaskList = len(taskList)
    for i in range(ltaskList):
        statics.append({})

    samples = True
    if samples==True:   
        getSamples(taskList,saveNpy = False)
    npyPath = '/Users/deepwise/Documents/02标注平台/taskStatics/SQL/data'
    datas = getDataFromNpy(npyPath)

    D =  []
    for idx,data in enumerate(datas):
        D.append(data)
    print('测试一下')
    
