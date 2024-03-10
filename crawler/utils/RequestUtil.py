import requests


class RequestUtil:
    baseUrl = "http://localhost:8080"
    headers = {"Content-Type": "application/json"}

    def post(self, data, path):
        return requests.post(url=self.baseUrl + path, json=data)

    def get(self, path):
        return requests.get(self.baseUrl + path)
