

"""
Date: 2025-02-13 19:14:01
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-13 23:14:50
FilePath: \spider\javbus\spiders\movie_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import json
from javbus.utils.page_util import PageUtil
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from javbus.common.redis_keys import movie_censored_link_key,actress_detail_start_url_key,actress_detail_censored_link_key

class MovieSpider(RedisSpider):
    name = "movie"
    allowed_domains = None
    is_censored = True
    censored_key = movie_censored_link_key

    def parse(self, response):
        censored_dict = self.server.lpop(self.censored_key)
        if censored_dict is None:
            self.log("censored_dict is None")
            return
        censored = json.loads(censored_dict.decode("utf-8"))
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            page = PageUtil().parse_page(
                link=response.url, source=bs, is_censored=censored["is_censored"]
            )
            if page == -1 or page is None:
                self.log("in " + censored["url"] + " found ban tag skipping crawl")
                return
            actresses = page["actresses"]
            # 启动女优详情页爬虫
            if actresses:
                for actress in actresses:
                    actress["is_censored"] = censored["is_censored"]
                    link = actress["actress_link"]
                    if link:
                        actress_detail_request_data = {
                            "url": link,
                        }
                        self.server.lpush(
                            actress_detail_start_url_key,
                            json.dumps(actress_detail_request_data),
                        )
                        actress_detail_request_data = {
                            "url": link,
                            "is_censored": censored["is_censored"],
                        }
                        self.server.lpush(
                            actress_detail_censored_link_key,
                            json.dumps(actress_detail_request_data),
                        )
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

    @signals.spider_error.connect
    def on_spider_error(self, failure, spider):
        # 触发爬虫停止，记录错误信息
        self.log(f"Spider error occurred: {failure}", level="ERROR")
        raise CloseSpider("An error occurred, stopping spider.")
