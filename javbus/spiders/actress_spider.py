import scrapy
from bs4 import BeautifulSoup
from items import ActressItem
from utils.log_util import LogUtil
from utils.page_util import PageUtil
from utils.request_util import RequestUtil
from utils.attrs_util import AttrsUtil
from utils.actress_util import ActressUtil
from utils.web_util import WebUtil

# 女友爬虫

class ActressSpider(scrapy.Spider):
    name = "actress"
    allowed_domains = ["javbus.com"]
    webUtil = WebUtil()
    actressUtil = ActressUtil()
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()
    requestUtil = RequestUtil()
    base_url = ""
    is_censored = True

    def __init__(self, url, is_censored, *args, **kwargs):
        super(ActressSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored

    def start_requests(self):
        """
        Start the first request to fetch the actress listing page.
        """
        yield scrapy.Request(self.base_url, callback=self.parse)
        
    # 用于解析reponse的方法
    def parse(self, response):
        """
        Parse the actress listing page and fetch next page if available.
        """
        if response.status == 200:
            self.log(f"Now parsing page {self.page_num}")

            # Process actress data on the current page
            self.process_actress_data(response)

            # Find the next page URL if it exists
            next_page = self.get_next_page(response)
            if next_page:
                self.page_num += 1  # Increment page number
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                self.log("Final page reached.")
        else:
            self.log(f"Request failed with status {response.status}")

    def process_actress_data(self, response):
        """
        Process the actress data on the current page.
        """
        bs = BeautifulSoup(response.text, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})

        if bricks:
            actress_list = []
            for brick in bricks:
                actress_dict = self.attrsUtil.getSingleActressLink(brick)
                if actress_dict:
                    actress = self.actressUtil.getActressDetails(actress_dict["actress_link"])
                    if actress:
                        if not self.actressUtil.matchLinkIsCompanyLink(actress_dict["photo_link"]):
                            # Ensure photo link is absolute
                            if self.base_url.endswith("/"):
                                url = self.base_url[:-1]
                                actress.photo_link = url + actress.photo_link
                        actress.actress_link = actress_dict["actress_link"]
                        actress.is_censored = self.is_censored
                        actress_list.append(actress.toDict())

                        #直接复制所有属性给 ActressItem
                        yield ActressItem(**actress.__dict__)
        else:
            self.log("Bricks not found on this page.")
            self.pageUtil.save2local(response.text, "actress", ".html")

    def get_next_page(self, response):
        """
        Check if there is a next page and return its URL.
        """
        bs = BeautifulSoup(response.text, "html.parser")
        next_button = bs.find("a", {"class": "next"})
        if next_button:
            return self.base_url + next_button.get("href")
        return None

    def log(self, message):
        """
        Log the message using LogUtil.
        """
        self.logUtil.log(message)
