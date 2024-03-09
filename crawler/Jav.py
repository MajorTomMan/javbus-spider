from ProxyPool import proxypool
from SearchBFS import search
from IndexBFS import index
from GenreBFS import GenreBFS


if __name__ == "__main__":
    baseUrl = "https://www.cdnbus.shop/"
    print(
        """
        welcome to the jav programmer
        pls select at less one choice 
        1. index
        2. search
        3. getProxyIp
        4. queryGenre
          """
    )
    num = int(input("input:"))
    if int(num) == 1:
        print("starting index bfs model")
        index(baseUrl).BFS()
    elif int(num) == 2:
        name = input("input what you want to search(only name):")
        print("starting search bfs model")
        search(baseUrl, name).BFS()
    elif int(num) == 3:
        print("starting proxy ip")
        proxypool().getPageList()
    elif int(num) == 4:
        print("querying genre bfs model")
        GenreBFS(baseUrl).BFS()
