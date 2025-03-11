import logging
import requests
from bs4 import BeautifulSoup
from javbus.utils.request_util import RequestUtil
from javbooks.common.constants import javbooks_search_url
from javbooks.common.constants import javbooks_base_url

headers = {
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding: gzip, deflate, br, zstd",
    "Accept-Language: zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5",
    "Cache-Control: no-cache",
    "Cookie: PHPSESSID=grrbpnkjqjkeuoj3iuo1g3fsr4; TSCvalue=gb; _ga=GA1.2.404428871.1741698410; _gid=GA1.2.450998999.1741698410; HstCfa3110609=1741698410763; HstCmu3110609=1741698410763; HstCnv3110609=1; HstCns3110609=1; __dtsu=104017399642172DB5D5A7E9CDBFF8D0; _cc_id=e8d1745776cb7a6906db8fe6f59e6950; panoramaId_expiry=1741784823187; panoramaId=6179d28ef7445275b9dd2563ffe7a9fb927ae11a3bd6173a4cd8bc43e2bc3f46; panoramaIdType=panoDevice; HstCla3110609=1741699282768; HstPn3110609=3; HstPt3110609=3; _ga_9RRW7ZEM7N=GS1.2.1741698411.1.1.1741699287.0.0.0",
    "Pragma: no-cache",
    "Priority: u=0, i",
    'Sec-CH-UA: "Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "Sec-CH-UA-Mobile: ?0",
    'Sec-CH-UA-Platform: "Windows"',
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Upgrade-Insecure-Requests: 1",
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

cookies = None  # Global cookies


class SearchPageUtil:
    logger = logging.getLogger(__name__)

    def get_topic_image(self, keyword=None):
        """
        Retrieves the topic image URL based on the given keyword.
        Handles expired cookies and retrieves new ones when necessary.
        """
        response = self._get_page(javbooks_search_url, keyword)
        if response:
            return self._extract_image_url(response)
        return None

    def _get_page(self, url, keyword):
        """
        Posts the keyword to the given URL and returns the response.
        If cookies have expired, it handles the re-acquisition of cookies.
        """
        global cookies
        response = RequestUtil().post(url, keyword, cookies=cookies)

        # If cookies are expired, re-fetch cookies and retry the request
        if self._cookies_expired(response):
            self._handle_cookie_expiry(response)

        return RequestUtil().post(url, keyword, cookies=cookies) if cookies else None

    def _cookies_expired(self, response):
        """
        Checks if the cookies are expired by looking for specific HTML elements.
        """
        if response is None:
            # 记录错误日志
            self.logger.error("Response is None")
            return False  # 或者返回其他适当值
        bs = BeautifulSoup(response.content, "html.parser")
        scale = bs.find("div", {"class": "scale_2"})
        return bool(scale)

    def _handle_cookie_expiry(self, response):
        """
        Handles the cookie expiry scenario, re-fetches cookies using DrissionPage.
        """
        global cookies
        self.logger.info("Cookies expired, attempting to fetch new cookies.")
        response = RequestUtil().get(
            javbooks_base_url+"/serchinfo_censored/IamOverEighteenYearsOld/topicsbt_1.htm"
        )
        if response:
            new_cookies = requests.utils.dict_from_cookiejar(response.cookies)
            if new_cookies:
                new_cookies["TSCvalue"] = "gb"
                self.logger.info("get new cookies:" + str(new_cookies))
                cookies = new_cookies
                self.logger.info("Successfully fetched new cookies.")

    def _extract_image_url(self, response):
        """
        Extracts the image URL from the topic page.
        """
        bs = BeautifulSoup(response.content, "html.parser")
        topic = bs.find("div", {"class": "Po_topic"})
        if topic:
            link = topic.find("a")["href"]
            if link:
                response = self._get_linked_page(link)
                if response:
                    return self._parse_image_from_page(response)
        return None

    def _get_linked_page(self, link):
        """
        Fetches the linked page containing the topic image.
        """
        response = RequestUtil().get(link, headers=headers, cookies=cookies)
        return response if response.status_code == 200 else None

    def _parse_image_from_page(self, response):
        """
        Parses the image source from the linked page.
        """
        bs = BeautifulSoup(response.content, "html.parser")
        info = bs.find("div", id="info")
        if info:
            info_cg = info.find("div", {"class": "info_cg"})
            if info_cg:
                src = info_cg.find("img")["src"]
                return src
        return None
