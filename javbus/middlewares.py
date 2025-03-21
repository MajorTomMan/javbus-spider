# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import redis
import json
import copy
from urllib.parse import urlparse, urlunparse
from twisted.internet.error import (
    TCPTimedOutError,
    ConnectionRefusedError,
    DNSLookupError,
)
from twisted.web._newclient import ResponseNeverReceived
from requests.exceptions import ConnectionError, ConnectTimeout
from javbus.common.redis_keys import javbus_backup_links


class JavbusSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

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


class JavbusDownloaderMiddleware:

    def process_request(self, request, spider):
        spider.logger.info(f"Sending request: {request.url}, with meta: {request.meta}")
        # 使用深拷贝来避免请求之间的共享引用
        # 防止多并发时meta里的数据因为scrapy本身对meta使用浅拷贝导致多个请求使用引用相同的meta
        # 会导致一旦meta使用可变类型就会导致多个爬虫中的数据错乱和混淆
        # 在meta中使用字典这种可变类型导致数据混淆或者错乱!!!!

    def process_response(self, request, response, spider):
        spider.logger.info(
            f"Received response: {response.url} with status: {response.status}"
        )
        if response.status == 403:
            spider.logger.warning(f"Request to {request.url} returned 403 Forbidden. Retrying...")
            return request.replace(url=request.url,meta=copy.deepcopy(request.meta),dont_filter=True)


        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(
            f"Exception occurred for request {request.url}: {exception}"
        )
        return None

class JavbusTimeOutMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.back_links = javbus_backup_links

    def process_exception(self, request, exception, spider):
        if isinstance(
            exception,
            (
                TCPTimedOutError,
                ConnectionRefusedError,
                DNSLookupError,
                ConnectionError,
                ConnectTimeout,
                ResponseNeverReceived,
            ),
        ):
            spider.logger.warning(
                f"request {request.url} timeout,try another link to request"
            )
            settings = spider.settings
            redis_client = redis.StrictRedis(
                host=settings.get("REDIS_HOST"),
                port=settings.get("REDIS_PORT"),
                db=settings.get("REDIS_DB"),
                password=settings.get("REDIS_PASSWORD")
            )
            # 从 Redis 获取备用 URL
            backup_url_dict = redis_client.spop(self.back_links)
            if backup_url_dict:
                backup_url_dict = json.loads(backup_url_dict)  # 需要解码 Redis 字符串
                # 替换原有 URL 的主机部分为新的 URL
                new_url = self.replace_base_url(request.url, backup_url_dict["url"])
                spider.logger.info(f"Retrying with new URL: {new_url}")
                # 创建新的 Request
                new_request = request.replace(
                    url=new_url,
                    meta=copy.deepcopy({
                        **request.meta,
                        "is_change_link": True,
                        "new_url": backup_url_dict["url"],
                    }),
                    dont_filter=True,
                )
                # 重新发起请求
                return new_request
        else:
            return None

    def replace_base_url(self, original_url, new_base_url):
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


class JavbusProxyMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        is_change_link = request.meta.get("is_change_link", False)
        if is_change_link:
            new_url = request.meta.get("new_url", "")
            if new_url:
                request.url = self.replace_base_url(request.url, new_url)
                return request


    def replace_base_url(self, original_url, new_base_url):
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
