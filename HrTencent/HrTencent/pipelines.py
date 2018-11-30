# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class HrtencentPipeline(object):
    def process_item(self, item, spider):
        print(item.values())
        with open('腾讯招聘.csv','a',newline='',encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerow(item.values())
            print('--------------')

