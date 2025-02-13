'''
Date: 2025-02-07 22:00:29
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-11 23:02:56
FilePath: \spider\javbus\settings.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
# Scrapy settings for javbus project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "javbus"

SPIDER_MODULES = ["javbus.spiders"]
NEWSPIDER_MODULE = "javbus.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "javbus.middlewares.JavbusSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "javbus.middlewares.JavbusDownloaderMiddleware": 543,
    "scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware": None,
    "scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware": None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "javbus.pipelines.JavbusPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 启用 scrapy-redis 的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 启用 scrapy-redis 的去重机制
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 配置请求队列使用 Redis 来存储待抓取链接
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"
# 持久化爬取队列（爬虫结束后，保留队列）
SCHEDULER_PERSIST = True

# Redis 服务器地址（默认 127.0.0.1:6379）
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PARAMS = {
    "db": 0,
    "password": "root",
}
# 设置请求之间的延迟时间（单位：秒）
DOWNLOAD_DELAY = 10  # 每个请求之间的延迟为 2 秒

# 设置下载中间件随机化延迟时间（单位：秒），通过设置`randomize_download_delay`来启用更随机的延迟
RANDOMIZE_DOWNLOAD_DELAY = True

# 设置最大并发请求数，避免过度并发
CONCURRENT_REQUESTS = 2

# 设置每个连接的最大并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2
