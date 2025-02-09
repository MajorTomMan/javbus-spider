from scrapy_redis.spiders import RedisSpider

class ActressMovieSpider(RedisSpider):
    name = "actress_movie"
    allowed_domains = ["javbus.com"]

    pass