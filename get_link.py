import datetime
import json
import re
import smtplib
import ssl
import imaplib
import time
from settings import MAIN_CONFIG

SMTP_HOST = MAIN_CONFIG['SMTP_HOST']
SMTP_PORT = MAIN_CONFIG['SMTP_PORT']
IMAP_HOST = MAIN_CONFIG['IMAP_HOST']
IMAP_PORT = MAIN_CONFIG['IMAP_PORT']
MAIL_ADDRESS = MAIN_CONFIG['MAIL_ADDRESS']
MAIL_PASSWORD = MAIN_CONFIG['MAIL_PASSWORD']
MAIL_RECEIVER = MAIN_CONFIG['MAIL_RECEIVER']


def send_mail():
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(MAIL_ADDRESS, MAIL_PASSWORD)
        logs = server.sendmail(MAIL_ADDRESS, MAIL_RECEIVER, "hi!")
        print(logs)


def receive_mail():
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context) as server:
        server.login(MAIL_ADDRESS, MAIL_PASSWORD)
        server.select("INBOX")
        for _ in range(5):
            status, messages = server.search(None, 'UNSEEN')
            if status == 'OK' and messages[0]:
                message_numbers = messages[0].split()
                last_message_number = message_numbers[-1]
                status, msg_data = server.fetch(last_message_number, '(RFC822)')
                if status == 'OK':
                    return msg_data[0][1].decode()
            time.sleep(2)


def parse_link(message):
    pattern = r"hdrezka[a-z0-9]+\.org"
    match = re.search(pattern, message)
    if match:
        link = match.group()
        return link


if __name__ == '__main__':
    send_mail()
    mail = receive_mail()
    if mail:
        hd_link = parse_link(mail)
        json.dump({'link': hd_link, 'time': int(time.time())}, open('link.json', 'w'), indent=4)
    print('null')
