#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'
import requests

url = 'http://httpbin.org/get'
headers = {'User-Agent':'Mozilla/5.0'}

#用户名：309435365
#密码：szayclhp


proxies = {'http':'http://309435365:szayclhp@116.255.162.107:16816'}


res = requests.get(url,proxies=proxies,headers=headers,timeout=3)
res.encoding='utf-8'
print(res.text)