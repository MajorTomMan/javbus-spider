from ProxyPool import proxypool
from SearchBFS import search
from IndexBFS import index
from GenreBFS import genre
from StarBFS import stars

if __name__ == "__main__":
    baseUrl = "https://www.cdnbus.shop/"
    print(
        """
        welcome to the jav programmer
        pls select at less one choice 
        1. index
        2. search
        3. genre
        4. stars
          """
    )
    num = int(input("input:"))
    if int(num) == 1:
        is_censored = input("isCensored:")
        if is_censored == "y" or is_censored == "yes":
            print("starting censored index bfs model")
            index(baseUrl, True).BFS()
        elif is_censored == "n" or is_censored == "no":
            print("starting uncensored index bfs model")
            index(baseUrl, False).BFS()
        else:
            print("done")
    elif int(num) == 2:
        name = input("input what you want to search(only name):")
        is_censored = input("isCensored:")
        if is_censored == "y" or is_censored == "yes":
            print("starting censored search bfs model")
            search(baseUrl, name, True).BFS()
        elif is_censored == "n" or is_censored == "no":
            print("starting uncensored search bfs model")
            search(baseUrl, name, False).BFS()
        else:
            print("done")
    elif int(num) == 3:
        is_censored = input("isCensored:")
        if is_censored == "y" or is_censored == "yes":
            print("starting censored genre bfs model")
            genre(baseUrl, True).BFS()
        elif is_censored == "n" or is_censored == "no":
            print("starting uncensored genre bfs model")
            genre(baseUrl, False).BFS()
        else:
            print("done")
    elif int(num) == 4:
        is_censored = input("isCensored:")
        if is_censored == "y" or is_censored == "yes":
            print("starting censored stars bfs model")
            stars(baseUrl, True).BFS()
        elif is_censored == "n" or is_censored == "no":
            print("starting uncensored stars bfs model")
            stars(baseUrl, False).BFS()
        else:
            print("done")
