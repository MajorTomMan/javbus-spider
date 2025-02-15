# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import redis
import json
import requests
from scrapy import signals
from scrapy.http.response import Response
from urllib.parse import urlparse, urlunparse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy_redis.spiders import RedisSpider


class JavbusSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class JavbusDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self,):
        self.back_links = "javbus:backup_links"
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 在请求发出之前添加请求头
        spider.logger.info(f"Updating request headers for {request.url}")
        return None

    def process_response(self, request, response, spider):
        # 处理响应，记录响应状态码并检查是否有异常
        # 检查状态码
        if response.status != 200:
            spider.logger.warning(
                f"Received non-200 status {response.status} from {request.url}"
            )
            redis_client = redis.StrictRedis(
                host=settings.get("REDIS_HOST"),
                port=settings.get("REDIS_PORT"),
                **settings.get("REDIS_PARAMS"),
            )
            # 从 Redis 获取备用 URL
            backup_url_dict = redis_client.get(self.back_links)
            if backup_url:
                backup_url_dict = json.loads(backup_url_dict)  # 需要解码 Redis 字符串
                # 替换原有 URL 的主机部分为新的 URL
                new_url = self._replace_base_url(request.url, backup_url_dict["url"])
                spider.logger.info(f"Retrying with new URL: {new_url}")
                # 创建新的 Request
                new_request = request.replace(url=new_url)
                # 重新发起请求
                return new_request
        else:
            spider.logger.info(
                f"Received response from {request.url} with status {response.status}"
            )
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(f"Exception while processing {request.url}: {exception}")

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def _replace_base_url(self, original_url, new_base_url):
        # 解析原始 URL 和新的 Base URL
        parsed_original = urlparse(original_url)
        parsed_new_base = urlparse(new_base_url)

        # 替换 scheme 和 netloc（即 http/https 和域名部分）
        new_url = urlunparse(
            (
                parsed_new_base.scheme,  # 使用新 URL 的 scheme
                parsed_new_base.netloc,  # 使用新 URL 的域名
                parsed_original.path,  # 保留原来的路径
                parsed_original.params,  # 保留原来的 params
                parsed_original.query,  # 保留原来的 query
                parsed_original.fragment,  # 保留原来的 fragment
            )
        )

        return new_url


class JavbusSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class JavbusProxyMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    session = requests.Session()
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
    }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        # 处理响应，记录响应状态码并检查是否有异常
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass
