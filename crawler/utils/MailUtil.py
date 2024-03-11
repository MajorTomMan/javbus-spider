import smtplib

# 构建邮件
from email.header import Header
from email.mime.text import MIMEText


class MailUtil:
    emailPath = "./email.txt"
    email = None
    mail = None
    server = "smtp.qq.com"
    port = 587
    email_from = "python spider"
    msg = None

    def send(cls, content, times):
        subject = f"Spider Error - {times}"
        body = f"Some exception occurred in the spider.\n\n{content}"
        if cls.email is None:
            cls.getEmailInfo(content, subject)
            try:
                with smtplib.SMTP(cls.server, cls.port) as client:
                    client.starttls()
                    client.login(cls.email["To"], cls.email["password"])
                    client.sendmail(
                        cls.email["To"], cls.email["To"], cls.msg.as_string()
                    )
            except Exception as e:
                print(e)

    def getEmailInfo(cls, content, subject):
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        cls.email = {}
        try:
            with open(cls.emailPath, "r") as file:
                for line in file:
                    # 去除行末尾的换行符，并使用等号分割键值对
                    line = line.strip()
                    key, value = line.split("=")
                    # 将键值对添加到字典
                    cls.email[key] = value
            cls.email["To"] = cls.email["account"]
            cls.msg = msg
        except FileNotFoundError as e:
            print(e)
            print("email info file not found")
