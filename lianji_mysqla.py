#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'

import requests
import re
import pymysql




class LianjiaSpider:
    def __init__(self):
        self.page=1
        #初始化URL
        self.url_temp = 'https://gz.lianjia.com/ershoufang/pg{}/'
        self.headers = {'User-Agent':'Mozilla/5.0'}
        #初始化私密代理
        self.proxies = {'http':'http://309435365:szayclhp@116.255.162.107:16816'}
        #初始化数据库链接对象
        self.db = pymysql.connect('localhost','root','123456','lianjia',charset='utf8')
        self.cursor = self.db.cursor()

    #发送请求获取响应对象
    def get_url_list(self,url):
        res = requests.get(url,proxies=self.proxies,headers=self.headers,timeout=3)
        res.enconding = 'utf-8'
        html = res.text
        self.parse_url(html)

    #正则解析数据
    def parse_url(self,html):
        #正则表达式对象
        p = re.compile(r'<div class="houseInfo">.*?data-el="region">(.*?)</a>.*?class="totalPrice">.*?<span>(.*?)</span>',re.S)
        #正则匹配响应内容
        r_list = p.findall(html)
        self.writeMysql(r_list)

    #保存至Mysql数据库
    def writeMysql(self,r_list):
        ins = 'insert into house(name,price) values(%s,%s)'
        #遍历数据列表
        for r in r_list:
            print(r)
            L =[r[0].strip(),float(r[1].strip())*10000]
            #提交操作
            self.cursor.execute(ins,L)
            self.db.commit()
            print('*********************')

    #循环运行函数
    def run(self):
        while True:
            c = input('爬取Y/退出N')
            if c =='y':
                #拼接URL
                url = self.url_temp.format(str(self.page))
                print(url)
                self.get_url_list(url)
                self.page+=1
            #爬取结束关闭数据库
            else:
                self.cursor.close()
                self.db.close()
                break

if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.run()



