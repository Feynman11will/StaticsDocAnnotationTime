import sys
import os
import numpy as np 
sys.path.append('../')
from config import config 
from HouTaiStatics import *
excel_header = ['caseid','serieasId','markerId','taskId','timeEnd_Begin','time','isReview']
def getDoctorsListName():
    database = database121
    sql = SqlOperator(logger=None, conf = database)
    caseInfo = list(sql. get_list_from_sql('user'))
    dictIdName = {}
    for idx, Doc in enumerate(caseInfo):
        dictIdName[Doc['id']] = Doc['username']
    return dictIdName
    
class Doctor():
    @classmethod
    def getList(cls,pPath = f'../../Data{config.server}'):
        """
        : excel_header = ['caseid','serieasId','markerId','taskId','timeEnd_Begin','time','isReview']
        : 在运行之前需要运行这个静态方法，获取静态变量
        1. 获取从服务器中生成的accurateTime.npy文件， one sheet one doctor
        2. 静态变量ListDoctor存储医生的列表
        3. ListDoctorMesage 存储医生的标注详细信息
        4. dictIdName 从服务器中获取医生的名字，医生的名字在服务器上为公用的
        """
        liPath = os.path.join(pPath,'accurateTime.npy')
        ListDoctorMesage = np.array(np.load(liPath,allow_pickle=True))
        ListDoctor = []
        ListDoctorMesagetmp = []
        for idx, DoctorMesage in enumerate(ListDoctorMesage):
            if DoctorMesage != []:
                ListDoctor.append(DoctorMesage[0][2])
                ListDoctorMesagetmp.append(DoctorMesage)
        Doctor.ListDoctor = np.array(ListDoctor)
        Doctor.ListDoctorMesage = np.array(ListDoctorMesagetmp)
        Doctor.dictIdName = getDoctorsListName()

    def __init__(self,doctorId,DoctorList = []):
        """
        : excel_header = ['caseid','serieasId','markerId','taskId','timeEnd_Begin','time','isReview']
        :1. self.data 当前医生所有的数据
        :2. self.index 医生数据在总数据中的索引
        """
        self.id = doctorId
        if self.id not in self.ListDoctor:
            raise Exception('没有在列表中，请重新输入')
        self.index = np.where(Doctor.ListDoctor==self.id)[0][0]
        
        self.data = Doctor.ListDoctorMesage[self.index]
        self.DoctorList = DoctorList

    def __str__(self):
        string = f"id:{self.id},index:{self.index}\n"
        string+= f"ListOfDoctor:{Doctor.ListDoctor}"
        return string

    def dayMesage(self):
        pass
    def taskMesage(self):
        pass
    def message(self):
        pass


if __name__=='__main__':
    getDoctorsListName()
    pass
        
    