# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from nba.items import NbaStoryItem

class EspnSpider(CrawlSpider):
    name = "espn"
    allowed_domains = ["espn.com"]
    start_urls = ['http://espn.com/nba/']
    
    rules = (
#            Rule(LinkExtractor(allow=(r'/nba/story/_/id.+',),restrict_css='a'), callback='parse_story_item'),
#            Rule(LinkExtractor(allow=(r'/espn/now/.+',), restrict_css='a'), callback='parse_now_item'),
             Rule(LinkExtractor(allow=('/espn.+?nowId=.+',), restrict_css='a'), callback='parse_now_item'),
            )

    def parse_story_item(self, response):
        nba_story_item = NbaStoryItem()
        nba_story_item['title'] = response.css('header.article-header>h1::text').extract()[0]
        nba_story_item['time'] = response.css('span.timestamp::attr(data-date)').extract()[0]
        nba_story_item['content'] = response.css('div.article-body p,img,h2').extract()
        nba_story_item['piclink'] = response.css('picture>source:nth-child(1)::attr(srcset)').extract()
        
        return nba_story_item
    
    def parse_now_item(self, response):
        nba_now_item = NbaStoryItem()
        nba_now_item['title'] = response.css('span.author::text').extract()[0]
        nba_now_item['content'] = response.css('p.contentItem__subhead::text').extract()
        nba_now_item['time'] = 0
        
        return nba_now_item
