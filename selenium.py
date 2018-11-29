# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import csv

class DouyuSpider:
    def __init__(self):
        #创建浏览器对象
        opt = webdriver.ChromeOptions()
        #设置无界面
        opt.set_headless()
        self.driver = webdriver.Chrome(options=opt)
          
    # 获取数据（主播名&观众数量）
    def getData(self):
        #发送请求
        self.driver.get('https://www.douyu.com/directory/all')
        #创建xpath的解析对象
        parseHtml = etree.HTML(self.driver.page_source)
        names = parseHtml.xpath('//div[@id="live-list-content"]//span[@class="dy-name ellipsis fl"]/text()')
        numbers = parseHtml.xpath('//div[@id="live-list-content"]//span[@class="dy-num fr"]/text()')
        for name,number in zip(names,numbers):
            L = [name.strip(),number.strip()]
            self.writeData(L)
        
    #保存到CSV文件
    def writeData(self,L):
        with open('douyu.csv','a',newline='',encoding='gb18030') as f:
            write = csv.writer(f)
            write.writerow(L)
    #主函数
    def workOn(self):
        while True:
            self.getData()
            if self.driver.page_source.find("shark-pager-next shark-pager-disable shark-pager-disable-next") == -1:
                self.driver.find_element_by_class_name("shark-pager-next").click()
            else:
                print('爬取结束')
                self.driver.close()
                break
            
    
if __name__ == '__main__':
    spider = DouyuSpider()
    spider.workOn()

