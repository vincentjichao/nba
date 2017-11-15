# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime,timedelta
from scrapy.exceptions import DropItem
import email
import smtplib

class NbaStoryTimeCheckPipeline(object):
    
    def process_item(self, item, spider):
        #checktime = timedelta(hours=0.6)
        timenow = datetime.today()
        storytime = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%SZ')
        cha_time = timenow - storytime - timedelta(hours=8)
        if cha_time.total_seconds()/3600 < 0.6:
            return item
        else:
            raise DropItem('历史文章-----'+item['time'])
            
class NbaStoryMailPipeline(object):
    
    def process_item(self, item, spider):
        mail_server = smtplib.
