'''
Date: 2025-02-08 22:42:20
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 11:37:29
FilePath: \JavBus\spider\javbus\spiders\actress_detail_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy

from bs4 import BeautifulSoup
from javbus.items import ActressItem
from javbus.utils.actress_util import ActressUtil
from scrapy_redis.spiders import RedisSpider
# 女优详情页爬虫
class ActressDetailSpider(RedisSpider):
    name = "actress_detail"
    allowed_domains = ["javbus.com"]
    redis_key="actress_detail:links"
    def __init__(self, link, is_censored, *args, **kwargs):
        super(IndexSpider, self).__init__(*args, **kwargs)
        self.link = link
        self.is_censored = is_censored

    def start_requests(self):
        yield scrapy.Request(self.link, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            actressDetail = ActressUtil().getActressDetails()
            if actressDetail:
                yield actressDetail
        else:
            self.log("Request failed with status code: {}".format(response.status))
