# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import requests
from scrapy import signals
from scrapy.http.response import Response
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
        spider.logger.info(
            f"Received response from {request.url} with status {response.status}"
        )
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(f"Exception while processing {request.url}: {exception}")

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)



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
    headers={
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
    }
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
            # 获取代理列表
            response = self.session.get(
                "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
                headers=self.headers
            )
            
            # 解析返回的代理列表
            ips = response.json()
            data = ips.get("data", [])
            
            for detail in data:
                ip = detail.get("ip")
                port = detail.get("port")
                if ip and port:
                    # 检查代理是否有效
                    try:
                        # 使用代理请求 httpbin
                        proxy = f"http://{ip}:{port}"
                        proxy_response = requests.get(
                            "http://httpbin.org/get",
                            proxies={"http": proxy, "https": proxy},
                            timeout=5
                        )
                        
                        # 检查返回的IP是否与代理IP相同
                        if proxy_response.status_code == 200:
                            proxy_data = proxy_response.json()
                            if proxy_data.get("origin") == ip:
                                spider.logger.info(f"Proxy {proxy} is working.")
                                
                                # 如果代理可用，将其设置到request中
                                request.meta['proxy'] = proxy
                                return None
                            else:
                                spider.logger.warning(f"Proxy {proxy} returned a different IP.")
                        else:
                            spider.logger.warning(f"Proxy {proxy} failed with status code {proxy_response.status_code}.")
                    except requests.exceptions.RequestException as e:
                        spider.logger.warning(f"Error with proxy {ip}:{port} - {e}")

            spider.logger.error("No valid proxies found.")
            return None

    def process_response(self, request, response, spider):
        # 处理响应，记录响应状态码并检查是否有异常
        return response

    def process_exception(self, request, exception, spider):
        pass
    def spider_opened(self, spider):
        pass