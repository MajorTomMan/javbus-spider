"""
Date: 2025-02-08 22:42:20
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 19:22:52
FilePath: \spider\javbus\spiders\actress_detail_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import scrapy

from bs4 import BeautifulSoup
from javbus.items import ActressItem
from javbus.utils.actress_util import ActressUtil
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import json
import redis

# 女优详情页爬虫
class ActressDetailSpider(RedisSpider):
    name = "actress_detail"
    allowed_domains = ["javbus.com"]
    censored_key = "actress_detail:censored_link"

    def parse(self, response):
        censored_dict = self.server.lpop(self.censored_key)
        censored = json.loads(censored_dict.decode("utf-8"))
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            actress_detail = ActressUtil().getActressDetails()
            actress_detail.is_censored = censored["is_censored"]
            if actress_detail:
                yield actress_detail
        else:
            self.log("Request failed with status code: {}".format(response.status))
