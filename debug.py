'''
Date: 2025-02-08 20:32:58
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-09 22:24:11
FilePath: \spider\debug.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from javbus.spiders.movie_spider import MovieSpider
from javbus.spiders.actress_detail_spider import ActressDetailSpider

process = CrawlerProcess(get_project_settings())

process.crawl(MovieSpider)
process.start()
