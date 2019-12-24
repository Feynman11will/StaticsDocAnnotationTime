
import sys
import os
import zipfile
sys.path.append('../')
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config import config
from datetime import datetime 
import shutil 
from lib.Zipfile import ZipFile
from config import safeMessConf as safeConf
import pandas as pd


import codecs


class SendEmail():
    def __init__(self,day,sender =None,myPass=None,receivers = None,dstPPath=None):
        self.sender = sender
        self.message = MIMEMultipart()
        self.day = day
        self.myPass = myPass
        self.receivers = receivers
        self.dstPPath = dstPPath
    def getHeader(self):
        
        self.message['From'] = Header(f"{self.sender}")
        
        self.message['To'] =  Header('') # utf-8 
        self.subject = f"内部标注医生工作时长统计{self.day}"
        self.message['Subject'] = Header(self.subject)

    def zipAllMessage(self):
        # 成功进入压缩文件
        print('------>')
        serverlist = config.serverlist
        serverlist.append('AllServer') 
        self.day = '_'.join(map(str,map(int,self.day.split('-'))))
        print(self.day)

        self.sourceFileList = ['accurateTime.xlsx','allInday.xlsx','synthesisAllOfServer.xlsx']
        self.dstFileList = [f'{self.day}医生原始统计.xlsx',f'{self.day}分析统计.xlsx',f'{self.day}分析结果服务器综合.xlsx']
        
        pathTmp = config.pPath
        
        for  server in serverlist:
            dstPPath = self.dstPPath
            print(f"dstPPath:-->{dstPPath}")
            print(f"dstPPath:-->{self.day}")
            dstPath = os.path.join(dstPPath,self.day)
            if pathTmp.split('/')[-2:][0].startswith('Data'):
                pathTmp = '/'.join(pathTmp.split('/')[0:-2])
                pathTmp = os.path.join(pathTmp,f"Data{server}",self.day)
                print(pathTmp)

            if not os.path.exists(dstPath):
                os.makedirs(dstPath)
            if isinstance(server,str) and server.endswith('Server'):
                sourceFile = self.sourceFileList[2]
                sourcePath = os.path.join(pathTmp,sourceFile)
                self.dstFile  = dstFile= os.path.join(dstPath,f"服务器{server}_"+self.dstFileList[2])
                if os.path.exists(sourcePath):
                    shutil.copyfile(sourcePath,dstFile)
            else:
                for idx, sourceFile in enumerate(self.sourceFileList):
                    if idx < len(self.sourceFileList)-2:
                        sourcePath = os.path.join(pathTmp,sourceFile)
                        dstFile = os.path.join(dstPath,f"服务器{server}_"+self.dstFileList[idx])
                        shutil.copyfile(sourcePath,dstFile)
        
        startdir = os.path.join(self.dstPPath,self.day)
        file_news = os.path.join(self.dstPPath,f'{self.day}.zip')
        ZipFile()(startdir = startdir,file_news = file_news)
        self.sendAttachPath  = file_news

    def messageAttach(self):
        self.getHeader()
        self.zipAllMessage() #生成压缩包
        self.message.attach(MIMEText('统计结果', 'plain', 'utf-8'))
        att1 = MIMEText(open(self.sendAttachPath, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        filename = self.sendAttachPath.split('/')[-1]
        att1["Content-Disposition"] = f'attachment; filename="{filename}"'
        self.message.attach(att1)


        self.readXlsx2Excel()

        self.Html=f"""
        以下为内部服务器{self.day}日标注时间统计情况：<br>
        
        """ + self.Html 

        self.message.attach(MIMEText(self.Html, 'html', 'utf-8'))
    

    def emailSend(self):
        self.messageAttach()
        try:
            if self.sender.endswith('qq.com'):
                self.sendServer = "smtp.qq.com"
            else :
                self.sendServer = "smtp.mxhichina.com"
            self.server=smtplib.SMTP_SSL(self.sendServer, 465)  # 发件人邮箱中的SMTP服务器，端口是465
            self.server.login(self.sender, self.myPass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            self.server.sendmail(self.sender, self.receivers,self.message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

    def readXlsx2Excel(self):
        inputXlsx = self.dstFile
        xd = pd.ExcelFile(inputXlsx)
        pd.set_option('display.max_colwidth',1200)#设置列的宽度，以防止出现省略号
        df = xd.parse()
        self.inputXlsx = inputXlsx.replace('.xlsx','.html')
        with codecs.open(self.inputXlsx,'w') as html_file:
            html_file.write(df.to_html(header = True,index = False))
        self.Html = """"""
        
        with open(self.inputXlsx,'r') as htmlR:
            Html = htmlR.readlines()
            print(type(Html))
            print(len(Html))
            for h in Html:
                self.Html += h
        
if __name__=='__main__':
    
    day = str(str(datetime(2019,12,4))).split(' ')[0]
    sender = safeConf.AliSender
    myPass = safeConf.AliPass
    receivers = safeConf.receivers
    
    objSender = SendEmail(day = day,
                        sender=sender,
                        myPass=myPass,
                        receivers = receivers,
                        dstPPath='../../testZip')

    objSender.emailSend()
