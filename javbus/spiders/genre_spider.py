"""
Date: 2025-02-14 20:07:34
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-16 20:17:45
FilePath: \spider\javbus\spiders\genre_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import scrapy
from bs4 import BeautifulSoup
from javbus.items import  GenreItem, GenreCategoryItem
from scrapy_redis.spiders import RedisSpider
from javbus.utils.attrs_util import AttrsUtil
from javbus.common.constants import javbus_base_url

class GenreSpider(RedisSpider):
    name = "genre"
    allowed_domains = None

    def __init__(self, url=javbus_base_url, is_censored=True):
        self.javbus_base_url = url
        self.is_censored = AttrsUtil().str_to_bool(is_censored)

    def start_requests(self):
        if self.is_censored:
            url = self.javbus_base_url + "genre"
        else:
            url = self.javbus_base_url + "uncensored" + "/genre"
        yield scrapy.Request(url, callback=self.parse,meta={"is_censored":self.is_censored},dont_filter=True)

    def parse(self, response):
        is_censored = response.meta.get("is_censored",self.is_censored)
        if is_censored is None:
            is_censored = self.is_censored
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
                    for index, box in enumerate(boxs):
                        categories = AttrsUtil().get_categories(box)
                        genres = GenreCategoryItem()
                        genre = genreList[index]
                        genres["genre"] = genre
                        genres["categories"] = categories
                        genres["is_censored"] =is_censored
                        yield genres
            self.log("No next page, stopping crawl.")
            self.crawler.engine.close_spider(self, "No next page")
        else:
            self.log("Request failed with status code: {}".format(response.status))
            
            
    @signals.spider_error.connect
    def on_spider_error(self, failure, spider):
        # 触发爬虫停止，记录错误信息
        self.log(f"Spider error occurred: {failure}", level="ERROR")
        raise CloseSpider("An error occurred, stopping spider.")
