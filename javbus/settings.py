"""
Date: 2025-02-07 22:00:29
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-17 20:40:51
FilePath: \spider\javbus\settings.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

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
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "javbus.middlewares.JavbusSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "javbus.middlewares.JavbusDownloaderMiddleware": 543,
    #"javbus.middlewares.JavbusProxyMiddleware": 544,
    "javbus.middlewares.JavbusTimeOutMiddleware": 545,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy_prometheus.prometheus.PrometheusExporter': 500,
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

# 使用 FIFO 队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.FifoQueue"


# 保证去重数据保存在 Redis 中，支持分布式
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 持久化爬取队列（爬虫结束后，保留队列）
SCHEDULER_PERSIST = False

# Redis 服务器地址（默认 127.0.0.1:6379）
REDIS_HOST = "13.114.140.140"
REDIS_PORT = 5533
REDIS_PARAMS = {
    "db": 0,
    "password": "root",
}
# 设置请求之间的延迟时间（单位：秒）
DOWNLOAD_DELAY = 1.2
# 保证每分钟只有50个请求
CONCURRENT_REQUESTS = 1

# 设置下载中间件随机化延迟时间（单位：秒），通过设置`randomize_download_delay`来启用更随机的延迟
RANDOMIZE_DOWNLOAD_DELAY = True

DUPEFILTER_DEBUG = True

LOG_LEVEL = "DEBUG"

DOWNLOAD_TIMEOUT = 10  # 设置请求超时时间
DOWNLOAD_CONNECT_TIMEOUT = 10  # 设置连接超时时间
RETRY_TIMES = 3  # 设置最大重试次数
RETRY_HTTP_CODES = [408, 500, 502, 503, 504, 403, 404]  # 重试时的错误码