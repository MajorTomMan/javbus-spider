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

    def make_request_from_data(self, data):
        data_dict = json.loads(data)
        self.is_censored = self.str_to_bool(data_dict["is_censored"])
        return Request(
            url=data_dict["url"],
            callback=self.parse,
        )

    def parse(self, response):
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            actressDetail = ActressUtil().getActressDetails()
            actressDetail.is_censored = self.is_censored
            if actressDetail:
                yield actressDetail
        else:
            self.log("Request failed with status code: {}".format(response.status))

    def str_to_bool(self,value: str) -> bool:
        if value.lower() in ["true", "1", "t", "y", "yes"]:
            return True
        elif value.lower() in ["false", "0", "f", "n", "no"]:
            return False
        else:
            raise ValueError(f"Cannot convert '{value}' to a boolean")
