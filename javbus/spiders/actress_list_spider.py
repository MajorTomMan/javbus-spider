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
from javbus.utils.attrs_util import AttrsUtil
from javbus.common.constants import javbus_base_url
from javbus.common.redis_keys import actress_detail_start_url_key,actress_detail_censored_link_key
from base.base_spider import BaseSpider

# 女优列表爬虫
class ActressListSpider(BaseSpider):
    name = "actresses_list"
    allowed_domains = None
    page_num = 1

    def __init__(self, url=javbus_base_url, is_censored=False):
        self.javbus_base_url = url
        self.is_censored = AttrsUtil().str_to_bool(is_censored)

    def start_requests(self):
        if self.is_censored is False:
            url = self.javbus_base_url + "uncensored" + "/actresses/"
        else:
            url = self.javbus_base_url + "actresses/"
        url = url + str(self.page_num)
        yield scrapy.Request(url, callback=self.parse, meta={"page_num": self.page_num,"is_censored":self.is_censored},dont_filter=True)

    # 用于解析reponse的方法
    def parse(self, response):
        page_num = response.meta.get("page_num", self.page_num)
        is_censored = response.meta.get("is_censored", self.is_censored)
        # 判断是否为 None，并记录日志
        if is_censored is None:
            self.logger.info("is_censored 为 None, 使用默认值: %s", self.is_censored)
            is_censored = self.is_censored
        if page_num is None:
            self.logger.info("page_num 为 None, 使用默认值: %s", self.page_num)
            page_num = self.page_num
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                boxs = bs.find_all("a", attrs={"class": "avatar-box text-center"})
                if boxs:
                    for box in boxs:
                        link = self.get_link(box)
                        if link:
                            actresses_request_data = {"url": link}
                            self.server.lpush(
                                actress_detail_start_url_key,
                                json.dumps(actresses_request_data),
                            )
                            actresses_request_data = {
                                "url": link,
                                "is_censored": is_censored,
                            }
                            self.server.lpush(
                                actress_detail_censored_link_key,
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
                if is_censored is False:
                    url = self.javbus_base_url + "uncensored" + "/actresses/"
                else:
                    url = self.javbus_base_url + "actresses/"
                url = url + str(next_page_num)
                yield scrapy.Request(
                    url, callback=self.parse, meta={"page_num": self.page_num,"is_censored":is_censored}
                )
            else:
                self.log("No next page, stopping crawl.")
                self.crawler.engine.close_spider(self, "No next page")
        else:
            