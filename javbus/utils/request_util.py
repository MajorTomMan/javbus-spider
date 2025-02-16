import random
import requests
import scrapy


class RequestUtil:
    baseUrl = "http://localhost:7788"
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

    def post(self, data, path, is_image=False):
        url = self.baseUrl + path
        headers = self.image_headers if is_image else self.headers

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()  # 触发异常以捕获 HTTP 错误
            return response
        except requests.exceptions.RequestException as e:
            scrapy.scrapy.logger.error(f"Error in POST request to {url}: {str(e)}")
        except Exception as e:
            scrapy.logger.error(f"Unexpected error in POST request: {str(e)}")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            scrapy.logger.error(f"Error in GET request to {url}: {str(e)}")
        except Exception as e:
            scrapy.logger.error(f"Unexpected error in GET request: {str(e)}")

    def send(self, data, path, is_image=False):
        response = self.post(data=data, path=path, is_image=is_image)
        if not response:
            scrapy.logger.error(
                f"Error sending data to {path}. Check server status or logs."
            )
            scrapy.logger.error(f"Data: {data}")
        elif response.status_code == 200:
            scrapy.logger.info(f"Successfully sent data to {path}")
        else:
            scrapy.logger.warning(f"Failed to send data to {path}")
            scrapy.logger.warning(
                f"Status Code: {response.status_code}, Reason: {response.reason}"
            )
            scrapy.logger.warning(f"Response Body: {response.text}")

    def sendImage(self, data, path):
        self.send(data, path, is_image=True)

    def sendMangets(self, base_url, gid, img, uc, referer):
        url = (
            base_url
            + f"/ajax/uncledatoolsbyajax.php?gid={gid}&lang=zh&img={img}&uc={uc}&floor={random.randint(1, 1000)}"
        )
        if referer:
            self.magnet_headers["referer"] = referer
        try:
            response = requests.get(
                url=url,
                headers=self.magnet_headers,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            scrapy.logger.error(f"请求失败: {error}")
            return None
