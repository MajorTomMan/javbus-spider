'''
Date: 2025-03-10 21:19:15
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-03-14 20:25:48
FilePath: \spiders\spider\javbus\spiders\actress_list_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''


import json
import threading
import scrapy
import copy
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
        
    def start_requests(self):
    
        page_num = 1
        if self.is_censored is False:
            url = self.javbus_base_url + "uncensored" + "/actresses/"
        else:
            url = self.javbus_base_url + "actresses/"
        url = url + str(page_num)
        
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta=copy.deepcopy({"page_num": page_num, "is_censored": self.is_censored}),
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
                    meta=copy.deepcopy({"page_num": next_page_num, "is_censored": self.is_censored}),
                    dont_filter=True,
                )
            else:
                self.log("No next page, stopping crawl.")
                self.crawler.engine.close_spider(self, "No next page")
