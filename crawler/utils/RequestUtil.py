import requests

from utils.LogUtil import LogUtil

requests.packages.urllib3.disable_warnings()


class RequestUtil:
    baseUrl = "http://101.43.91.110:7788/spider"
    headers = {"Content-Type": "application/json"}
    logUtil = LogUtil()
    image_headers = {"Content-Type": "image/jpeg"}

    def post(self, data, path):
        try:
            return requests.post(url=self.baseUrl + path, json=data)
        except ConnectionError as connectionError:
            self.logUtil.log(connectionError)
        except TimeoutError as timeoutError:
            self.logUtil.log(timeoutError)
        except Exception as e:
            self.logUtil.log(e)

    def postImage(self, data, path, filename):
        try:
            return requests.post(
                url=self.baseUrl + path + "/" + filename,
                data=data,
                headers=self.image_headers,
            )
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
            self.logUtil.log("error request to " + path, "./errorRequestServer.log")
            self.logUtil.log("error data is " + data, "./errorRequestServer.log")
            self.logUtil.log(
                "request not response pls check server is open or has expection "
            )
        elif response.status_code == 200:
            self.logUtil.log("send data to " + path + " was success")
        else:
            self.logUtil.log("send data to " + path + " was failure")

    def sendImage(self, data, path, filename):
        response = self.postImage(data=data, path=path, filename=filename)
        if not response:
            self.logUtil.log("error request to " + path, "./errorRequestServer.log")
            self.logUtil.log("error data is ", "./errorRequestServer.log")
            self.logUtil.log(data, "./errorRequestServer.log")
            self.logUtil.log(
                "request not response pls check server is open or has expection "
            )
        elif response.status_code == 200:
            self.logUtil.log("send data to " + path + " was success")
        else:
            self.logUtil.log("send data to " + path + " was failure")
