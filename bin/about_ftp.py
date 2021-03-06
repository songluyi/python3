# -*- coding: utf-8 -*-
# 2016/7/31 21:31
"""
-------------------------------------------------------------------------------
Function:   一键上传至FTP
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 
 
-------------------------------------------------------------------------------
"""
import paramiko,re
import os,time,shutil
from cqs_branch_connect_database import get_batch_id

def get_ini():
    with open('setting.ini','r',errors='ignore') as f:
        data=f.readlines()
    return [data[4].replace('\n',''),data[5].replace('\n','')]
db_connect=get_ini()[1]
def get_path():
    import os
    current_path=os.path.abspath(os.path.join(os.path.dirname('cqs_index.py'),os.path.pardir))
    new_path=current_path+'\\'+'excel\\'
    FileList = []
    rootdir = new_path
    for root, subFolders, files in os.walk(rootdir):
        #排除特定的子目录
        if 'done' in subFolders:
            subFolders.remove('done')
        #查找特定扩展名的文件，只要包含'索引表'但不包含"new"字符串的文件，都会被包含
        for f in files:
            if f.find('表') != -1 and f.find('new')==-1:
                FileList.append(os.path.join(root, f))
    return FileList

if __name__ == '__main__':
    ftp_ini=get_ini()[1]
    today_time=time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    new_ftp_path=str(today_time)+' '+str(get_batch_id())
    parent_path=os.path.abspath(os.path.join(os.path.dirname('cqs_index.py'),os.path.pardir))
    os.chdir(parent_path)
    remotepath='/'+new_ftp_path+'/'
    # file_path='/backup/'+new_ftp_path
    os.mkdir(new_ftp_path)
    base_path=os.getcwd()#获取当前目录
    namelist=get_path()
    for name in namelist:
        shutil.copy(name,new_ftp_path)
        print(name)
    excel_path=base_path+'\\'+new_ftp_path
    os.chdir(excel_path)
    print(os.getcwd())
    namelist=get_path()
    count_index=1
    count_rate=1
    ftp_name=re.findall('(.*?)/',ftp_ini)
    ftp_pass=re.findall('/(.*?)@',ftp_ini)
    ftp_ip=re.findall('@(.*?):',ftp_ini)
    row_ftp_port=re.findall(':\d*',ftp_ini)
    ftp_port=row_ftp_port[0].replace(':','')
    ftp=paramiko.Transport((ftp_ip[0], int(ftp_port)))
    ftp.connect(username=ftp_name[0], password=ftp_pass[0], hostkey=None)
    sftp =paramiko.SFTPClient.from_transport(ftp)
    sftp.mkdir(new_ftp_path)
    print(sftp.listdir())
    print(sftp.getcwd())
    for name in namelist:
        if '索引表' in name:
            newname='cqs_index_'+''+'uploaded_'+str(count_index)+'.xlsx'
            count_index+=1
            os.rename(name,newname)
            remotepath_index=remotepath+newname
            sftp.put(newname,remotepath_index)
        if '等级表' in name:
            newname='cqs_rate_'+'uploaded'+str(count_rate)+'.xlsx'
            count_rate+=1
            os.rename(name,newname)
            remotepath_rate=remotepath+newname
            sftp.put(newname,remotepath_rate)
    print(sftp.listdir())
    ftp.close()