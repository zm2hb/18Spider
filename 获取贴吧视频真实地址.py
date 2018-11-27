#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'
import requests

url = 'http://tb-video.bdstatic.com/tieba-smallvideo-transcode/11513982_bbd7426663f061230c83a7afc8ea36f1_0.mp4'
headers  = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'}
res = requests.get(url,headers=headers)
res.encoding='utf-8'
html = res.text
with open('t.html','w',encoding='utf-8') as f:
    f.write(html)