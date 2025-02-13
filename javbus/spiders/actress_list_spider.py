"""
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-08 22:41:54
FilePath: \spider\javbus\spiders\actress_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import json
import scrapy
from bs4 import BeautifulSoup
from javbus.utils.page_util import PageUtil
from scrapy_redis.spiders import RedisSpider


# 女优列表爬虫
class ActressListSpider(RedisSpider):
    name = "actresses_list"
    allowed_domains = ["javbus.com"]
    page_num = 1

    def __init__(self, url="https://www.javbus.com/actresses", is_censored=True):
        self.base_url = url
        self.is_censored = is_censored
        if is_censored is False:
            self.base_url = "https://www.javbus.com/uncensored/actresses"

    def start_requests(self):
        url = self.base_url + str(self.page_num)
        yield scrapy.Request(
            self.base_url, callback=self.parse, meta={"page_num": self.page_num}
        )

    # 用于解析reponse的方法
    def parse(self, response):
        page_num = response.meta['page_num'] 
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {self.page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                boxs = bs.find_all("a", attrs={"class": "avatar-box text-center"})
                if boxs:
                    for box in boxs:
                        link = self.get_link(box)
                        if link:
                            actresses_request_data = {"url": link}
                            self.server.lpush(
                                "actress_detail:start_urls",
                                json.dumps(actresses_request_data),
                            )
                            actresses_request_data = {
                                "url": link,
                                "is_censored": self.is_censored,
                            }
                            self.server.lpush(
                                "actress_detail:censored_link",
                                json.dumps(actresses_request_data),
                            )

                else:
                    self.log("No boxs found on this page.")
            else:
                self.log("No waterfall found on this page.")
            # 检查是否有下一页并跳转
            next_page = self.get_next_page(bs)
            if next_page:
                next_page_num = page_num + 1
                base_url = self.base_url + "/" + str(self.page_num)
                yield scrapy.Request(
                    base_url, callback=self.parse, meta={"page_num": next_page_num}
                )
            else:
                self.log("No next page, stopping crawl.")

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None

    def get_next_page(self, bs):
        return PageUtil().hasNextPage(bs)
