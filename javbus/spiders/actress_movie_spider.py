
"""
Date: 2025-02-14 20:07:34
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-16 21:06:21
FilePath: \spider\javbus\spiders\actress_movie_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import json
import scrapy
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from javbus.utils.page_util import PageUtil
from javbus.common.redis_keys import movie_start_url_key,movie_censored_link_key,actress_movie_censored_link_key
from base.base_spider import BaseSpider


class ActressMovieSpider(BaseSpider):
    name = "actress_movie"
    allowed_domains = None
    page_num = 1
    censored_key = actress_movie_censored_link_key
    is_first_time = True
    
    def __init__(self, *args, **kwargs):
        # 父类会处理参数初始化
        super().__init__(*args, **kwargs)
        
    def parse(self, response):
        current_page_num = None 
        if self.is_first_time is False:
            current_page_num = response.meta.get("page_num", self.page_num)
        else:
            self.is_first_time = False
        if current_page_num is None:
            current_page_num = self.page_num
        if response.status == 200:
            censored_dict = self.pop_from_redis(self.censored_key)
            if censored_dict is None:
                self.log("censored_dict is None")
                return
            censored = json.loads(censored_dict.decode("utf-8"))
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {current_page_num}")
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
                                "is_censored": censored["is_censored"],
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
                next_page_num = current_page_num + 1
                javbus_base_url = censored["url"] + "/" + str(next_page_num)
                yield scrapy.Request(
                    javbus_base_url, callback=self.parse, meta={"page_num": next_page_num}
                )
            else:
                self.log("No next page, stopping crawl.")

