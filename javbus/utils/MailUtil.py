import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailUtil:
    username = "765719516@qq.com"
    password = "jtsrxuvmtnafbecc"
    subject = "message from spider"

    def send_email(self, message):
        # 创建邮件对象
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = self.username
        msg["Subject"] = self.subject

        # 添加邮件正文
        msg.attach(MIMEText(message, "plain"))

        # 建立与 Gmail SMTP 服务器的连接
        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.ehlo()
            server.login(self.username, self.password)
        except Exception as e:
            print("Failed to connect to qq SMTP server:", e)
            return False
        # 发送邮件
        try:
            server.sendmail(self.username, self.username, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)
            return False
        finally:
            # 关闭连接
            server.quit()

        return True
