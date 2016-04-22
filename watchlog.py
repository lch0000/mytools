# -*- coding: utf-8 -*-
'''
使用multitail查看指定目录下文件名正则匹配的log文件
1 查找当前目录下所有的文件名
2 正则匹配所有的文件名,选择需要的log文件
3 使用multitail打开并监控所有符合条件的log
'''
import os
import re
import sys
import datetime

def IsSubString(SubStrList,Str):
    '''''
    #判断字符串Str是否包含序列SubStrList中的每一个子字符串
    #>>>SubStrList=['F','EMS','txt']
    #>>>Str='F06925EMS91.txt'
    #>>>IsSubString(SubStrList,Str)#return True (or False)
    '''
    flag=True
    for substr in SubStrList:
        if not(substr in Str):
            flag=False

    return flag

def GetFileList(FindPath,FlagStr=[]):
    '''''
    #获取目录中指定的文件名
    #>>>FlagStr=['F','EMS','txt'] #要求文件名称中包含这些字符
    #>>>FileList=GetFileList(FindPath,FlagStr) #
    '''
    import os
    FileList=[]
    FileNames=os.listdir(FindPath)
    if (len(FileNames)>0):
       for fn in FileNames:
           if (len(FlagStr)>0):
               #返回指定类型的文件名
               if (IsSubString(FlagStr,fn)):
                   fullfilename=os.path.join(FindPath,fn)
                   FileList.append(fullfilename)
           else:
               #默认直接返回所有文件名
               fullfilename=os.path.join(FindPath,fn)
               FileList.append(fullfilename)

    #对文件名排序
    if (len(FileList)>0):
        FileList.sort()

    return FileList


if __name__ == '__main__':
    # 输出当天的日期和基础定义
    datestr = datetime.datetime.today().strftime('%Y-%m-%d')  # %Y-%m-%d-%H-%M-%S 指定日期格式
    filename = ['logger', datestr]  # 要查看的文件名
    print filename
    # 输出当前文件路径
    project_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在路径
    print project_path
    # 输出所有匹配文件名
    filenames = GetFileList(project_path, filename)
    print filenames
    # 使用multitail打开并监控所有符合条件的log
    parm = ' -i '
    parmlist = parm.join(filenames)
    print parmlist
    os.system('multitail -i %s' %parmlist)
