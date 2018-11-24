#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Benben'
import requests
import csv
from lxml import etree
import pymysql
import warnings

class maoyanSpider:
    def __init__(self):
        self.url_temp='http://maoyan.com/board/4?offset={}'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
       #csv文件表头
        with open('mayan.csv','r+',newline='') as f:
            headers = ['电影名称','主演','上映时间']
            self.writer = csv.DictWriter(f,headers)
            self.writer.writeheader()
        #创建数据库链接对象
        self.db = pymysql.connect('localhost','root','123456',charset='utf8')
        #创建游标
        self.cursor = self.db.cursor()
        #execute(sql命令)


    def get_url_list(self):
        url_list = [self.url_temp.format((i-1)*10) for i in range(1,11)]
        print(url_list)
        return url_list
        
    def prase_ulr(self,url):
        res = requests.get(url,headers=self.headers)
        return res.content.decode()
    
    def get_content_list(self,html_str):
        html = etree.HTML(html_str)
        content_list = []
        div_list = html.xpath('/html/body/div[4]/div/div/div[1]/dl/dd')
        for dd in div_list:
            item={}
            item['电影名称'] = dd.xpath('.//p[@class="name"]/a/@title')[0]
            item['主演'] = dd.xpath('.//p[@class="star"]/text()')[0].strip()
            item['上映时间'] = dd.xpath('.//p[@class="releasetime"]/text()')[0]
            content_list.append(item)
        return content_list
            
    def writeTocsv(self,content_list):
        with open('mayan.csv','a',newline='',encoding='utf-8') as f:
            write = csv.writer(f)
            for content in content_list:
                write.writerow(content.values())

    def writeTomysql(self,content_list):
        c_db = "create database if not exists spiderdb charset utf8"
        u_db = 'use spiderdb'
        c_tab = 'create table if not exists top100( \
                id int primary key auto_increment,\
                name varchar(50),star varchar(100),\
                time varchar(50))'
        ins = 'insert into top100(name,star,time) values(%s,%s,%s)'
        warnings.filterwarnings('ignore')
        try:
            self.cursor.execute(c_db)
            self.cursor.execute(u_db)
            self.cursor.execute(c_tab)
        except:
            pass

        for r_dict in content_list:
            L = [r_dict['电影名称'],r_dict['主演'],r_dict['上映时间']]
            self.cursor.execute(ins,L)
            self.db.commit()
            print('yes')

    def run(self):
        url_lisr = self.get_url_list()
        for url in url_lisr:
            print(url)
            html_str = self.prase_ulr(url)
            content_list=self.get_content_list(html_str)
            self.writeTocsv(content_list)
            self.writeTomysql(content_list)
    
if __name__ =='__main__':
    my = maoyanSpider()
    my.run()