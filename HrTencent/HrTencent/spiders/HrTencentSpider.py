# -*- coding: utf-8 -*-
import scrapy
from ..items import HrtencentItem
from lxml import etree


class HrtencentspiderSpider(scrapy.Spider):
    name = 'HrTencentSpider'
    allowed_domains = ['hr.tencent.com']
    #定义一个基准的url,方便后期拼接290个URL
    url = 'https://hr.tencent.com/position.php?start='
    start = 0
    #拼接初始的URl
    start_urls = [url + str(start)]

    #paser函数是第一次从start_ulrs中初始URL发情求
    #得到响应后必须要调用的函数return item
    def parse(self, response):
        for i in range(0,2891,10):
            #scrapy.Request()

            yield scrapy.Request(self.url+str(i),callback=self.parseHTML)

    def parseHTML(self,response):
        baseList = response.xpath('//tr[@class="odd"]| //tr[@class="even"]')
        for base in baseList:
            item = HrtencentItem()
            # 职称
            item['zhName'] = base.xpath('./td[1]/a/text()').extract()[0]
            # 链接
            item['zhLink'] = base.xpath('./td[1]/a/@href').extract()[0]
            # 类别
            item['zhType'] = base.xpath('./td[2]/text()').extract()[0] if len ( base.xpath('./td[2]/a/text()')) > 0 else None
            # 人数
            item['zhNum']= base.xpath('./td[3]/text()').extract()[0]
            # 地点
            item['zhAddress'] = base.xpath('./td[4]/text()').extract()[0]
            # 时间
            item['zhTime'] = base.xpath('./td[5]/text()').extract()[0]
            yield item
