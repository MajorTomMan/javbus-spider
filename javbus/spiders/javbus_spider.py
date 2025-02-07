import scrapy
import time
from urllib.parse import urlparse
from Genre import genre
from Search import search
from Index import index
from Actress import actresses


class JavBusSpider(scrapy.Spider):
    name = "javbus_spider"
    allowed_domains = ["seedmm.shop"]
    base_url = "https://www.seedmm.shop/"
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
            yield scrapy.Request(
                self.base_url + "index/censored/", callback=self.parse_index
            )
            yield scrapy.Request(
                self.base_url + "index/uncensored/", callback=self.parse_index
            )
        elif self.num == 2:
            keyword = input("input what keyword you want to search:")
            yield scrapy.Request(
                f"{self.base_url}searchstar/{keyword}/1", callback=self.parse_search
            )
        elif self.num == 3:
            yield scrapy.Request(
                self.base_url + "genre/censored/", callback=self.parse_genre
            )
            yield scrapy.Request(
                self.base_url + "uncensored/genre", callback=self.parse_genre
            )
        elif self.num == 4:
            yield scrapy.Request(
                self.base_url + "actresses/censored/", callback=self.parse_actresses
            )
            yield scrapy.Request(
                self.base_url + "actresses/uncensored/", callback=self.parse_actresses
            )
        elif self.num == 5:
            # Start all tasks
            for keyword in self.keywords:
                yield scrapy.Request(
                    f"{self.base_url}searchstar/{keyword}/1", callback=self.parse_search
                )
            yield scrapy.Request(
                self.base_url + "index/censored/", callback=self.parse_index
            )
            yield scrapy.Request(
                self.base_url + "index/uncensored/", callback=self.parse_index
            )
            yield scrapy.Request(
                self.base_url + "genre/censored/", callback=self.parse_genre
            )
            yield scrapy.Request(
                self.base_url + "uncensored/genre", callback=self.parse_genre
            )
            yield scrapy.Request(
                self.base_url + "actresses/censored/", callback=self.parse_actresses
            )
            yield scrapy.Request(
                self.base_url + "actresses/uncensored/", callback=self.parse_actresses
            )

    def parse_index(self, response):
        """
        Parsing logic for the index page.
        """
        self.log(f"Starting parse_index for {response.url}")
        # Use BeautifulSoup to parse and extract content, or use Scrapy selectors directly
        # Example:
        # bs = BeautifulSoup(response.text, 'html.parser')
        # Extract information like so:
        # bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        # (Alternatively, use Scrapy selectors, e.g. response.xpath() or response.css())
        # Process the page here, handle pagination, etc.
        pass  # Add your logic here

    def parse_search(self, response):
        """
        Parsing logic for the search result page.
        """
        self.log(f"Starting parse_search for {response.url}")
        # Handle search results pagination, extracting links, etc.
        pass  # Add your logic here

    def parse_genre(self, response):
        """
        Parsing logic for the genre page.
        """
        self.log(f"Starting parse_genre for {response.url}")
        # Handle genre parsing and extraction
        pass  # Add your logic here

    def parse_actresses(self, response):
        """
        Parsing logic for the actress page.
        """
        self.log(f"Starting parse_actresses for {response.url}")
        # Handle actress parsing, extraction, etc.
        pass  # Add your logic here
