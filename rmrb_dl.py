#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LCH @ 2017-04-26 15:21:35

import datetime
import requests
from pyPdf import PdfFileWriter, PdfFileReader

PAGE_NUM = ['%02d' %num for num in range(1, 100)]
output = PdfFileWriter()

if __name__ == "__main__":
    print "download start"
    today = datetime.datetime.now()
    date_str = today.strftime("%Y-%m/%d")
    filename = 'rmrb' + today.strftime("%Y%m%d")
    to_union_list = []
    for page in PAGE_NUM:
        url = 'http://paper.people.com.cn/rmrb/page/%s/%s/%s%s.pdf' %(date_str, page, filename, page) 
        print url
        r = requests.get(url)
        if r.status_code == 200:
            to_union_list.append("%s%s.pdf" %(filename, page))
            print 'done'
        else:
            print 'all finished'
            break
        with open("%s%s.pdf" %(filename, page), "wb") as pdf:
            pdf.write(r.content)
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
