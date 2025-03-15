'''
Date: 2025-03-10 21:19:15
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-03-11 20:03:33
FilePath: \spider\base\base_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''


import copy
from scrapy.exceptions import CloseSpider
from scrapy_redis.spiders import RedisSpider
import logging
import redis
import time
from scrapy.utils.project import get_project_settings
from scrapy import signals
from javbus.utils.page_util import PageUtil
from javbus.common.constants import javbus_base_url
from javbus.utils.attrs_util import AttrsUtil

settings = get_project_settings()
logger = logging.getLogger(__name__)

class BaseSpider(RedisSpider):
    """所有爬虫的基类"""
    def __init__(self, *args, **kwargs):
        # 深拷贝 kwargs
        kwargs = copy.deepcopy(kwargs)
        self.javbus_base_url = kwargs.get("url", javbus_base_url)
        self.is_censored = AttrsUtil().str_to_bool(kwargs.get("is_censored", True))
        self.actress = kwargs.get("actress", "北野未奈")
        self.code = kwargs.get("code", "")
        self.director = kwargs.get("director", "")
        self.studio = kwargs.get("studio", "")
        self.label = kwargs.get("label", "")
        self.series = kwargs.get("series", "")
        
        
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

    def log(self, message,level=None):
        """统一日志记录，动态适配日志级别"""
        if level:
            level = level.upper() 
            if level == "DEBUG":
                logger.debug(message)
            elif level == "INFO":
                logger.info(message)
            elif level == "WARNING":
                logger.warning(message)
            elif level == "ERROR":
                logger.error(message)
            elif level == "CRITICAL":
                logger.critical(message)
        else:
            logger.info(message)

    def on_spider_error(self, failure, response, spider):
        """捕获爬虫错误"""
        self.log(f"Spider error occurred: {failure}", level="ERROR")
        raise CloseSpider("An error occurred, stopping spider.")

    def get_link(self, brick):
        return brick["href"] if brick["href"] else None

    def get_next_page(self, bs):
        return PageUtil().has_next_page(bs)

    def push_to_redis(self,key,data):
        # 获取微秒级别的时间戳
        timestamp_us = int(time.time() * 1_000_000)
        counter_id = self.server.incr("unique_id")
        score = timestamp_us + counter_id
        self.server.execute_command("ZADD", key, score, data)

    def pop_from_redis(self,key):
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        # 取出分数最大的元素（先进先出）
        # 取出并从redis中删除最旧的数据
        pipe.zrange(key, 0, 0)
        pipe.zremrangebyrank(key, 0, 0)
        results, count = pipe.execute()
        if results:
            return results[0]
        else:
            return None

    def pop_priority_queue(self, redis_key, batch_size):
        results = []
        for _ in range(batch_size):
            item = self.pop_from_redis(redis_key)
            if item is not None:
                results.append(item)
        return results
