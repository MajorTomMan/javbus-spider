import scrapy
import hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from javbus.items import CategoryItem, GenreItem,GenresItem
from scrapy_redis.spiders import RedisSpider
from javbus.utils.attrs_util import AttrsUtil


class GenreSpider(RedisSpider):
    name = "genre"
    allowed_domains = ["javbus.com"]

    def __init__(
        self,
        url="https://www.javbus.com/genre",
        is_censored=True,
    ):
        self.base_url = url
        self.is_censored = is_censored

    def start_requests(self):
        yield scrapy.Request(self.base_url, callback=self.parse)

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
