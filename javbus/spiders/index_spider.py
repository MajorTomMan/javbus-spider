import scrapy
from bs4 import BeautifulSoup
from items import MovieItem


class IndexSpider(scrapy.Spider):
    name = "index"
    allowed_domains = ["javbus.com"]

    def __init__(
        self, url="https://www.javbus.com/", is_censored=True, *args, **kwargs
    ):
        super(IndexSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored
        self.page_num = 1  # Initial page number, will be handled in URL construction

    def start_requests(self):
        # Start request by determining if the page is censored or not
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:

            bs = BeautifulSoup(response.body, "html.parser")
            self.log(f"Now parsing page {self.page_num}")

            # Process the bricks (movie links) on this page
            self.process_bricks(bs)

            # Check for the next page and continue crawling if it exists
            next_page = self.get_next_page(bs)
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                self.log("No next page, stopping crawl.")
        else:
            self.log("Request failed with status code: {}".format(response.status))

    def process_bricks(self, bs):
        """
        Extract movie links from the page and follow them.
        """
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.get_link(brick)
                if link:
                    yield scrapy.Request(link, callback=self.parse_detail_page)
        else:
            self.log("No bricks found on this page.")

    def parse_detail_page(self, response):
        """
        Parse the detailed movie page and yield the movie item.
        """
        bs = BeautifulSoup(response.text, "html.parser")
        movie_item = self.parse_movie_details(bs)
        if movie_item:
            yield movie_item

    def parse_movie_details(self, bs):
        """
        Extract the movie details from the page.
        """
        movie_item = MovieItem()
        movie_item["title"] = bs.find("h1", {"class": "movie-title"}).get_text(
            strip=True
        )
        # Additional fields can be added as needed
        return movie_item

    def get_link(self, brick):
        """
        Extract the movie link from the brick element.
        """
        link = brick.find("a", href=True)
        return link["href"] if link else None

    def get_next_page(self, bs):
        """
        Check if the next page exists and return its URL.
        """
        next_button = bs.find("a", {"class": "next"})
        if next_button:
            return self.base_url + next_button.get("href")
        return None

    def log(self, message):
        """
        Log the message for debugging purposes.
        """
        self.logger.info(message)
