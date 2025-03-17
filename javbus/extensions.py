import logging
import os
import copy
from datetime import datetime
from scrapy import signals

class JavbusLoggerExtension:
    def __init__(self, log_file):
        self.log_file = log_file

    @classmethod
    def from_crawler(cls, crawler):
        log_base_dir = crawler.settings.get("LOG_DIRECTORY", "logs")

        # 以当前时间（精确到秒）作为文件夹名
        timestamp_dir = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = os.path.join(log_base_dir, timestamp_dir)
        os.makedirs(log_dir, exist_ok=True)  # 确保目录存在

        # 获取爬虫名字
        spider_name = crawler.spider.name

        # 获取爬虫参数
        kwargs = copy.deepcopy(crawler.spider.kwargs)

        # 生成参数字符串，保证参数顺序一致
        params_str = "_".join(f"{key}={value}" for key, value in sorted(kwargs.items())) if kwargs else ""

        # 构造日志文件名
        if params_str:
            log_file_name = f"{spider_name}_{params_str}.log"
        else:
            log_file_name = f"{spider_name}.log"

        log_file = os.path.join(log_dir, log_file_name)

        # 创建扩展实例
        ext = cls(log_file)

        # 连接信号
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
