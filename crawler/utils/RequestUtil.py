import requests

from utils.LogUtil import LogUtil


class RequestUtil:
    baseUrl = "http://localhost:7788"
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

    def send(self, data, path):
        response = self.post(data=data, path=path)
        if not response:
            self.logUtil.log(
                "request not response pls check server is open or has expection "
            )
        elif response.status_code == 200:
            self.logUtil.log("send data to " + path + " was success")
        else:
            self.logUtil.log("send data to " + path + " was failure")
