#coding=utf-8
import requests
from lxml import etree

if __name__ == "__main__":
    r = requests.get("http://top.baidu.com/category?c=2&fr=topcategory_c1")
    html = etree.HTML(r.text) 
    # 获取榜单内容
    itemlst = \
        html.xpath('//div[@class="box-cont"]')
    for item in itemlst:
        title = item.xpath('./div[@class="hd"]/h2/a/text()')
        for i in title:
            print(i.encode("ISO-8859-1").decode("gbk"))
        items = \
            item.xpath('./div[@class="bd"]/div[@class="tab"]/div[contains(@class,"tab-bd")]/div[@class="tab-box"]/ul[@class="item-list"]/li/div[@class="item-hd"]/a[@class="list-title"]/text()')
        for i in items:
            print(i.encode("ISO-8859-1").decode("gbk"))
        print("****")
