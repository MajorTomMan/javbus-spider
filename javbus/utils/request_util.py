import random
from curl_cffi import requests
import logging
from javbus.common.constants import server_url
# 创建日志记录器
logger = logging.getLogger(__name__)


class RequestUtil:
    baseUrl = "http://"+server_url+"/api"
    # baseUrl = "http://localhost:9999"
    headers = {"Content-Type": "application/json"}
    image_headers = {"Content-Type": "image/jpeg"}
    magnet_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5",
        "cookie": "PHPSESSID=27pp7v8mq4sho8mnodel9q4m72; existmag=mag",
        "priority": "u=1, i",
        "referer": "",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    def __init__(self):
        self.session = requests.Session()  # 使用 Session 复用连接，提高效率

    def get(self, url):
        try:
            response = self.session.get(url,impersonate="chrome",timeout=3)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in GET request to {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GET request: {str(e)}")

    def post_to_server(self, data, path=None):
        if path:
            url = self.baseUrl + path
        else:
            url = self.baseUrl
        try:
            response = self.session.post(
                url, json=data, headers=self.headers, impersonate="chrome", timeout=3
            )
            response.raise_for_status()  # 触发异常以捕获 HTTP 错误
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in POST request to {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in POST request: {str(e)}")

    def post(self, url, data, cookies=None):
        try:
            if cookies:
                response = self.session.post(
                    url, data=data, cookies=cookies, impersonate="chrome", timeout=3
                )
            else:
                response = self.session.post(
                    url, data=data, impersonate="chrome", timeout=3
                )
            response.raise_for_status()  # 触发异常以捕获 HTTP 错误
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in POST request to {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in POST request: {str(e)}")

    def send(self, data, path):
        response = self.post_to_server(data=data, path=path)
        if not response:
            logger.error(f"Error sending data to {path}. Check server status or logs.")
            logger.error(f"Data: {data}")
        elif response.status_code == 200:
            logger.info(f"Successfully sent data to {path}")
        else:
            logger.warning(f"Failed to send data to {path}")
            logger.warning(
                f"Status Code: {response.status_code}, Reason: {response.reason}"
            )
            logger.warning(f"Response Body: {response.text}")

    def request_magnets(self, base_url, gid, img, uc, referer):
        url = (
            base_url
            + f"/ajax/uncledatoolsbyajax.php?gid={gid}&lang=zh&img={img}&uc={uc}&floor={random.randint(1, 1000)}"
        )
        if referer:
            self.magnet_headers["referer"] = referer
        try:
            response = requests.get(url=url,impersonate="chrome",headers=self.magnet_headers,timeout=3)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            logger.error(f"request failed with: {error}")
