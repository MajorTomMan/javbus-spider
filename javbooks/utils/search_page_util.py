import logging
import requests
from bs4 import BeautifulSoup
from javbus.utils.request_util import RequestUtil
from javbus.common.constants import javbooks_url

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

cookies = None  # Global cookies


class SearchPageUtil:
    logger = logging.getLogger(__name__)

    def get_topic_image(self, keyword=None):
        """
        Retrieves the topic image URL based on the given keyword.
        Handles expired cookies and retrieves new ones when necessary.
        """
        response = self._get_page(javbooks_url, keyword)
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
            self._handle_cookie_expiry(response, keyword)

        return RequestUtil().post(url, keyword, cookies=cookies) if cookies else None

    def _cookies_expired(self, response):
        """
        Checks if the cookies are expired by looking for specific HTML elements.
        """
        bs = BeautifulSoup(response.content, "html.parser")
        scale = bs.find("div", {"class": "scale_2"})
        return bool(scale)

    def _handle_cookie_expiry(self, response, keyword):
        """
        Handles the cookie expiry scenario, re-fetches cookies using DrissionPage.
        """
        global cookies
        self.logger.info("Cookies expired, attempting to fetch new cookies.")

        response = RequestUtil().get(
            "https://jkk057.com//serchinfo_censored/IamOverEighteenYearsOld/topicsbt_1.htm"
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
        response = requests.get(link, headers=headers, cookies=cookies)
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
