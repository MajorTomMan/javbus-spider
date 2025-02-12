'''
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 18:25:15
FilePath: \spider\javbus\spiders\actress_list_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
'''
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-08 22:41:54
FilePath: \spider\javbus\spiders\actress_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
from bs4 import BeautifulSoup
from javbus.items import ActressItem
from javbus.utils.log_util import LogUtil
from javbus.utils.page_util import PageUtil
from javbus.utils.request_util import RequestUtil
from javbus.utils.attrs_util import AttrsUtil
from javbus.utils.actress_util import ActressUtil
from javbus.utils.web_util import WebUtil
from scrapy_redis.spiders import RedisSpider

# 女优列表爬虫
class ActressListSpider(RedisSpider):
    name = "actress"
    allowed_domains = ["javbus.com"]

    def __init__(self, url, is_censored, *args, **kwargs):
        super(ActressListSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored

    def start_requests(self):
        """
        Start the first request to fetch the actress listing page.
        """
        yield scrapy.Request(self.base_url, callback=self.parse)

    # 用于解析reponse的方法
    def parse(self, response):
        """
        Parse the actress listing page and fetch next page if available.
        """
        if response.status == 200:
            self.log(f"Now parsing page {self.page_num}")
