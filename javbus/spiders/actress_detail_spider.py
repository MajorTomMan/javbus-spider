"""
Date: 2025-02-08 22:42:20
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 19:22:52
FilePath: \spider\javbus\spiders\actress_detail_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""


from bs4 import BeautifulSoup
from javbus.items import ActressesItem
from javbus.utils.actress_util import ActressUtil
from javbus.common.redis_keys import (
    actress_movie_start_url_key,
)

import json

from base.base_spider import BaseSpider


# 女优详情页爬虫
class ActressDetailSpider(BaseSpider):
    name = "actress_detail"
    allowed_domains = None
    
        
    def parse(self, response):
        if response.status == 200:
            link = response.url
            is_censored = response.meta["is_censored"]
            bs = BeautifulSoup(response.body, "html.parser")
            actress_detail = ActressUtil().get_details(bs)
            actress_detail["is_censored"] = is_censored
            actress_detail["actress_link"] = link
            if actress_detail:
                actresses = ActressesItem()
                actresses["actresses"] = [actress_detail]
                yield actresses
            # 爬取女优详情页的电影
            actresses_movie_request_data = {"url": link,"meta":{
                "is_censored": is_censored
            }}
            self.push_to_redis(
                actress_movie_start_url_key, json.dumps(actresses_movie_request_data)
            )
        else:
            self.log("Request failed with status code: {}".format(response.status))

