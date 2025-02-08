'''
Date: 2025-02-08 20:32:58
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-08 20:55:29
FilePath: \spider\javbus\runner.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.index_spider import IndexSpider


process = CrawlerProcess(get_project_settings())

process.crawl(IndexSpider)
process.start()  # the script will block here until the crawling is finished
