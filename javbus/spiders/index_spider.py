'''
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 11:31:55
FilePath: \spider\javbus\spiders\index_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy

from javbus.spiders.movie_spider import MovieSpider
from bs4 import BeautifulSoup
from javbus.items import MovieItem
from javbus.utils.page_util import PageUtil
from scrapy_redis.spiders import RedisSpider

class IndexSpider(RedisSpider):
    name = "index"
    allowed_domains = ["javbus.com"]
    redis_key="index:links"
    def __init__(
        self, url="https://www.javbus.com/page/", is_censored=True, *args, **kwargs
    ):
        super(IndexSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored
        self.page_num = 1

    def start_requests(self):
        base_url = self.base_url + str(self.page_num)
        yield scrapy.Request(base_url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {self.page_num}")
            bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
            if bricks:
                for brick in bricks:
                    link = self.get_link(brick)
                    if link:
                        self.server.lpush("movie:links", link)  # 推送到 `movie` 队列
            else:
                self.log("No bricks found on this page.")

            # 检查是否有下一页并跳转
            next_page = self.get_next_page(bs)
            if next_page:
                self.page_num += 1
                base_url = self.base_url + str(self.page_num)
                yield scrapy.Request(base_url, callback=self.parse)
            else:
                self.log("No next page, stopping crawl.")
        else:
            self.log("Request failed with status code: {}".format(response.status))

    def get_link(self, brick):
        link = brick.find("a", href=True)
        return link["href"] if link else None

    def get_next_page(self, bs):
        return PageUtil().hasNextPage(bs)

    def log(self, message):
        """
        Log the message for debugging purposes.
        """
        self.logger.info(message)
