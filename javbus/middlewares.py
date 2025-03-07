# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import redis
import json
from urllib.parse import urlparse, urlunparse
from twisted.internet.error import (
    TCPTimedOutError,
    ConnectionRefusedError,
    DNSLookupError,
)
from requests.exceptions import ConnectionError, ConnectTimeout
from javbus.common.redis_keys import javbus_backup_links,proxy_ip_key
from javbus.utils.request_util import RequestUtil
from javbus.common.constants import get_cloud_ip_proxy_url




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
        spider.logger.info(f"Sending request: {request.url}")
        return None

    def process_response(self, request, response, spider):
        spider.logger.info(
            f"Received response: {response.url} with status: {response.status}"
        )
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(
            f"Exception occurred for request {request.url}: {exception}"
        )
        if response.status == 403:
            spider.logger.warning(f"Request to {request.url} returned 403 Forbidden. Retrying...")
            return request
        return None

class JavbusTimeOutMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.back_links = javbus_backup_links

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        if (
            type(exception) is TCPTimedOutError
            or ConnectionRefusedError
            or DNSLookupError
            or ConnectionError
            or ConnectTimeout
        ):
            spider.logger.warning(
                f"request {request.url} timeout,try another link to request"
            )
            settings = spider.settings
            redis_client = redis.StrictRedis(
                host=settings.get("REDIS_HOST"),
                port=settings.get("REDIS_PORT"),
                **settings.get("REDIS_PARAMS"),
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
                    meta={
                        **request.meta,
                        "is_change_link": True,
                        "new_url": backup_url_dict["url"],
                    },
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
        response = RequestUtil().get(get_cloud_ip_proxy_url)
        if response.status_code == 200:
            proxy = json.loads(response)
            ip = proxy["ip"]
            port = proxy["port"]
            new_ip = f"http://{ip}:{port}"
            request.meat["proxy"] = new_ip
            spider.logger.info(f"change proxy ip to {new_ip}")
        return None

    def process_response(self, request, response, spider):
        # 处理响应，记录响应状态码并检查是否有异常
        return response

    def process_exception(self, request, exception, spider):
        pass

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
