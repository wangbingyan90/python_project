#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
#小橙子api
#

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
import re

url = 'http://43.225.157.231/api/values/GetShort'

headers = {
    'Host': "www.520yb.top",
    'Connection':"keep-alive",
    'Accept':"application/json",
    'X-Requested-With':"XMLHttpRequest",
    'User-Agent':"Mozilla/5.0 (Linux; Android 6.0.1; C106 Build/ZAXCNFN5801712291S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.91 Mobile Safari/537.36 Html5Plus/1.0",
    'Content-Type':"application/json",
    'Accept-Encoding':"gzip, deflate",
    'Accept-Language':"zh-CN,en-US;q=0.8"
    }

r = requests.get(url,headers=headers,timeout=30).text
s = r[30:3000]
hrefs = re.findall(r'shorturl\":\"(.*?)\"',s)
url = '链接:\n'
for one in hrefs:
    url = url + 'https://pan.baidu.com/mbox/homepage?short=' + one +'\n'
print (url)
