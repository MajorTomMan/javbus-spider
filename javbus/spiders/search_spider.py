"""
Date: 2025-02-07 22:00:48
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-08 00:00:09
FilePath: \JavBus\spider\javbus\Search.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

import scrapy
from bs4 import BeautifulSoup
from jav_scraper.items import MovieItem  # 假设你有一个 MovieItem 类来存储数据
from utils.LogUtil import LogUtil
from utils.PageUtil import PageUtil
from utils.AttrsUtil import AttrsUtil
from utils.WebUtil import WebUtil
from utils.TimeoutUtil import TimeoutUtil


class SearchSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["seedmm.shop"]

    webUtil = WebUtil()
    pageUtil = None
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()
    timeoutUtil = None

    base_url = ""
    page_num = 1
    tag = ""

    def __init__(self, url, tag, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.page_num = 1
        self.tag = tag
        self.pageUtil = PageUtil(url)
        self.timeoutUtil = TimeoutUtil(self.pageUtil)

    def start_requests(self):
        # 起始请求页面
        url = f"{self.base_url}searchstar/{self.tag}/{self.page_num}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 处理每一页的结果
        if response.status == 200:
            self.logUtil.log(f"now page num is {self.page_num}")
            self.bfs(response)

            # 查找是否有下一页，若有则抓取
            next_page = self.get_next_page(response)
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                self.logUtil.log("final page is reached")
        else:
            self.logUtil.log(f"Request failed with status {response.status}")

    def bfs(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})

        if bricks:
            for brick in bricks:
                is_censored = self.attrsUtil.getIsCensored(brick)
                link = self.attrsUtil.getLink(brick)
                if link:
                    self.logUtil.log(f"now visit website link is {link}")
                    is_final_page = False
                    page_num = 0
                    while not is_final_page:
                        page_num += 1
                        is_final_page = self.pageUtil.parseMovieListPage(
                            link + "/" + str(page_num), is_censored
                        )
        else:
            self.logUtil.log("bricks not found")
            self.pageUtil.save2local(response.text, self.tag, ".html")

    def get_next_page(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        next_button = bs.find("a", {"class": "next"})
        if next_button:
            return self.base_url + next_button.get("href")
        return None

    def log(self, message):
        self.logUtil.log(message)
