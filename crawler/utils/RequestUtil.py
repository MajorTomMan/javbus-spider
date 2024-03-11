import requests

from utils.LogUtil import LogUtil


class RequestUtil:
    baseUrl = "http://localhost:8080"
    headers = {"Content-Type": "application/json"}
    logUtil = LogUtil()

    def post(self, data, path):
        try:
            return requests.post(url=self.baseUrl + path, json=data)
        except ConnectionError as connectionError:
            self.logUtil.log(connectionError)
        except TimeoutError as timeoutError:
            self.logUtil.log(timeoutError)
        except Exception as e:
            self.logUtil.log(e)

    def get(self, path):
        try:
            return requests.get(self.baseUrl + path)
        except ConnectionError as connectionError:
            self.logUtil.log(connectionError)
        except TimeoutError as timeoutError:
            self.logUtil.log(timeoutError)
        except Exception as e:
            self.logUtil.log(e)
