from utils.log_util import LogUtil
from utils.web_util import WebUtil


class TimeoutUtil:

    def __init__(self, page_util) -> None:
        self.webUtil = WebUtil()
        self.timeouts = []
        self.logUtil = LogUtil()
        self.pageUtil = page_util  # 通过依赖注入传递 PageUtil 的实例

    def addLink(self, link, isCensored):
        self.timeouts.append(
            {"link": link, "is_censored": isCensored, "is_visited": False}
        )

    def requestTimeoutLink(self):
        if len(self.timeouts) >= 1:
            for timeout in self.timeouts[:]:
                if not timeout["is_visited"]:
                    isFinalPage = self.pageUtil.parseMovieListPage(
                        timeout["link"], timeout["is_censored"]
                    )
                    if isFinalPage:
                        self.logUtil.log(
                            "requst link"
                            + timeout["link"]
                            + " still timeout, abandon this link"
                        )
                    self.timeouts.remove(timeout)

    def isEmpty(self):
        if len(self.timeouts) == 0:
            return True
        return False
