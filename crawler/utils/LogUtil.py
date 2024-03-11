import datetime
import traceback
from utils.MailUtil import MailUtil


class LogUtil:
    logPath = "./spider.log"
    mailUtil = MailUtil()

    def log(self, log):
        if log:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 判断传入实参是否是对象类型
            if isinstance(log, Exception):
                log = f"Exception: {str(log)}\n"
            elif hasattr(log, "__dict__"):
                log = log.__dict__
            with open(self.logPath, "a", encoding="utf-8") as file:
                self.log_recursive(log, current_time, file)

    def log_recursive(self, obj, current_time, file=None, indent=0, parent_key=None):
        if isinstance(obj, dict):
            for k, v in obj.items():
                self.log_recursive(
                    v,
                    current_time,
                    file,
                    indent + 1,
                    parent_key=f"{parent_key}.{k}" if parent_key else k,
                )
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self.log_recursive(
                    item,
                    current_time,
                    file,
                    indent + 1,
                    parent_key=f"{parent_key}[{i}]" if parent_key else f"[{i}]",
                )
        else:
            key_info = f"{parent_key}:" if parent_key else ""
            log_entry = f"[{current_time}] {key_info}{str(obj)}\n"
            print(log_entry)
            if file:
                file.write(log_entry)
