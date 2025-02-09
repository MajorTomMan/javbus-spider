'''
Date: 2025-02-08 22:06:25
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 11:31:32
FilePath: \spider\javbus\spiders\movie_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
from javbus.utils.page_util import PageUtil
from javbus.spiders.actress_detail_spider import ActressDetailSpider
from scrapy_redis.spiders import RedisSpider

class MovieSpider(RedisSpider):
    name = "movie"
    allowed_domains = ["javbus.com"]
    redis_key="movie:links"
    def __init__(self, link, is_censored, *args, **kwargs):
        super(IndexSpider, self).__init__(*args, **kwargs)
        self.link = url
        self.is_censored = is_censored
        self.page_num = 1

    def start_requests(self):
        self.log("Now is visiting movie link:" + self.link)
        yield scrapy.Request(self.link, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            page = PageUtil().parseDetailPage(link=link, is_censored=is_censored)
            actresses=page.actresses
            # 启动女优详情页爬虫
            if actresses:
                for actress in actresses:
                    link = actress["link"]
                    if link:
                        self.server.lpush(
                            "actress_detail:links", link
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
