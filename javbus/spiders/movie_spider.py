

import json
from javbus.utils.page_util import PageUtil
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup


class MovieSpider(RedisSpider):
    name = "movie"
    allowed_domains = ["javbus.com"]
    is_censored = True
    censored_key = "movie:censored_link"

    def parse(self, response):
        censored_dict = self.server.lpop(self.censored_key)
        censored = json.loads(censored_dict.decode("utf-8"))
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            page = PageUtil().parsePage(
                link=response.url, source=bs, is_censored=censored["is_censored"]
            )
            if page== -1:
                self.log("in "+censored["url"]+" found ban tag skipping crawl")
                return
            actresses = page["actresses"]
            # 启动女优详情页爬虫
            if actresses:
                for actress in actresses:
                    link = actress["link"]
                    if link:
                        actress_detail_request_data = {
                            "url": link,
                        }
                        self.server.lpush(
                            "actress_detail:start_urls", actress_detail_request_data
                        )
                        actress_detail_request_data = {
                            "url": link,
                            "is_censored": censored["is_censored"],
                        }
                        self.server.lpush(
                            "actress_detail:censored", actress_detail_request_data
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
