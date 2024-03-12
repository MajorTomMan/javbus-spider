import threading
import time
from GenreBFS import genre
from searchBFS import search
from IndexBFS import index
from StarBFS import stars

if __name__ == "__main__":
    baseUrl = "https://www.cdnbus.shop/"
    print(
        """
        welcome to the jav program
        pls select at less one choice 
        1. index
        2. search
        3. genre
        4. stars
          """
    )
    num = int(input("input:"))

    def run_bfs(model, is_censored):
        print(f"starting {model} BFS model")
        model(baseUrl, is_censored).BFS()

    if num == 1:
        threads = [
            threading.Thread(
                target=run_bfs, args=(index, True), name="thread_name:index/censored"
            ),
            threading.Thread(
                target=run_bfs, args=(index, False), name="thread_name:index/uncensored"
            ),
        ]
    elif num == 2:
        name = input("input what you want to search(only name):")
        threads = [
            threading.Thread(
                target=run_bfs,
                args=(search, name, True),
                name="thread_name:search/censored",
            ),
            threading.Thread(
                target=run_bfs,
                args=(search, name, False),
                name="thread_name:search/uncensored",
            ),
        ]
    elif num == 3:
        threads = [
            threading.Thread(
                target=run_bfs, args=(genre, True), name="thread_name:genre/censored"
            ),
            threading.Thread(
                target=run_bfs, args=(genre, False), name="thread_name:genre/uncensored"
            ),
        ]
    elif num == 4:
        threads = [
            threading.Thread(
                target=run_bfs, args=(stars, True), name="thread_name:stars/censored"
            ),
            threading.Thread(
                target=run_bfs, args=(stars, False), name="thread_name:stars/uncensored"
            ),
        ]

    for thread in threads:
        # 在第一个线程之外，等待前一个线程至少20秒,防止瘫痪对方服务器而察觉爬虫
        if thread != threads[0]:
            time.sleep(20)
        thread.start()
    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("All threads have finished.")
