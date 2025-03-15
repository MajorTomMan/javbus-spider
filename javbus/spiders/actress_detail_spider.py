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
    actress_detail_censored_link_key,
    actress_movie_censored_link_key,
    actress_movie_start_url_key,
)

import json

from base.base_spider import BaseSpider


# 女优详情页爬虫
class ActressDetailSpider(BaseSpider):
    name = "actress_detail"
    allowed_domains = None
    censored_key = actress_detail_censored_link_key
    
        
    def parse(self, response):
        censored_dict = self.pop_from_redis(self.censored_key)
        if censored_dict is None:
            self.log("censored_dict is None")
            return
        censored = json.loads(censored_dict.decode("utf-8"))
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            actress_detail = ActressUtil().get_details(bs)
            actress_detail["is_censored"] = censored["is_censored"]
            actress_detail["actress_link"] = censored["url"]
            if actress_detail:
                actresses = ActressesItem()
                actresses["actresses"] = [actress_detail]
                yield actresses
            # 爬取女优详情页的电影
            movie_request_data = {"url": censored["url"]}
            self.push_to_redis(
                actress_movie_start_url_key, json.dumps(movie_request_data)
            )
            movie_request_data = {
                "url": censored["url"],
                "is_censored": censored["is_censored"],
            }
            self.push_to_redis(
                actress_movie_censored_link_key, json.dumps(movie_request_data)
            )
        else:
            self.log("Request failed with status code: {}".format(response.status))

