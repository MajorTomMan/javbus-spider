import logging
import os
import copy
from datetime import datetime
from scrapy import signals
from scrapy.utils.log import configure_logging
class JavbusLoggerExtension:
    def __init__(self, log_file):
        self.log_file = log_file

    @classmethod
    def from_crawler(cls, crawler):
        log_base_dir = crawler.settings.get("LOG_DIRECTORY", "logs")

        # 以当前时间（精确到秒）作为文件夹名
        timestamp_dir = datetime.now().strftime("%Y-%m-%d_%H-%M")
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
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        """设置日志系统，输出到文件和终端"""
        configure_logging(install_root_handler=False)  # 关闭 Scrapy 默认日志处理器

        log_formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')

        # 文件日志
        self.file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(log_formatter)

        # 终端日志
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(log_formatter)

        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(self.file_handler)
        root_logger.addHandler(self.console_handler)
        spider.logger.info(f"Logging to file: {self.log_file}")
        
    def spider_closed(self, spider, reason):
        spider.logger.info(f"Spider {spider.name} closed: {reason}")
        root_logger = logging.getLogger()
        # 先检查 handler 是否存在再移除
        if hasattr(self, "file_handler"):
            root_logger.removeHandler(self.file_handler)
            self.file_handler.close()  # 关闭文件

        if hasattr(self, "console_handler"):
            root_logger.removeHandler(self.console_handler)
            self.console_handler.close()