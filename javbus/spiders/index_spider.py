"""
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 18:04:20
FilePath: \spider\javbus\spiders\index_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import scrapy
import json
from javbus.spiders.movie_spider import MovieSpider
from bs4 import BeautifulSoup
from javbus.utils.page_util import PageUtil
from scrapy_redis.spiders import RedisSpider


class IndexSpider(RedisSpider):
    name = "index"
    allowed_domains = ["javbus.com"]

    def __init__(self, url="https://www.javbus.com/page/", is_censored=True):
        self.base_url = url
        self.is_censored = is_censored
        self.page_num = 1

    def start_requests(self):
        base_url = self.base_url + str(self.page_num)
        yield scrapy.Request(base_url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {self.page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                bricks = bs.find_all("a", attrs={"class": "movie-box"})
                if bricks:
                    for brick in bricks:
                        link = self.get_link(brick)
                        if link:
                            movie_request_data = {"url": link}
                            self.server.lpush(
                                "movie:start_urls", json.dumps(movie_request_data)
                            )
                            movie_request_data = {
                                "url": link,
                                "is_censored": self.is_censored,
                            }
                            self.server.lpush(
                                "movie:censored_link", json.dumps(movie_request_data)
                            )

                else:
                    self.log("No bricks found on this page.")
            else:
                self.log("No waterfall found on this page.")
            # 检查是否有下一页并跳转
            next_page = self.get_next_page(bs)
            if next_page:
                self.page_num += 1
                base_url = self.base_url + str(self.page_num)
                yield scrapy.Request(base_url, callback=self.parse)
            else:
                self.log("No next page, stopping crawl.")
        else:
            self.log("Request failed with status code: {}".format(response.status))

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None

    def get_next_page(self, bs):
        return PageUtil().hasNextPage(bs)

    def log(self, message):
        """
        Log the message for debugging purposes.
        """
        self.logger.info(message)
