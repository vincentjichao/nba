# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from nba.items import NbaStoryItem

class EspnSpider(CrawlSpider):
    name = "espn"
    allowed_domains = ["espn.com"]
    start_urls = ['http://espn.com/nba/']
    
    rules = {
            Rule(LinkExtractor(allow=(r'/nba/story/_/id.+',),restrict_css='a'), callback='parse_item')
            }

    def parse_item(self, response):
        nba_story_item = NbaStoryItem()
        nba_story_item['title'] = response.css('header.article-header>h1::text').extract()[0]
        nba_story_item['time'] = response.css('span.timestamp::attr(data-date)').extract()[0]
        nba_story_item['content'] = response.css('div.article-body>p').extract()
        nba_story_item['piclink'] = response.css('source::attr(data-srcset)').extract()
        return nba_story_item
