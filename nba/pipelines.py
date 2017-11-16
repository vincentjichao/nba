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
        if item['time'] == 0:
            item['content'] = item['content'][0]
            return item
        #checktime = timedelta(hours=0.6)
        timenow = datetime.today()
        storytime = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%SZ')
        cha_time = timenow - storytime - timedelta(hours=8)
        #if item
        if cha_time.total_seconds()/3600 < 0.6:
            con = ''
            for i in item['piclink']:
                con += '<img src="' + i + '" />' + '<br />'
            for i in item['content']:
                con += i
            item['content'] = con
            return item
        else:
            raise DropItem('历史文章-----'+item['time'])
            
class NbaStoryMailPipeline(object):
    
    def process_item(self, item, spider):
        mail_server = smtplib.SMTP(host='smtp.qq.com', port=587)
        mail_server.starttls()
        mail_server.set_debuglevel(1)
        mail_server.login(user='497521249@qq.com', password='mferuahgophvcbcg')
        msg = email.mime.text.MIMEText(item['content'], 'html', 'utf-8')
        msg['From'] = 'vincent'
        msg['To'] = 'somebody'
        msg['Subject'] = email.header.Header(item['title'], 'utf-8').encode()
        mail_server.sendmail('497521249@qq.com', 
                             ['497521249@qq.com', '2488317486@qq.com'],
                             msg.as_string())
        mail_server.quit()
        return item
