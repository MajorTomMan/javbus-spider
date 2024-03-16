import threading
import time
from GenreBFS import genre
from SearchBFS import search
from IndexBFS import index
from ActressBFS import actresses

if __name__ == "__main__":
    baseUrl = "https://www.cdnbus.shop/"
    print(
        """
        welcome to the jav program
        pls select at less one choice 
        1. index
        2. search
        3. genre
        4. actress
          """
    )
    num = int(input("input:"))

    def run_bfs(model, keyword, is_censored):
        print(f"starting {model} BFS model")
        if keyword:
            model(baseUrl, keyword, is_censored).BFS()
        else:
            model(baseUrl, is_censored).BFS()

    if num == 1:
        threads = [
            threading.Thread(
                target=run_bfs,
                args=(index, None, True),
                name="thread_name:index/censored",
            ),
            threading.Thread(
                target=run_bfs,
                args=(index, None, False),
                name="thread_name:index/uncensored",
            ),
        ]
    elif num == 2:
        keyword = input("input what keyword you want to search:")
        threads = [
            # threading.Thread(
            #    target=run_bfs,
            #    args=(search, keyword, True),
            #    name="thread_name:search/censored",
            # ),
            threading.Thread(
                target=run_bfs,
                args=(search, keyword, False),
                name="thread_name:search/uncensored",
            ),
        ]
    elif num == 3:
        threads = [
            threading.Thread(
                target=run_bfs,
                args=(genre, None, True),
                name="thread_name:genre/censored",
            ),
            threading.Thread(
                target=run_bfs,
                args=(genre, None, False),
                name="thread_name:genre/uncensored",
            ),
        ]
    elif num == 4:
        threads = [
            threading.Thread(
                target=run_bfs,
                args=(actresses, None, True),
                name="thread_name:actresses/censored",
            ),
            threading.Thread(
                target=run_bfs,
                args=(actresses, None, False),
                name="thread_name:actresses/uncensored",
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
