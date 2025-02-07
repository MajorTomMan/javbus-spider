'''
Date: 2025-02-07 23:57:11
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-07 23:57:21
FilePath: \JavBus\spider\javbus\spiders\index_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
import random
from collections import OrderedDict
from bs4 import BeautifulSoup
from jav_scraper.items import MovieItem

visited = OrderedDict()


class IndexSpider(scrapy.Spider):
    name = "index"
    allowed_domains = ["seedmm.shop"]

    def __init__(self, url, is_censored, *args, **kwargs):
        super(IndexSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored
        self.page_num = 1
        self.visited = visited

    def start_requests(self):
        if self.is_censored:
            url = self.base_url + f"page/{self.page_num}"
        else:
            url = self.base_url + f"uncensored/page/{self.page_num}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            self.log(f"now page num is {self.page_num}")
            self.bfs(bs)

            next_page = self.get_next_page(bs)
            if next_page:
                next_url = self.base_url + next_page
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                self.log("No next page, stopping crawl")
        else:
            self.log("Request failed")

    def bfs(self, bs):
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.get_link(brick)
                if link:
                    visited[link] = False
                    self.follow_link(link)

    def follow_link(self, link):
        if not visited[link]:
            visited[link] = True
            yield scrapy.Request(link, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        movie_item = self.parse_movie_details(bs)
        if movie_item:
            yield movie_item

    def parse_movie_details(self, bs):
        # 提取电影详细信息（这是一个示例，你需要根据实际页面修改）
        movie_item = MovieItem()
        movie_item["title"] = bs.find("h1", {"class": "movie-title"}).get_text()
        return movie_item

    def get_link(self, brick):
        link = brick.find("a", href=True)
        return link["href"] if link else None

    def get_next_page(self, bs):
        next_button = bs.find("a", {"class": "next"})
        if next_button:
            return next_button.get("href")
        return None
