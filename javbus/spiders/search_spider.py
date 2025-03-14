"""
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-12 19:42:58
FilePath: \spider\javbus\spiders\search_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import json
import copy
import scrapy
from bs4 import BeautifulSoup
from javbus.utils.page_util import PageUtil
from javbus.common.constants import javbus_base_url
from javbus.common.redis_keys import (
    movie_censored_link_key,
    actress_detail_start_url_key,
    actress_detail_censored_link_key,
    movie_start_url_key,
)
from base.base_spider import BaseSpider


class SearchSpider(BaseSpider):
    name = "search"
    allowed_domains = None

    def __init__(self, *args, **kwargs):
        # 父类会处理参数初始化
        super().__init__(*args, **kwargs)

    def start_requests(self):
        page_num = 1
        if self.is_censored is False:
            self.javbus_base_url = self.javbus_base_url + "uncensored/"

        if self.actress:
            url = self.javbus_base_url + "searchstar/" + self.actress
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=copy.deepcopy({"page_num": page_num}),
                dont_filter=True,
            )

        if self.code:
            url = (
                self.javbus_base_url
                + "search/"
                + self.code
                + "&type="
                + ("1" if self.is_censored else "0")
            )
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=copy.deepcopy({"page_num": page_num}),
                dont_filter=True,
            )

        if self.director:
            url = self.javbus_base_url + "search/" + self.director + "&type=2"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=copy.deepcopy({"page_num": page_num}),
                dont_filter=True,
            )

        if self.studio:
            url = self.javbus_base_url + "search/" + self.studio + "&type=3"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=copy.deepcopy({"page_num": page_num}),
                dont_filter=True,
            )

        if self.label:
            url = self.javbus_base_url + "search/" + self.label + "&type=4"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=copy.deepcopy({"page_num": page_num}),
                dont_filter=True,
            )

        if self.series:
            url = self.javbus_base_url + "search/" + self.series + "&type=5"
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=copy.deepcopy({"page_num": page_num}),
                dont_filter=True,
            )

    def parse(self, response):
        page_num = response.meta.get("page_num", 1)

        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {page_num}")
            waterfall = bs.find(id="waterfall")

            if waterfall:
                if self.actress:
                    avatar_boxes = bs.find_all("a", attrs={"class": "avatar-box text-center"})
                    if avatar_boxes:
                        for box in avatar_boxes:
                            link = self.get_link(box)
                            if link:
                                actress_detail_request_data = {"url": link}
                                self.push_to_redis(actress_detail_start_url_key, json.dumps(actress_detail_request_data))

                                actress_detail_request_data = {"url": link, "is_censored": self.is_censored}
                                self.push_to_redis(actress_detail_censored_link_key, json.dumps(actress_detail_request_data))
                else:
                    bricks = bs.find_all("a", attrs={"class": "movie-box"})
                    if bricks:
                        for brick in bricks:
                            link = self.get_link(brick)
                            if link:
                                movie_request_data = {"url": link}
                                self.push_to_redis(movie_start_url_key, json.dumps(movie_request_data))

                                movie_request_data = {"url": link, "is_censored": self.is_censored}
                                self.push_to_redis(movie_censored_link_key, json.dumps(movie_request_data))
                    else:
                        self.log("No bricks found on this page.")
            else:
                self.log("No waterfall found on this page.")

            # 处理下一页逻辑
            next_page = self.get_next_page(bs)
            if next_page:
                next_page_num = page_num + 1
                next_url = self.get_next_url(str(next_page_num))
                yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                    meta=copy.deepcopy({"page_num": next_page_num}),
                    dont_filter=True,
                )
            else:
                self.log("Final page reached.")
                self.crawler.engine.close_spider(self, "No next page")
                return

        elif response.status == 404:
            self.log("Key Word Not Exist")
        else:
            self.log(f"Request failed with status {response.status}")

    def get_next_url(self, page_num):
        url = ""
        if self.actress:
            url = self.javbus_base_url + "searchstar/" + self.actress + "/" + page_num
        elif self.code:
            url = (
                self.javbus_base_url
                + "search/"
                + self.code
                + "/"
                + page_num
                + "&type=1"
            )
        elif self.director:
            url = (
                self.javbus_base_url
                + "search/"
                + self.director
                + "/"
                + page_num
                + "&type=2"
            )
        elif self.studio:
            url = (
                self.javbus_base_url
                + "search/"
                + self.studio
                + "/"
                + page_num
                + "&type=3"
            )
        elif self.label:
            url = (
                self.javbus_base_url
                + "search/"
                + self.label
                + "/"
                + page_num
                + "&type=4"
            )
        elif self.series:
            url = (
                self.javbus_base_url
                + "search/"
                + self.series
                + "/"
                + page_num
                + "&type=5"
            )
        return url
