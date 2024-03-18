from utils.LogUtil import LogUtil
from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.TimeoutUtil import TimeoutUtil


class TimeoutUtil:
    webUtil = WebUtil()
    timeouts = []
    pageUtil = PageUtil()
    logUtil = LogUtil()
    timeoutUtil = TimeoutUtil()

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
