import scrapy
from bs4 import BeautifulSoup
from items import MovieItem
from utils.log_util import LogUtil
from utils.page_util import PageUtil
from utils.attrs_util import AttrsUtil
from utils.web_util import WebUtil
from utils.timeout_util import TimeoutUtil


class SearchSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["javbus.com"]

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
        """
        Starts the requests by fetching the first page.
        """
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response for each page and check if there is a next page.
        """
        if response.status == 200:
            self.log(f"Now parsing page {self.page_num}")

            # 处理当前页面内容
            self.parse_movies(response)

            # 查找是否有下一页，若有则抓取
            next_page = self.get_next_page(response)
            if next_page:
                self.page_num += 1
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                self.log("Final page reached.")
        else:
            self.log(f"Request failed with status {response.status}")

    def parse_movies(self, response):
        """
        Parse the movies on the current page.
        """
        bs = BeautifulSoup(response.text, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})

        if bricks:
            for brick in bricks:
                is_censored = self.attrsUtil.getIsCensored(brick)
                link = self.attrsUtil.getLink(brick)
                if link:
                    self.log(f"Now visiting website link: {link}")
                    is_final_page = False
                    page_num = 0
                    while not is_final_page:
                        page_num += 1
                        is_final_page = self.pageUtil.parseMovieListPage(
                            link + "/" + str(page_num), is_censored
                        )
        else:
            self.log("Bricks not found, saving HTML locally.")
            self.pageUtil.save2local(response.text, self.tag, ".html")

    def get_next_page(self, response):
        """
        Check if there is a next page available and return its URL.
        """
        bs = BeautifulSoup(response.text, "html.parser")
        next_button = bs.find("a", {"class": "next"})
        if next_button:
            return self.base_url + next_button.get("href")
        return None

    def log(self, message):
        """
        Log the messages using the utility.
        """
        self.logUtil.log(message)
