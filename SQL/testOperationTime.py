'''
@Author: your name
@Date: 2019-12-04 10:19:55
@LastEditTime: 2019-12-04 11:15:11
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /taskStatics/SQL/testOperationTime.py
'''
"""
1. sql.get_from_sql(table = 't_eva_task',key = 'status',key_value='10')
    从 t_eva_task 列表中读取状态为10的任务项目
    得到lNameSet，该列表中包含了所有符合条件的{taskId,taskNames}字典
2. getTasks(lNameSet,print2Screen = False)函数对
    肺全科   
    肺结节   
    脑梗塞   
    纵膈     
    脑全科   
    胸部骨折 
    肋骨骨折 
    肋骨轮廓 
    血管     
    9个大类的任务按照名称关键字查询得到相应的任务和任务的id
3. 使用getSamples(taskList,saveNpy = False)对获取每个任务样本的id
    getTaskIdSamples = list(sql.get_from_sql(table = 't_eva_case',key = 'taskId',key_value=keys[0]))
    其中每一个样本有多个子序列,同一个样本的patientID相同，任务号码相同，但是自增id不同，可以通过patientid计算有多少个样本。
    自增id可以用来在t_user_operation统计一个序列的操作时间。

"""