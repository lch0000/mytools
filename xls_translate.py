# -*- coding: utf-8 -*-
'''
Excel文件翻译
'''
import xlrd
import gevent
import logging
from xlutils.copy import copy
from HTMLParser import HTMLParser
from textblob import TextBlob
from gevent import monkey; monkey.patch_socket()

final_text = {}

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='xls_translate.log',
                filemode='w')
logger = logging.getLogger()    #生成一个日志对象

class MLStripper(HTMLParser):
    '''HTML标签过滤'''
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html_text):
    '''返回过滤掉标签后的文字列表'''
    s = MLStripper()
    s.feed(html_text)
    return s.fed
    # return s.get_data()

def section_translate(section, row):
    '''段落翻译，不翻译html标签和无法翻译的字段'''
    global final_text
    if isinstance(section, (str, unicode)):
        sentence_list = strip_tags(section)
        to_translate_list = []
        translated_list = []
        for sentence in sentence_list:
            if len(sentence) <= 3:
                continue
            to_translate_list.append(sentence)
            blob = TextBlob(sentence)
            try:
                translated_list.append(blob.translate(to="zh").string)
            except Exception, e:
                logger.error('出现异常:%s',e)
                translated_list.append(sentence)
        # print to_translate_list, translated_list
        for num in range(len(to_translate_list)):
            section = section.replace(to_translate_list[num], translated_list[num], 1)
        final_text[row] = section
        print section
    else:
        final_text[row] = section
        print section

if __name__ == '__main__':
    excel = xlrd.open_workbook('106974.xls', formatting_info=True)
    w = copy(excel)
    textlist = []
    nodes = []
    for y in range(1,excel.sheet_by_index(0).nrows):
        # 读取待翻译语句
        section_text = excel.sheet_by_index(0).cell(y,5).value
        textlist.append(section_text)
    for no in range(len(textlist)):
        # 分解语句并翻译
        nodes.append(gevent.spawn(section_translate, textlist[no], str(no)))
        # w.get_sheet(0).write(y,6,translated_sec)
    gevent.joinall(nodes)

    for row in range(1,excel.sheet_by_index(0).nrows):
        # 存储进xls文件
        w.get_sheet(0).write(row,6,final_text[str(row)])

    w.save('test_newcode.xls')
