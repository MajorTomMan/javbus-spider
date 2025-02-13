import json
import scrapy
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from javbus.utils.page_util import PageUtil


class ActressMovieSpider(RedisSpider):
    name = "actress_movie"
    allowed_domains = ["javbus.com"]
    page_num = 1
    censored_key = "actress_movie:censored_link"

    def parse(self, response):
        if response.status == 200:
            censored_dict = self.server.lpop(self.censored_key)
            censored = json.loads(censored_dict.decode("utf-8"))
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {self.page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                bricks = bs.find_all("a", attrs={"class": "movie-box"})
                if bricks:
                    for brick in bricks:
                        link = self.get_link(brick)
                        if link:
                            movie_request_data = {"url": link}
                            self.server.lpush(
                                "movie:start_urls", json.dumps(movie_request_data)
                            )
                            movie_request_data = {
                                "url": link,
                                "is_censored": censored["is_censored"],
                            }
                            self.server.lpush(
                                "movie:censored_link", json.dumps(movie_request_data)
                            )

                else:
                    self.log("No bricks found on this page.")
            else:
                self.log("No waterfall found on this page.")
                # 检查是否有下一页并跳转
            next_page = self.get_next_page(bs)
            if next_page:
                self.page_num += 1
                base_url = censored["url"] + "/" + str(self.page_num)
                yield scrapy.Request(base_url, callback=self.parse)
            else:
                self.log("No next page, stopping crawl.")

    def get_next_page(self, bs):
        return PageUtil().hasNextPage(bs)

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None
