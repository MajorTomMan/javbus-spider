"""
Date: 2025-02-13 19:14:01
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-15 20:33:54
FilePath: \spider\javbus\spiders\index_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import threading
import scrapy
import json
from bs4 import BeautifulSoup
from javbus.utils.page_util import PageUtil
from scrapy_redis.spiders import RedisSpider
from javbus.utils.attrs_util import AttrsUtil
from javbus.common.constants import javbus_base_url
from javbus.common.redis_keys import (
    movie_start_url_key,
    javbus_backup_links,
    movie_censored_link_key,
)
from base.base_spider import BaseSpider


class IndexSpider(BaseSpider):
    name = "index"
    allowed_domains = None
    # 定义 thread_local 为类变量
    thread_local = threading.local()
    def __init__(self, url=javbus_base_url, is_censored=True):
        self.javbus_base_url = url
        self.is_censored = AttrsUtil().str_to_bool(is_censored)
        # 设置线程局部存储
        IndexSpider.thread_local.is_censored = AttrsUtil().str_to_bool(is_censored)
        IndexSpider.thread_local.page_num = 1
    def start_requests(self):
        # 从线程局部存储获取 is_censored
        is_censored = getattr(IndexSpider.thread_local, 'is_censored', False)
        page_num = getattr(IndexSpider.thread_local, 'page_num', 1)
        if is_censored is False:
            javbus_base_url = (
                self.javbus_base_url + "uncensored/" + "page/" + str(page_num)
            )
        else:
            javbus_base_url = self.javbus_base_url + "page/" + str(page_num)
        yield scrapy.Request(
            javbus_base_url,
            callback=self.parse,
            meta={"page_num": page_num, "is_censored": is_censored},
            dont_filter=True,
        )

    def parse(self, response):
        page_num = response.meta["page_num"]
        is_censored = response.meta["is_censored"]
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            links = PageUtil().get_backup_links(bs)
            if links:
                for link in links:
                    back_link = {"url": link}
                    self.push_to_redis(javbus_backup_links, json.dumps(back_link))
            self.log(f"Now parsing page {page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                bricks = bs.find_all("a", attrs={"class": "movie-box"})
                if bricks:
                    for brick in bricks:
                        link = self.get_link(brick)
                        if link:
                            movie_request_data = {"url": link}
                            self.push_to_redis(
                                movie_start_url_key, json.dumps(movie_request_data)
                            )
                            movie_request_data = {
                                "url": link,
                                "is_censored": is_censored,
                            }
                            self.push_to_redis(
                                movie_censored_link_key, json.dumps(movie_request_data)
                            )

                else:
                    self.log("No bricks found on this page.")
            else:
                self.log("No waterfall found on this page.")
            # 检查是否有下一页并跳转
            next_page = self.get_next_page(bs)
            if next_page:
                next_page_num = page_num + 1
                if is_censored is False:
                    javbus_base_url = (
                        self.javbus_base_url
                        + "uncensored/"
                        + "page/"
                        + str(next_page_num)
                    )
                else:
                    javbus_base_url = (
                        self.javbus_base_url + "page/" + str(next_page_num)
                    )
                yield scrapy.Request(
                    javbus_base_url,
                    callback=self.parse,
                    meta={"page_num": next_page_num, "is_censored": is_censored},
                    dont_filter=True,
                )
            else:
                self.log("No next page, stopping crawl.")
                self.crawler.engine.close_spider(self, "No next page")
        else:
            self.log("Request failed with status code: {}".format(response.status))
