# Introduction
Crawl news with a specific keyword. We also implemented a function which could get the hotest keywords from Baidu Bangdan and crawl news about these keywords.
# Enviroment
- python 3.7.0
- Other requirements please checkout the requirements.txt
# Usage
- To crawl a specific keyword, please use
```
scrapy crawl eventspider -a keyword=关键字
```
- To crawl BaiduBangdan please use
```
scrapy crawl bangdanspider
```
The news will be stored under "news" file folder.
