#coding=utf-8
from lxml import etree
import urllib.request
import urllib.parse

class LinkExtracter(object):
    def __init__(self):
        return
    
    '''获取搜索页'''
    def get_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        return html
    
    '''获取新闻列表'''
    def collect_newslist(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        urls = selector.xpath('//h3[@class="c-title"]/a/@href')
        return set(urls)