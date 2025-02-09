import time
import threading
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage
from javbus.utils.log_util import LogUtil


class WebUtil:
    _instance = None
    _lock = threading.Lock()
    page = None
    logUtil = LogUtil()
    baseUrls = ["https://www.javbus.com/"]
    logFilePath = "./driver.log"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(WebUtil, cls).__new__(cls)
                    cls._instance.__init_once()
        return cls._instance

    def __init_once(self):
        self.lock = threading.Lock()
        self.page = self.initialize_driver()

    def initialize_driver(self):
        """初始化浏览器驱动配置"""
        options = ChromiumOptions()
        options.auto_port()
        options.headless(False)
        options.ignore_certificate_errors()
        options.no_imgs(True).mute(True)
        options.set_argument("--no-sandbox")
        options.set_browser_path("C:\\Users\\master\\Desktop\\Soft\\Chrome\\chrome.exe")
        return ChromiumPage(options)

    def get(self, link):
        """尝试通过备选URL列表获取网页内容"""
        parsed_url = urlparse(link)
        for base_url in self.baseUrls:
            new_url = self._build_url(base_url, parsed_url)
            try:
                source = self.send(new_url)
                if self.checkIsBeDetected(source):
                    return None
                return source
            except Exception as e:
                self.logUtil.log(f"Error with URL {new_url}: {e}", log_file_path=self.logFilePath)
        self.logUtil.log("All backup URLs tried, none successful.", log_file_path=self.logFilePath)
        return None

    def send(self, new_url):
        """发送请求并返回响应内容"""
        self.logUtil.log(f"Starting request to {new_url} ...........", log_file_path=self.logFilePath)
        start_time = time.time()
        tag = self.page.new_tab()
        tag.get(new_url)
        time.sleep(20)  # 可以根据需要调整等待时间
        end_time = time.time()
        source = tag.html
        self.logUtil.log(f"Request finished. Time spent: {end_time - start_time:.2f} seconds.", log_file_path=self.logFilePath)
        tag.close()
        return source

    def checkIsBeDetected(self, source):
        """检测网页是否被识别出来"""
        bs = BeautifulSoup(source, "html.parser")
        if bs and bs.title and "Age" in bs.title.text:
            return True
        return False

    def close(self):
        """关闭浏览器"""
        self.page.quit()

    def _build_url(self, base_url, parsed_url):
        """构建新的请求URL"""
        base_parsed_url = urlparse(base_url)
        return urlunparse(
            (
                base_parsed_url.scheme,
                base_parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )
