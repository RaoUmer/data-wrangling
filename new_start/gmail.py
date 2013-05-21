import smtplib
from email.MIMEMultipart import MIMEMultipart
# from email.MIMEBase import MIMEBase  # For attachments
from email.MIMEText import MIMEText
# from email import Encoders
import os


def get_info():
    with open(os.environ["HOME"] + '/.google_file') as f:
        for line in f:
            k, v = line.split(':')
            if k == 'google_pw':
                gmail_pwd = v
            else:
                gmail_user = v
    return gmail_user, gmail_pwd


def mail(to, subject, text, attach=None):
    gmail_user, gmail_pwd = get_info()
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
