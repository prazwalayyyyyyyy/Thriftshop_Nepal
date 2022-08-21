import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()
gmail_user = os.environ["SMTP_EMAIL"] 
gmail_password = os.environ["SMTP_PASSWORD"]# 'fuybuzodriwskbnf'
SMTP_SERVER='smtp.gmail.com'
msg=MIMEMultipart()

def send_email(to, msg, subject):
    """sends an email 
    """
   
    by = ' <%s>' % "thriftshop@thriftshop.com"
    msg['Subject'] = subject
    msg['From'] = by
    msg['To'] = ",".join(to)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        # server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(by, to, msg.as_string())
        server.close()
    except smtplib.SMTPException as e:
        print(e)

    return True


if __name__ == '__main__':
    to = ["@gmail.com"]
    html="<p> Hello </p>"
    msg.attach(MIMEText(html,'html'))
    subject= "keraaa is imported"
    send_email(to, msg, subject)