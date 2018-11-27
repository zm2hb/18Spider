#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'
import requests
from lxml import etree
import urllib.parse
#爬取百度贴吧图片
class ImageSpider:
    def  __init__(self):
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'}
        self.baseurl = 'http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'

    #获取所有帖子URL列表
    def getPageUrl(self,url):
        #获取贴吧页面的html
        res = requests.get(url,headers=self.headers)
        res.encoding='utf-8'
        html = res.text
        #贴取所有页面帖子的URL
        paresHtml = etree.HTML(html)
        t_list = paresHtml.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        print(t_list)
        for t_href in t_list:
            #拼接帖子URL
            t_url = 'http://tieba.baidu.com' + t_href
            self.getImgeUrl(t_url)

    #获取每个帖子中图片的URL列表
    def getImgeUrl(self,t_url):
        #获取贴子的响应html
        res = requests.get(t_url,headers=self.headers)
        res.encoding ='utf-8'
        html = res.text
        #从帖子html响应提取所有图片和视频的url列表
        parseHtml =etree.HTML(html)
        img_list = parseHtml.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/img/@src | //embed/@data-video')
        #遍历图片列表链接
        for img_link in img_list:
            if img_link[-3:] !='jpg':
                continue
            self.writeImage(img_link)

    #保存图片
    def writeImage(self,img_link):
        #获取文件二进制字节流
        res = requests.get(img_link,headers=self.headers)
        res.encoding='utf-8'
        html=res.content
        #以链接的后10位作为文件名
        filename = img_link[-10:]
        #保存到本地
        with open(filename,'wb') as f:
            f.write(html)

    #主要函数
    def workon(self):
        name = input('贴吧名:')
        begin =int(input('贴吧启始页：'))
        end = int(input('贴吧结束页：'))
        for pn in range(begin,end+1):
            pn = (pn-1)*50
            url = self.baseurl.format(name,pn)
            #urllib.parse方法拼接
            # kw = urllib = {'kw':name}
            # kw = urllib.parse.urlencode(kw)
            # url = 'http://tieba.baidu.com/f?'+kw+'&pn='str(pn)
            self.getPageUrl(url)

if __name__=='__main__':
    spider = ImageSpider()
    spider.workon()