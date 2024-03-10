import requests


class RequestUtil:
    baseUrl = "http://localhost:8080"
    headers = {"Content-Type": "application/json"}

    def post(self, data, path):
        try:
            return requests.post(url=self.baseUrl + path, json=data)
        except ConnectionError as connectionError:
            print(connectionError)
        except TimeoutError as timeoutError:
            print(timeoutError)
        except Exception as e:
            print(e)

    def get(self, path):
        try:
            return requests.get(self.baseUrl + path)
        except ConnectionError as connectionError:
            print(connectionError)
        except TimeoutError as timeoutError:
            print(timeoutError)
        except Exception as e:
            print(e)
