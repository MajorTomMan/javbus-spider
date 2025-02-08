# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import Response
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from utils.web_util import WebUtil

class JavbusDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    
    def __init__(self):
        self.web_util = WebUtil()
    
    
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """拦截请求，使用 WebUtil 代替 Scrapy 自带下载器"""
        url = request.url
        spider.logger.info(f"Using WebUtil to fetch: {url}")

        try:
            response_content = self.web_util.get(url)  # 调用 WebUtil 的 get 方法
            if response_content is None:
                spider.logger.warning(f"WebUtil failed to fetch {url}, returning 404")
                return Response(url=url, status=404, body=b"", request=request)

            return Response(
                url=url,
                status=200,
                body=response_content.encode("utf-8"),
                request=request,
                headers={"Content-Type": "text/html; charset=utf-8"},
            )
        except Exception as e:
            spider.logger.error(f"Error fetching {url} using WebUtil: {str(e)}")
            return Response(url=url, status=500, body=b"", request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        """处理 WebUtil 可能抛出的异常"""
        spider.logger.error(f"Exception while processing {request.url}: {exception}")

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
