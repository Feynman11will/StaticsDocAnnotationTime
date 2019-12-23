import sys
import os
import numpy as np 
sys.path.append('../')
from config import config 
from HouTaiStatics import *

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
        
    