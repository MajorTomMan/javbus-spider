import scrapy
from scrapy.crawler import CrawlerProcess
from genre_spider import GenreSpider
from search_spider import SearchSpider
from index_spider import IndexSpider
from actress_spider import ActressSpider


class JavBusSpider(scrapy.Spider):
    name = "javbus"
    allowed_domains = ["javbus.com"]
    base_url = "https://www.javbus.com/"
    keywords = [
        "北野未奈",
        "Rion",
        "大橋未久",
        "藤森里穂",
        "安齋らら",
        "吉沢明歩",
        "メロディー・雛・マークス",
        "星宮一花",
    ]
    process = CrawlerProcess() 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num = None
        self.is_censored = True

    def start_requests(self):
        """
        This method is responsible for starting the scraping process based on the user's input.
        """
        print(
            """
            welcome to the jav program
            pls select at least one choice 
            1. index
            2. search
            3. genre
            4. actress
            5. startAllThread
            """
        )
        self.num = int(input("input:"))
        if self.num == 1:
            self.process.crawl(IndexSpider,url=self.base_url + "index/censored/",is_censored=True)
            self.process.crawl(IndexSpider,url=self.base_url + "index/uncensored/",is_censored=False)
        elif self.num == 2:
            keyword = input("input what keyword you want to search:")
            if keyword is not None:
                self.process.crawl(SearchSpider,url=self.base_url,tag=keyword)
        elif self.num == 3:
            self.process.crawl(GenreSpider,url=self.base_url + "genre/censored/",is_censored=True)
            self.process.crawl(GenreSpider,url=self.base_url + "uncensored/genre",is_censored=False)
        elif self.num == 4:
            self.process.crawl(ActressSpider,url=self.base_url + "actresses/censored/",is_censored=True)
            self.process.crawl(ActressSpider,url=self.base_url + "actresses/uncensored/",is_censored=False)
        elif self.num == 5:
            # Start all tasks
            for keyword in self.keywords:
                self.process.crawl(SearchSpider,url=self.base_url,tag=keyword)
            self.process.crawl(IndexSpider,url=self.base_url + "index/censored/",is_censored=True)
            self.process.crawl(IndexSpider,url=self.base_url + "index/uncensored/",is_censored=False)
            self.process.crawl(GenreSpider,url=self.base_url + "genre/censored/",is_censored=True)
            self.process.crawl(GenreSpider,url=self.base_url + "uncensored/genre",is_censored=False)
            self.process.crawl(ActressSpider,url=self.base_url + "actresses/censored/",is_censored=True)
            self.process.crawl(ActressSpider,url=self.base_url + "actresses/uncensored/",is_censored=False)
        # 启动爬虫进程
        self.process.start()