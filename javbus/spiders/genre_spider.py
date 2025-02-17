"""
Date: 2025-02-14 20:07:34
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-16 20:17:45
FilePath: \spider\javbus\spiders\genre_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import scrapy
import hashlib
from bs4 import BeautifulSoup
from javbus.items import CategoryItem, GenreItem, GenresItem
from scrapy_redis.spiders import RedisSpider
from javbus.utils.attrs_util import AttrsUtil
from javbus.common.static import base_url

class GenreSpider(RedisSpider):
    name = "genre"
    allowed_domains = None

    def __init__(self, url=base_url, is_censored=True):
        self.base_url = url
        self.is_censored = AttrsUtil().str_to_bool(is_censored)

    def start_requests(self):
        if self.is_censored:
            url = self.base_url + "genre"
        else:
            url = self.base_url + "uncensored" + "/genre"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            genreList = []
            bs = BeautifulSoup(response.body, "html.parser")
            titles = bs.find_all("h4", {"class": "modal-title"})
            for title in titles:
                # 将所有带有modal-title属性的html元素去掉
                bs.find("h4", {"class": "modal-title"}).extract()
            h4s = bs.find_all("h4")
            if h4s:
                for h4 in h4s:
                    genre = GenreItem()
                    genre["name"] = h4.text.strip()
                    genreList.append(genre)
                boxs = bs.find_all("div", {"class": "row genre-box"})
                if boxs:
                    vos = []
                    for index, box in enumerate(boxs):
                        categories = AttrsUtil().getCategories(box, self.is_censored)
                        genres = GenresItem()
                        genre = genreList[index]
                        genres["genre"] = genre
                        genres["categories"] = categories
                        yield genres
        else:
            self.log("Request failed with status code: {}".format(response.status))
