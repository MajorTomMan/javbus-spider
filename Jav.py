
from IndexBFS import index


if __name__=="__main__":
    baseUrl="https://www.javbus.com/"
    print("""
        welcome to the jav programmer
        pls select at less one choice 
        1. index
        2. search
          """)
    num=int(input("input:"))
    if int(num)==1:
        print("starting index bfs model")
        index(baseUrl).BFS()
    elif int(num)==2:
        print("starting search bfs model")