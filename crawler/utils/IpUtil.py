import requests


class IpUtil:
    def getProxy(self):
        return requests.get("http://127.0.0.1:5010/get/").json()
