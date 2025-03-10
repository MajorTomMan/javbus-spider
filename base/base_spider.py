

from scrapy.exceptions import CloseSpider
from scrapy_redis.spiders import RedisSpider
import logging
import redis
from scrapy.utils.project import get_project_settings
from scrapy import signals
from javbus.utils.page_util import PageUtil

settings = get_project_settings()
logger = logging.getLogger(__name__)

class BaseSpider(RedisSpider):
    """所有爬虫的基类"""
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        
        # **在这里绑定 spider_error 信号**
        spider.crawler.signals.connect(spider.on_spider_error, signal=signals.spider_error)
        
        return spider
    
    
    def parse(self, response):
        """可以覆盖此方法来处理 response"""
        pass

    def get_redis_connection(self):
        """获取 Redis 连接"""
        redis_params = settings.get('REDIS_PARAMS')
        # 请根据你的 Redis 设置调整
        return redis.StrictRedis(    
                        host=redis_params['host'],
                        port=redis_params['port'],
                        db=redis_params['db'],
                        password=redis_params['password']
        )


    def handle_exception(self, failure):
        """统一处理爬虫中的异常"""
        logger.error(f"Spider encountered an exception: {failure}")
        raise CloseSpider("Encountered an exception, stopping spider.")
    
    def log(self, message):
        """统一日志记录"""
        logger.info(message)
            

    def on_spider_error(self, failure, response, spider):
        """捕获爬虫错误"""
        self.log(f"Spider error occurred: {failure}", level="ERROR")
        raise CloseSpider("An error occurred, stopping spider.")

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None

    def get_next_page(self, bs):
        return PageUtil().has_next_page(bs)