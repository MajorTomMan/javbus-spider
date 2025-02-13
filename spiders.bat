@echo off
start cmd /K scrapy crawl movie
start cmd /K scrapy crawl actress_detail
start cmd /K scrapy crawl actress_movie
pause