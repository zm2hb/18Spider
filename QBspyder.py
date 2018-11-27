# -*- coding: utf-8 -*-

import requests
from lxml import etree
import csv
import pymongo
'''

Created on Tue Nov 20 2018
@author:Benben
糗事百科爬虫

'''

class QiubaiSpider:
    #初始化url请求头
    def __init__(self):
        self.url_temp='https://www.qiushibaike.com/8hr/page/{}/'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        #链接数据库对象
        self.conn = pymongo.MongoClient('localhost',27017)
        #库对象
        self.db = self.conn['Qiushi']
        #集合对象
        self.myset = self.db['qiushiinfo']
       #csv文件表头
        with open('qb.csv','w',newline='') as f:
            headers = ['author_name','content','stats_vote','stats_comments','img']
            self.writer = csv.DictWriter(f,headers)
            self.writer.writeheader()
   
    #根据url地址的规律构造url_list
    def get_url_list(self):
        url_list = [self.url_temp.format(i) for i in range(1,14)]
        return url_list
    
    #发送请求
    def parse_url(self,url):
        #获取响应
        response = requests.get(url,headers=self.headers)
        #返回响应解析
        return response.content.decode()
    
    #获取数据
    def get_content_list(self,html_str):
        html = etree.HTML(html_str)
        #数据分组
        content_list = []
        div_list = html.xpath("//div[@id='content-left']/div")
        for div in div_list:
            print('正在读取')
            item = {}
            #用户名
            item['author_name'] = div.xpath('.//h2/text()')[0].strip() if len (div.xpath('.//h2/text()')) > 0 else None
            #内容
            item['content']=div.xpath('.//div[@class="content"]/span/text()')
            item['content']=[i.strip() for i in item['content']]
            #评论数
            item['stats_vote']=div.xpath('.//span[@class="stats-vote"]//i/text()')
            item['stats_vote']=item['stats_vote'][0] if len(item['stats_vote'])>0 else None
            #好笑数
            item['stats_comments']=div.xpath('.//span[@class="stats-comments"]//i/text()')
            item['stats_comments']=item['stats_comments'][0] if len(item['stats_comments'])>0 else None
            #获取图片链接
            item['img'] = div.xpath('.//div[@class="thumb"]//img/@src')
            item['img'] = item['img'][0] if len(item['img'])>0 else None
            content_list.append(item)            
        return content_list
    
    #保存数据
    def save_content_list(self,content_list):
       
#        print(content_list)        print(img_list)
        with open('qb.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            print(content_list)
            cl = content_list
            #写入数据
            for content in cl:
#                print(content)
                writer.writerow(content.values())
#                f.write(json.dumps(content,ensure_ascii=False)) #保存txt文件
#                f.write('\n')
                print('保存成功')

    #保存进mongodb数据库
    def save_parse_Page(self,content_list):
        self.myset.insert(content_list)

    
    #主要运行逻辑
    def run(self):
        #根据url地址的规律,构造url_list
        url_list = self.get_url_list()
        #发送请求，获取响应
        for url in url_list:
            html_str = self.parse_url(url)
            #执行解析数据
            content_list = self.get_content_list(html_str)
            #保存文件
            self.save_content_list(content_list)
            self.myset.insert(content_list)
        
if __name__ == '__main__':
    qb = QiubaiSpider()
    qb.run()