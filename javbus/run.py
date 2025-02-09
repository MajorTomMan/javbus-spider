'''
Date: 2025-02-08 19:33:55
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 00:33:06
FilePath: \spider\javbus\run.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
from scrapy.crawler import CrawlerProcess
from javbus.spiders.genre_spider import GenreSpider
from javbus.spiders.search_spider import SearchSpider
from javbus.spiders.index_spider import IndexSpider
from javbus.spiders.actress_spider import ActressSpider

import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    选择爬取模式，并启动爬虫
    """
    print(
        """
        Welcome to the JavBus Scraper
        Please select at least one choice:
        1. Index
        2. Search
        3. Genre
        4. Actress
        5. Start All Threads
        """
    )

    num = int(input("Input: "))  # 选择模式
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

    process = CrawlerProcess()  # 创建爬虫进程

    if num == 1:
        process.crawl(IndexSpider, url=base_url + "censored/", is_censored=True)
        process.crawl(
            IndexSpider, url=base_url + "uncensored/", is_censored=False
        )
    elif num == 2:
        keyword = input("Input the keyword you want to search: ")
        if keyword:
            process.crawl(SearchSpider, url=base_url, tag=keyword)
    elif num == 3:
        process.crawl(GenreSpider, url=base_url + "genre/censored/", is_censored=True)
        process.crawl(GenreSpider, url=base_url + "uncensored/genre", is_censored=False)
    elif num == 4:
        process.crawl(
            ActressSpider, url=base_url + "actresses/censored/", is_censored=True
        )
        process.crawl(
            ActressSpider, url=base_url + "actresses/uncensored/", is_censored=False
        )
    elif num == 5:
        # 启动所有爬虫
        for keyword in keywords:
            process.crawl(SearchSpider, url=base_url, tag=keyword)
        process.crawl(IndexSpider, url=base_url + "index/censored/", is_censored=True)
        process.crawl(
            IndexSpider, url=base_url + "index/uncensored/", is_censored=False
        )
        process.crawl(GenreSpider, url=base_url + "genre/censored/", is_censored=True)
        process.crawl(GenreSpider, url=base_url + "uncensored/genre", is_censored=False)
        process.crawl(
            ActressSpider, url=base_url + "actresses/censored/", is_censored=True
        )
        process.crawl(
            ActressSpider, url=base_url + "actresses/uncensored/", is_censored=False
        )

    # 启动爬虫
    process.start()


if __name__ == "__main__":
    main()
