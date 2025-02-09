"""
Date: 2025-02-08 22:06:25
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 19:20:11
FilePath: \spider\javbus\spiders\movie_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import scrapy
from javbus.utils.page_util import PageUtil
from javbus.spiders.actress_detail_spider import ActressDetailSpider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import json


class MovieSpider(RedisSpider):
    name = "movie"
    allowed_domains = ["javbus.com"]
    is_censored = True
    censored_key = "movie:censored_link"


    
    def parse(self, response):
        self.log("parse")
        censored_dict = self.server.lpop(censored_key)
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            page = PageUtil().parseDetailPage(
                link=link, is_censored=self.str_to_bool(censored_dict["is_censored"])
            )
            actresses = page.actresses
            # 启动女优详情页爬虫
            if actresses:
                for actress in actresses:
                    link = actress["link"]
                    if link:
                        actress_detail_request_data = {
                            "url": link,
                            "is_censored": self.str_to_bool(
                                censored_dict["is_censored"]
                            ),
                        }
                        self.server.rpush("actress_detail:start_urls", link)
            else:
                self.log("get actresses failed")
            yield page
        else:
            self.log("Request failed with status code: {}".format(response.status))

    def log(self, message):
        """
        Log the message for debugging purposes.
        """
        self.logger.info(message)

    def str_to_bool(self, value: str) -> bool:
        if value.lower() in ["true", "1", "t", "y", "yes"]:
            return True
        elif value.lower() in ["false", "0", "f", "n", "no"]:
            return False
        else:
            raise ValueError(f"Cannot convert '{value}' to a boolean")
