from typing import Any
from scrapy.http import Response
from scrapy_redis.spiders import RedisSpider

class ActressMovieSpider(RedisSpider):
    name = "actress_movie"
    allowed_domains = ["javbus.com"]

    def parse(self, response):
        pass