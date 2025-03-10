"""
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-08 22:41:54
FilePath: \spider\javbus\spiders\actress_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import json
import threading
import scrapy
from bs4 import BeautifulSoup
from javbus.utils.attrs_util import AttrsUtil
from javbus.common.constants import javbus_base_url
from javbus.common.redis_keys import (
    actress_detail_start_url_key,
    actress_detail_censored_link_key,
)
from base.base_spider import BaseSpider


# 女优列表爬虫
class ActressListSpider(BaseSpider):
    name = "actresses_list"
    allowed_domains = None
    # 定义 thread_local 为类变量
    thread_local = threading.local()
    def __init__(self, url=javbus_base_url, is_censored=False):
        self.javbus_base_url = url
        self.is_censored = AttrsUtil().str_to_bool(is_censored)
        # 设置线程局部存储
        ActressListSpider.thread_local.is_censored = AttrsUtil().str_to_bool(is_censored)
        ActressListSpider.thread_local.page_num = 1
        
    def start_requests(self):
        # 从线程局部存储获取 is_censored
        is_censored = getattr(ActressListSpider.thread_local, 'is_censored', False)
        page_num = getattr(ActressListSpider.thread_local, 'page_num', 1)
        if is_censored is False:
            url = self.javbus_base_url + "uncensored" + "/actresses/"
        else:
            url = self.javbus_base_url + "actresses/"
        url = url + str(page_num)
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={"page_num": page_num, "is_censored": is_censored},
            dont_filter=True,
        )

    # 用于解析reponse的方法
    def parse(self, response):
        page_num = response.meta["page_num"]
        is_censored = response.meta["is_censored"]
        self.log(f"page_num:{page_num} is_censored:{is_censored}")
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
                            self.push_to_redis(
                                actress_detail_start_url_key,
                                json.dumps(actresses_request_data),
                            )
                            actresses_request_data = {
                                "url": link,
                                "is_censored": is_censored,
                            }
                            self.push_to_redis(
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
                    url,
                    callback=self.parse,
                    meta={"page_num": next_page_num, "is_censored": is_censored},
                    dont_filter=True,
                )
            else:
                self.log("No next page, stopping crawl.")
                self.crawler.engine.close_spider(self, "No next page")
