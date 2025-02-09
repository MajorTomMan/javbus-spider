'''
Date: 2025-02-08 20:32:58
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 00:12:21
FilePath: \spider\javbus\debug.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javbus.spiders.index_spider import IndexSpider


process = CrawlerProcess(get_project_settings())

process.crawl(IndexSpider)
process.start()
