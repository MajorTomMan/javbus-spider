import os
import concurrent.futures
import queue
from Genre import genre
from Search import search
from Index import index
from Actress import actresses
import atexit

q = queue.Queue()


def cleanChromeDriver():
    try:
        os.system("taskkill /F /im chromedriver.exe")
        os.system("taskkill /F /im undetected_chromedriver.exe")
        os.system("taskkill /F /im chrome.exe")
        os.system("taskkill /F /im python.exe")
    except TypeError as e:
        pass


def run_bfs(model, keyword, is_censored):
    print(f"starting {model} BFS model")
    if keyword:
        model(baseUrl, keyword).BFS()
    else:
        model(baseUrl, is_censored).BFS()


def queue_worker():
    while True:
        item = q.get()
        if item is None:
            break
        model, keyword, is_censored = item
        run_bfs(model, keyword, is_censored)
        q.task_done()


if __name__ == "__main__":
    keywords = [
        "北野未奈",
        "Rion",
        "大橋未久",
        "藤森里穂",
        "安齋らら",
        "吉沢明歩",
        "メロディー・雛・マークス",
        "星宮一花",
    ]
    baseUrl = "https://www.cdnbus.shop/"

    print(
        """
        welcome to the jav program
        pls select at less one choice 
        1. index
        2. search
        3. genre
        4. actress
        5. startAllThread
        """
    )
    while True:
        try:
            num = int(input("input:"))

            if num in range(1, 6):
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    if num == 1:
        tasks = [
            (index, None, True),
            (index, None, False),
        ]
    elif num == 2:
        keyword = input("input what keyword you want to search:")
        tasks = [
            (search, keyword, True),
        ]
    elif num == 3:
        tasks = [
            (genre, None, True),
            (genre, None, False),
        ]
    elif num == 4:
        tasks = [
            (actresses, None, True),
            (actresses, None, False),
        ]
    elif num == 5:
        tasks = [
            (index, None, True),
            (index, None, False),
            (genre, None, True),
            (genre, None, False),
            (actresses, None, True),
            (actresses, None, False),
        ]
        for keyword in keywords:
            tasks.append((search, keyword, True))

    # 创建ThreadPoolExecutor，设置最大并发线程数为5
    with concurrent.futures.ThreadPoolExecutor(max_workers=3,thread_name_prefix="jav-thread") as executor:
        # 提交任务给线程池执行
        for task in tasks:
            executor.submit(run_bfs, *task)

    print("All tasks have been submitted to the thread pool.")
    print("Waiting for all tasks to complete...")

    # 等待队列中的任务完成
    q.join()

    print("All threads have finished.")
    print("exec clean operation")
    atexit.register(cleanChromeDriver)
