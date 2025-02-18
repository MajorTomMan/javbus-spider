import time
import threading
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, WebPage
import logging


class WebUtil:
    _instance = None
    _lock = threading.Lock()
    page = None  # 浏览器驱动
    logFilePath = "./driver.log"

    def __init__(self):
        self.logger = logging.getLogger(__name__)  # 初始化 Scrapy 的日志记录器

    def initialize_driver(self):
        """初始化浏览器驱动配置"""
        if self.page is None:  # 如果没有初始化浏览器，则进行初始化
            options = ChromiumOptions()
            options.auto_port()
            options.headless(True)
            options.ignore_certificate_errors()
            options.no_imgs(True).mute(True)
            options.set_argument("--no-sandbox")
            options.set_browser_path(
                "C:\\Users\\master\\Desktop\\Soft\\Chrome\\chrome.exe"
            )
            self.page = WebPage(chromium_options=options)

    def get(self, link):
        try:
            tag = self.send(link)
            return tag
        except Exception as e:
            self.logger.error(f"Error with URL {link}: {e}")


    def send(self, link):
        """发送请求并返回响应内容"""
        self.logger.info(f"Starting request to {link} ...........")
        start_time = time.time()

        self.initialize_driver()  # 确保在请求时浏览器已经初始化
        if self.page is None:  # 如果浏览器初始化失败，直接返回
            self.logger.error(f"Browser initialization failed for {link}.")
            return None
        tag = self.page.new_tab()  # 创建新标签页
        tag.get(link)
        end_time = time.time()
        self.logger.info(
            f"Request finished. Time spent: {end_time - start_time:.2f} seconds."
        )
        return tag

    def close(self):
        """关闭浏览器"""
        if self.page:
            self.page.quit()
            self.page = None  # 重置浏览器驱动为 None，确保下次需要时再初始化
