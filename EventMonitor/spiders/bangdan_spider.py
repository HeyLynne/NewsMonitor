#!/usr/bin/env python3
# coding: utf-8
# File: news_spider.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-7-15

import scrapy
from lxml import etree
import requests
import urllib.parse
from .extract_news import *
from EventMonitor.items import EventmonitorItem
from .extract_link import *

class NewsSpider(scrapy.Spider):
    name = 'bangdanspider'
    def __init__(self, end = 100):
        # 百度排行榜娱乐版块url
        self.pageurl = "http://top.baidu.com/category?c=2&fr=topcategory_c1"
        self.start = 20
        self.end = 100
        self.step = 20
        self.parser = NewsParser()
        self.link_extractor = LinkExtracter()

    '''获取搜索页'''
    def get_html(self, url):
        r = requests.get(url)
        return r.text

    '''获取新闻列表'''
    def collect_bangdan(self, content):
        html = etree.HTML(content)
        itemlst = html.xpath('//div[@class="box-cont"]')
        bangdans = {}
        for item in itemlst:
            title = item.xpath('./div[@class="hd"]/h2/a/text()')
            if len(title) > 1:
                continue
            title_content = title[0].encode("ISO-8859-1").decode("gbk")
            bangdans[title_content] = []
            items = \
                item.xpath('./div[@class="bd"]/div[@class="tab"]/div[contains(@class,"tab-bd")]/div[@class="tab-box"]/ul[@class="item-list"]/li/div[@class="item-hd"]/a[@class="list-title"]/text()')
            for i in items:
                if u"." in i:
                    continue
                bangdans[title_content].append(i.encode("ISO-8859-1").decode("gbk"))
        return bangdans
    
    def gen_bangdan_result(self, bangdan):
        result = []
        for k, v in bangdan.items():
            result.extend(v)
        return result

    '''采集主函数'''
    def start_requests(self):
        html = self.get_html(self.pageurl)
        bangdan = self.collect_bangdan(html)
        bangdan_result = self.gen_bangdan_result(bangdan)

        if len(bangdan_result) > 0:
            for name in bangdan_result:
                word = urllib.parse.quote_plus(name)
                for page_num in range(self.start, self.end, self.step):
                    url = 'http://news.baidu.com/ns?word=title%3A%28'+word+'%29&pn=' + str(page_num) + '&cl=2&ct=0&tn=newstitle&rn=20&ie=utf-8&bt=0&et=0'
                    news_links = self.link_extractor.collect_newslist(url)
                    for news_link in news_links:
                        param = {'url': news_link, "keyword":name}
                        yield scrapy.Request(url=news_link, meta=param, callback=self.page_parser, dont_filter=True)
        else:
            return
    
    '''对网站新闻进行结构化抽取'''
    def page_parser(self, response):
        data = self.parser.extract_news(response.text)
        if data:
            item = EventmonitorItem()
            item['keyword'] = response.meta['keyword']
            item['news_url'] = response.meta['url']
            item['news_time'] = data['news_pubtime']
            item['news_date'] = data['news_date']
            item['news_title'] = data['news_title']
            item['news_content'] = data['news_content']
            yield item
        return
