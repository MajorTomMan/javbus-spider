import requests

from javbus.utils.log_util import LogUtil


class IpUtil:
    target_url = "http://httpbin.org/get"
    logUtil = LogUtil()

    def getProxy(self):
        ip = requests.get("http://localhost:5555/random").text.strip()
        while self.checkIsGood(ip) == False:
            ip = requests.get("http://localhost:5555/random").text.strip()
        return ip

    def checkIsGood(self, ip):
        proxies = {"https": "https://" + ip}
        response = requests.get(self.target_url, proxies=proxies)
        origin_address = response.json()["origin"]
        proxy_ip = ip.split(":")[0]
        if origin_address == proxy_ip and response.status_code == 200:
            self.logUtil.log(proxy_ip + " was be undetected,choice")
            return True
        self.logUtil.log(proxy_ip + " was be detected,abandon")
        return False
