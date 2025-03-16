'''
Date: 2025-03-10 21:19:15
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-03-16 18:19:05
FilePath: \spider\javbus\spiders\actress_movie_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''

import json
import re
from bs4 import BeautifulSoup
from javbus.common.redis_keys import (
    movie_start_url_key,
    actress_movie_start_url_key
)
from base.base_spider import BaseSpider

class ActressMovieSpider(BaseSpider):
    name = "actress_movie"
    allowed_domains = None
    page_num = 1
    def parse(self, response):
        current_page_num = response.meta.get("page_num", self.page_num)
        is_censored = response.meta["is_censored"]
        if response.status == 200:
            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {current_page_num}")
            waterfall = bs.find(id="waterfall")
            if waterfall:
                bricks = bs.find_all("a", attrs={"class": "movie-box"})
                if bricks:
                    for brick in bricks:
                        link = self.get_link(brick)
                        if link:
                            movie_request_data = {"url": link,"meta":{
                                "is_censored": is_censored
                            }}
                            self.push_to_redis(
                                movie_start_url_key, json.dumps(movie_request_data)
                            )

                else:
                    self.log("No bricks found on this page.")
            else:
                self.log("No waterfall found on this page.")
            # 检查是否有下一页并跳转
            next_page = self.get_next_page(bs)
            if next_page:
                next_page_num = current_page_num + 1
                next_link = self.get_next_link(response.url, next_page_num)

                self.log(f"Fetching next page: {next_link}")
                next_params = {
                    "url":next_link,
                    "meta":{
                        "page_num": next_page_num, 
                        "is_censored": is_censored
                    }
                }
                self.push_to_redis(actress_movie_start_url_key,json.dumps(next_params))
            else:
                self.log("No next page, waiting for new request.")


    def get_next_link(self,current_url, next_page_num):
        if re.search(r"/\d+$", current_url):  # 检查 URL 是否以数字结尾
            return re.sub(r"/\d+$", f"/{next_page_num}", current_url)
        else:
            return f"{current_url}/{next_page_num}"  # 直接拼接页码
