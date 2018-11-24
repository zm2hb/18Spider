# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:13:17 2018

@author: Administrator
"""
import requests
import re

class nhspider:
        def __init__(self):
            self.baseurl = 'https://www.neihan8.com/njjzw/'
            self.headers = {'User-Agent':'Mozilla/5.0'}
            
        #获取页面
        def getPage(self,url):
            res = requests.get(url,headers=self.headers)
            html = res.content.decode('utf-8')
            print(html)
            self.parsePage(html)
            
         #解析页面
        def parsePage(self,html):
            p = re.compile(r'<div class="text-column-item box box-790">.*?title="(.*?)">.*?<div class="desc">(.*?)</div>',re.S)
            r_list = p.findall(html)
            print(r_list)
            self.writePage(r_list)
            
        #保存数据 
        def writePage(self,r_list):
            for r_tuple in r_list:
                for r_str in r_tuple:
                    with open('脑筋急转弯.txt','a',encoding='gb18030') as f:
                        f.write(r_str.strip()+'\n')
                with open('脑筋急转弯.txt','a',encoding='gb18030') as f:
                        f.write('\n')
            
        #主函数
        def run(self):
            self.getPage(self.baseurl)
#            while True:
#                c =input('是否继续')
#                if c.strip().lower() == 'y':
#                    self.Page +=1
#                    url = self.baseurl +'index_{}.html'
    



if __name__ == '__main__':
    spider = nhspider()
    spider.run()
