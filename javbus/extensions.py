import logging
import os
import copy
from datetime import datetime
from scrapy import signals
import json

class JavbusLoggerExtension:
    def __init__(self, log_file):
        self.log_file = log_file

    @classmethod
    def from_crawler(cls, crawler):
        log_dir = crawler.settings.get("LOG_DIRECTORY", "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 获取爬虫名字
        spider_name = crawler.spider.name

        # 获取爬虫参数
        kwargs = copy.deepcopy(crawler.spider.kwargs)

        # 构建参数字符串，保证参数顺序一致（这样不同参数组合会生成不同的文件）
        params_str = "_".join(f"{key}={value}" for key, value in sorted(kwargs.items())) if kwargs else ""

        # 获取当前时间戳（精确到秒）
        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 构造日志文件名（文件名带时间戳和参数）
        if params_str:
            log_file_name = f"{spider_name}_{params_str}_{timestamp_str}.log"
        else:
            log_file_name = f"{spider_name}_{timestamp_str}.log"
        
        log_file = os.path.join(log_dir, log_file_name)

        # 检查日志文件是否已存在
        if not os.path.exists(log_file):
            # 文件不存在时创建
            ext = cls(log_file)
        else:
            # 文件已存在，使用现有文件
            ext = cls(log_file)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        return ext

    def spider_opened(self, spider):
        """爬虫启动时，检查是否已存在相同 handler，避免重复添加"""
        logger = logging.getLogger()

        # 避免重复添加 file handler
        if any(isinstance(h, logging.FileHandler) and h.baseFilename == self.log_file for h in logger.handlers):
            return

        # 创建文件 handler
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # 设置日志格式
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        spider.logger.info(f"Logging to file: {self.log_file}")
