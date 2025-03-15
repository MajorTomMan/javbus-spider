import logging
import os
from datetime import datetime
from scrapy import signals
from scrapy.exceptions import NotConfigured

class LogExtension:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    @classmethod
    def from_crawler(cls, crawler):
        log_dir = crawler.settings.get("LOG_DIRECTORY", "logs")  # 默认日志目录
        ext = cls(log_dir)

        # 监听爬虫信号
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_opened(self, spider):
        """当爬虫启动时，设置日志"""
        log_filename = os.path.join(self.log_dir, f"{spider.name}_{datetime.now().strftime('%Y-%m-%d')}.log")

        # 获取 Scrapy 的 root logger
        logger = logging.getLogger('scrapy')

        handler = logging.FileHandler(log_filename, encoding="utf-8")
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)

        # 添加处理程序到 Scrapy logger
        logger.addHandler(handler)
        spider.logger.info(f"logger opened: {log_filename}")

    def spider_closed(self, spider):
        """爬虫结束时，移除日志 handler，避免影响下次爬取"""
        logger = logging.getLogger('scrapy')

        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
                handler.close()
