#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'

import requests

url = 'http://httpbin.org/get'
headers = {'User-Agent':'Mozilla/5.0'}
proxies = {'https':'https://115.231.5.230:44524'}

res = requests.get(url,proxies=proxies,headers=headers)
res.encoding='utf-8'
print(res.text)
