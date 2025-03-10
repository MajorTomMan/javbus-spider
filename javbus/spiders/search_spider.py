"""
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-12 19:42:58
FilePath: \spider\javbus\spiders\search_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import json
import scrapy
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from javbus.utils.page_util import PageUtil
from javbus.common.constants import javbus_base_url
from javbus.common.redis_keys import movie_censored_link_key,actress_detail_start_url_key,actress_detail_censored_link_key,movie_start_url_key

class SearchSpider(RedisSpider):
    name = "search"
    allowed_domains = None
    search_type = 1

    def __init__(
        self,
        url=javbus_base_url,
        actress="北野未奈",
        code="",
        director="",
        studio="",
        label="",
        series="",
        is_censored=False,
    ):
        self.javbus_base_url = url
        self.page_num = 1
        self.actress = actress
        self.code = code
        self.director = director
        self.studio = studio
        self.label = label
        self.series = series
        self.is_censored = is_censored

    def start_requests(self):
        """
        Starts the requests by fetching the first page.
        """
        if self.is_censored is False:
            self.javbus_base_url = self.javbus_base_url + "uncensored/"
        url = ""
        if self.actress:
            url = self.javbus_base_url + "searchstar/" + self.actress
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"page_num": self.page_num},
            )

        # Code search
        if self.code:
            if self.is_censored:
                url = self.javbus_base_url + "search/" + self.code + "&type=1"
            else:
                url = self.javbus_base_url + "search/" + self.code + "&type=0"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"page_num": self.page_num},
            )

        # Director search
        if self.director:
            url = self.javbus_base_url + "search/" + self.director + "&type=2"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"page_num": self.page_num},
            )

        # Studio search
        if self.studio:
            url = self.javbus_base_url + "search/" + self.studio + "&type=3"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"page_num": self.page_num},
            )

        # Label search
        if self.label:
            url = self.javbus_base_url + "search/" + self.label + "&type=4"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"page_num": self.page_num},
            )

        # Series search
        if self.series:
            url = self.javbus_base_url + "search/" + self.series + "&type=5"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"page_num": self.page_num},
            )

    def parse(self, response):
        page_num = response.meta.get("page_num", self.page_num)
        if page_num is None:
            page_num = self.page_num
        if response.status == 200:

            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                if self.actress:
                    avatar_boxs = bs.find_all(
                        "a", attrs={"class": "avatar-box text-center"}
                    )
                    if avatar_boxs:
                        for box in avatar_boxs:
                            link = self.get_link(box)
                            actress_detail_request_data = {
                                "url": link,
                            }
                            self.server.lpush(
                                actress_detail_start_url_key,
                                json.dumps(actress_detail_request_data),
                            )
                            actress_detail_request_data = {
                                "url": link,
                                "is_censored": self.is_censored,
                            }
                            self.server.lpush(
                                actress_detail_censored_link_key,
                                json.dumps(actress_detail_request_data),
                            )
                else:
                    bricks = bs.find_all("a", attrs={"class": "movie-box"})
                    if bricks:
                        for brick in bricks:
                            link = self.get_link(brick)
                            if link:
                                movie_request_data = {"url": link}
                                self.server.lpush(
                                    movie_start_url_key, json.dumps(movie_request_data)
                                )
                                movie_request_data = {
                                    "url": link,
                                    "is_censored": self.is_censored,
                                }
                                self.server.lpush(
                                    movie_censored_link_key,
                                    json.dumps(movie_request_data),
                                )

                    else:
                        self.log("No bricks found on this page.")
            else:
                self.log("No waterfall found on this page.")
            # 查找是否有下一页，若有则抓取
            next_page = self.get_next_page(bs)
            if next_page:
                next_page_num = page_num + 1
                next_url = self.get_next_url(str(next_page_num))
                yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                    meta={"page_num": self.page_num},
                )
            else:
                self.log("Final page reached.")
                self.crawler.engine.close_spider(self, "No next page")
                return
        elif response.status == 404:
            self.log(f"Key Word Not Exist")
        else:
            self.log(f"Request failed with status {response.status}")

    def get_next_url(self, page_num):
        url = ""
        if self.actress:
            url = self.javbus_base_url + "searchstar/" + self.actress + "/" + page_num
        # Code search
        if self.code:
            url = self.javbus_base_url + "search/" + self.code + "/" + page_num + "&type=1"
        # Director search
        if self.director:
            url = self.javbus_base_url + "search/" + self.director + "/" + page_num + "&type=2"
        # Studio search
        if self.studio:
            url = self.javbus_base_url + "search/" + self.studio + "/" + page_num + "&type=3"
        # Label search
        if self.label:
            url = self.javbus_base_url + "search/" + self.label + "/" + page_num + "&type=4"
        # Series search
        if self.series:
            url = self.javbus_base_url + "search/" + self.series + "/" + page_num + "&type=5"
        return url

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None

    def get_next_page(self, bs):
        return PageUtil().has_next_page(bs)

    def log(self, message):
        """
        Log the messages using the utility.
        """
        self.logger.info(message)

    @signals.spider_error.connect
    def on_spider_error(self, failure, spider):
        # 触发爬虫停止，记录错误信息
        self.log(f"Spider error occurred: {failure}", level="ERROR")
        raise CloseSpider("An error occurred, stopping spider.")
