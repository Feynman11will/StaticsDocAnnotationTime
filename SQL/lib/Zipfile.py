import zipfile
import os 
class ZipFile():
    def __call__(self,startdir, file_news):
        z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename),fpath+filename)
                print ('压缩成功')
        z.close()