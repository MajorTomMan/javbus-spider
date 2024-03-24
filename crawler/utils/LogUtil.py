import datetime
from utils.MailUtil import MailUtil
import threading
import traceback


class LogUtil:
    logPath = "./spider.log"
    mailUtil = MailUtil()
    lock = threading.Lock()

    def log(self, log, log_file_path="./spider.log"):
        if log:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            thread_name = threading.current_thread().name
            # 判断传入实参是否是对象类型
            if isinstance(log, Exception):
                log = f"Exception: {str(log)}\n" + f"stack:{traceback.format_exc()}"
                self.mailUtil.send_email(log)
            elif hasattr(log, "__dict__"):
                log = log.__dict__
            with self.lock:  # 使用锁确保多线程环境下的安全性
                with open(log_file_path, "a", encoding="utf-8") as file:
                    self.log_recursive(log, current_time, thread_name, file)

    def log_recursive(
        self, obj, current_time, thread_name, file=None, indent=0, parent_key=None
    ):
        if isinstance(obj, dict):
            for k, v in obj.items():
                self.log_recursive(
                    v,
                    current_time,
                    thread_name,
                    file,
                    indent + 1,
                    parent_key=f"{parent_key}.{k}" if parent_key else k,
                )
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self.log_recursive(
                    item,
                    current_time,
                    thread_name,
                    file,
                    indent + 1,
                    parent_key=f"{parent_key}[{i}]" if parent_key else f"[{i}]",
                )
        else:
            key_info = f"{parent_key}:" if parent_key else ""
            log_entry = f"[{current_time}] [{thread_name}] {key_info}{str(obj)}\n"
            print(log_entry)
            if file:
                file.write(log_entry)
