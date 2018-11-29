# -*- coding: utf-8 -*-
import requests
from lxml import etree
from queue import Queue
import threading
import time


class bsSpider:
    def __init__(self):
        self.baseurl = 'http://www.budejie.com/{}'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
        #URL队列
        self.urlQueue = Queue()
        #响应URL队列
        self.resQueue = Queue() 
    
    #生成URL队列
    def getUrl(self):
        for pNum in range(1,51):
            #拼接URL放到队列里
            url = self.baseurl.format(pNum)
            self.urlQueue.put(url)
            
            
    
    #请求，得到响应html,放到解析队列
    def getHtml(self):
        while True:
            #从URL队列中get值
            url = self.urlQueue.get()
            #发请求得响应put到响应队列中
            res = requests.get(url,headers=self.headers)
            res.encoding = 'utf-8'
            html = res.text
            #响应HTML放到队列
            self.resQueue.put(html)
            #清除此任务
            self.urlQueue.task_done()
            
    #解析页面方法
    def getText(self):
        while True:
            html = self.resQueue.get()
            parseHtml = etree.HTML(html)
            r_list = parseHtml.xpath('//div[@class="j-r-list-c-desc"]/a/text()')
            for r in r_list:
                print(r+'\n')
            #清除此任务
            self.resQueue.task_done()
    
    #实现多线程
    def run(self):
        #空列表用来存放所有的线程
        th_list = []
        #生成URL队列
        self.getUrl()
        #创建请求线程，放到列表中
        for i in range(3):
            th_res = threading.Thread(target=self.getHtml)
            th_list.append(th_res)
        
        #创建解析线程，放到列表中
        for i in range(3):
            th_parse = threading.Thread(target=self.getText)
            th_list.append(th_parse)
        
        #所有线程开始运行
        for th in th_list:
            th.setDaemon(True)
            th.start()
            
        #如果队列为空，则执行其他程序
        self.urlQueue.join()
        self.resQueue.join()
            
    
if __name__=="__main__":
    begin = time.time()
    spider =bsSpider()
    spider.run()
    end = time.time()
    print(end-begin)