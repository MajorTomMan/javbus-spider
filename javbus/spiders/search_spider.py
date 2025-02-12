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


class SearchSpider(RedisSpider):
    name = "search"
    allowed_domains = ["javbus.com"]
    search_type = 1

    def __init__(
        self,
        url="https://www.javbus.com/",
        actress="",
        code="",
        director="麒麟",
        studio="",
        label="",
        series="",
        is_censored=True,
    ):
        self.base_url = url
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
            self.base_url = self.base_url + "uncensored/"
        url = ""
        if self.actress:
            url = self.base_url + "searchstar/" + self.actress
            yield scrapy.Request(url, callback=self.parse)

        # Code search
        if self.code:
            url = self.base_url + "search/" + self.code + "&type=1"
            yield scrapy.Request(url, callback=self.parse)

        # Director search
        if self.director:
            url = self.base_url + "search/" + self.director + "&type=2"
            yield scrapy.Request(url, callback=self.parse)

        # Studio search
        if self.studio:
            url = self.base_url + "search/" + self.studio + "&type=3"
            yield scrapy.Request(url, callback=self.parse)

        # Label search
        if self.label:
            url = self.base_url + "search/" + self.label + "&type=4"
            yield scrapy.Request(url, callback=self.parse)

        # Series search
        if self.series:
            url = self.base_url + "search/" + self.series + "&type=5"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response for each page and check if there is a next page.
        """
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
            # 查找是否有下一页，若有则抓取
            next_page = self.get_next_page(response)
            if next_page:
                self.page_num += 1
                next_url = self.get_next_url(str(self.page_num))
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                self.log("Final page reached.")
        elif response.status == 404:
            self.log(f"Key Word Not Exist")
        else:
            self.log(f"Request failed with status {response.status}")

    def get_next_url(self, page_num):
        url = ""
        if self.actress:
            url = self.base_url + "searchstar/" + self.actress + "/" + page_num
        # Code search
        if self.code:
            url = self.base_url + "search/" + self.code + "/" + page_num + "&type=1"
        # Director search
        if self.director:
            url = self.base_url + "search/" + self.director + "/" + page_num + "&type=2"
        # Studio search
        if self.studio:
            url = self.base_url + "search/" + self.studio + "/" + page_num + "&type=3"
        # Label search
        if self.label:
            url = self.base_url + "search/" + self.label + "/" + page_num + "&type=4"
        # Series search
        if self.series:
            url = self.base_url + "search/" + self.series + "/" + page_num + "&type=5"
        return url

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None

    def get_next_page(self, response):
        return PageUtil().hasNextPage(bs)

    def log(self, message):
        """
        Log the messages using the utility.
        """
        self.logger.info(message)
