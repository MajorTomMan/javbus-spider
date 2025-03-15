from datetime import datetime
import logging
import os
import sys
from scrapy import signals
import copy



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
        kwargs = copy.deepcopy(crawler.spider.custom_settings)  # 获取爬虫的参数（可以是 custom_settings 或者其他地方）

        # 初始化 params_str
        params_str = ""
        if kwargs:
            # 提取所有参数并拼接成一个字符串
            for key, value in kwargs.items():
                params_str += f"_{key}={str(value)}"  # 拼接每个参数
            # 根据爬虫名字、参数和时间生成日志文件名
            log_file = os.path.join(log_dir, f"{spider_name}{params_str}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        else:
            log_file = os.path.join(log_dir, f"{spider_name}_{datetime.now().strftime('%Y-%m-%d')}.log")
        # 创建扩展对象
        ext = cls(log_file)

        # 监听爬虫启动信号
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        return ext

    def spider_opened(self, spider):
        """爬虫启动时，设置日志到文件 + 控制台"""
        logger = logging.getLogger()

        # 文件日志
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # 设置格式
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加到 Scrapy logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        spider.logger.info(f"Logging to file: {self.log_file}")
