#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LCH @ 2017-04-26 15:21:35

import os
import sys
import time
import shutil
import datetime
import requests
from requests.adapters import HTTPAdapter
from pyPdf import PdfFileWriter, PdfFileReader

PAGE_NUM = ['%02d' %num for num in range(1, 100)]

#获取当前路径  
def fileDir() :  
    path = sys.path[0]  
    print '当前路径为' + path
    #判断为脚本文件还是编译后文件，如果是脚本文件则返回脚本目录，否则返回编译后的文件路径  
    if os.path.isdir(path) :  
        return path  
    elif os.path.isfile(path) :  
        return os.path.dirname(path)  
  
#获取文件后缀名  
def suffix(file, *suffixName) :  
    array = map(file.endswith, suffixName)  
    if True in array :  
        return True  
    else :  
        return False  
  
#删除目录下扩展名为.o,.exe,.bak的文件  
def deleteFile() :  
    targetDir = fileDir()  
    for file in os.listdir(targetDir) :  
        targetFile = os.path.join(targetDir, file)  
        if suffix(file, '.pdf'):  
            os.remove(targetFile)  

def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    time.sleep(5)
                    return func(*args, **kw)
                except Exception as e:
                    att += 1
                    print '下载错误! 第%s次重试' % att
        return wrapper
    return decorator

@retry(attempt=100)
def get_response(url):
    r = requests.get(url)
    print r.status_code
    return {'content': r.content, 'status': r.status_code}

if __name__ == "__main__":
	while True:
		output = PdfFileWriter()
		today = datetime.datetime.now()
		date_str = today.strftime("%Y-%m/%d")
		filename = 'rmrb' + today.strftime("%Y%m%d")
		# 判断当日的报纸是否已经下载完成
		if os.path.exists('/data/rmrb/%s.pdf' %filename):
			file_exist_flag = True
		else:
			file_exist_flag = False	
		# 七点至八点之间执行下载任务
		if today.hour in (7,8) and file_exist_flag == False:
			to_union_list = []
			print "download start"
			for page in PAGE_NUM:
				if os.path.exists('/root/src/rmrb/%s%s.pdf' %(filename, page)):
					to_union_list.append("%s%s.pdf" %(filename, page))
					continue
				url = 'http://paper.people.com.cn/rmrb/page/%s/%s/%s%s.pdf' %(date_str, page, filename, page) 
				print url
				r = get_response(url)
				if r['status'] == 200:
					to_union_list.append("%s%s.pdf" %(filename, page))
					print 'done'
				else:
					print 'all finished'
					break
				with open("%s%s.pdf" %(filename, page), "wb") as pdf:
					pdf.write(r['content'])
			outputPages = 0
			for names in to_union_list:
				inputfile = PdfFileReader(file(names, "rb"))

				# 如果加密了,必须先解密
				if inputfile.isEncrypted == True:
					inputfile.decrypt("map")

				# 获得源pdf文件中页面总数
				page_count = inputfile.getNumPages()
				outputPages += page_count
				# print page_count

				# 分别将page添加到输出output中
				for ipage in range(0, page_count):
					output.addPage(inputfile.getPage(ipage))

			print "All Pages Number:" + str(outputPages)
			outputStream = file("%s.pdf" %filename, "wb")
			output.write(outputStream)
			outputStream.close()
			print "finished"
			# 将文件拷贝到指定位置
			print '拷贝文件到指定位置'
			shutil.copy('/root/src/rmrb/%s.pdf' %filename, '/data/rmrb/%s.pdf' %filename)
			shutil.copy('/root/src/rmrb/%s.pdf' %filename, '/data/rmrb/rmrb.pdf')
		if today.hour == 23 and file_exist_flag == True:
			print '开始清理'
			# 每天23点后删除当天的报纸
			os.remove('/data/rmrb/%s.pdf' %filename)
			# 清理本目录下数据
			deleteFile()
        time.sleep(600)
