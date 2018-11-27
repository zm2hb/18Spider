#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'
import requests
import re
import pymongo

class LianjiaSpider:
    def __init__(self):
        self.baseurl = "https://bj.lianjia.com/ershoufang/pg"
        self.headers = {"User-Agent":"Mozilla/5.0"}
        self.proxies = {"http":"http://309435365:szayclhp@116.255.162.107:16816"}
        self.page = 1
        self.conn = pymongo.MongoClient("localhost",27017)
        self.db = self.conn["lianjia"]
        self.myset = self.db["house"]

    def getPage(self,url):
        res = requests.get(url,proxies=self.proxies,headers=self.headers)
        res.encoding = "utf-8"
        html = res.text

        self.parsePage(html)

    def parsePage(self,html):
        p = re.compile('<div class="houseInfo">.*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>',re.S)
        r_list = p.findall(html)
        self.writeMysql(r_list)

    #保存至Mysql数据库
    def writeMysql(self,r_list):
        ins = 'insert into house(name,price) values(%s,%s)'
        #遍历数据列表
        for r in r_list:
            D = {
                "name":r[0].strip(),
                "price":float(r[1].strip())*10000
                }
            self.myset.insert(D)


    def workOn(self):
        while True:
            c = input("y爬取/任意键结束:")
            if c == "y":
                url = self.baseurl + \
                      str(self.page) + "/"
                self.getPage(url)
                self.page += 1
            else:
                break

if __name__ == "__main__":
    spider = LianjiaSpider()
    spider.workOn()


















