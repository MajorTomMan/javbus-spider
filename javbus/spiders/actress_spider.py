import scrapy
from bs4 import BeautifulSoup
from jav_scraper.items import ActressItem
from utils.LogUtil import LogUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil
from utils.AttrsUtil import AttrsUtil
from utils.ActressUtil import ActressUtil
from utils.WebUtil import WebUtil


class ActressSpider(scrapy.Spider):
    name = "actress"
    allowed_domains = ["seedmm.shop"]

    webUtil = WebUtil()
    actressUtil = ActressUtil()
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()
    requestUtil = RequestUtil()

    base_url = ""
    page_num = 1
    is_censored = True

    def __init__(self, url, is_censored, *args, **kwargs):
        super(ActressSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored
        self.page_num = 1

    def start_requests(self):
        if self.is_censored:
            url = f"{self.base_url}actresses/{self.page_num}"
        else:
            url = f"{self.base_url}uncensored/actresses/{self.page_num}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
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
            actress_list = []
            for brick in bricks:
                actress_dict = self.attrsUtil.getSingleActressLink(brick)
                if actress_dict:
                    actress = self.actressUtil.getActressDetails(
                        actress_dict["actress_link"]
                    )
                    if actress:
                        if not self.actressUtil.matchLinkIsCompanyLink(
                            actress_dict["photo_link"]
                        ):
                            if self.base_url.endswith("/"):
                                url = self.base_url[:-1]
                                actress.photo_link = url + actress.photo_link
                        actress.actress_link = actress_dict["actress_link"]
                        actress.is_censored = self.is_censored
                        actress_list.append(actress.toDict())

            # 保存收集的数据
            if actress_list:
                self.requestUtil.send(actress_list, "/actress/save")
        else:
            self.logUtil.log("bricks not found on this page.")
            self.pageUtil.save2local(response.text, "actress", ".html")

    def get_next_page(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        next_button = bs.find("a", {"class": "next"})
        if next_button:
            return self.base_url + next_button.get("href")
        return None

    def log(self, message):
        self.logUtil.log(message)
