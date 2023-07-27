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
        server.sendmail(MAIL_ADDRESS, MAIL_RECEIVER, "hi")


def receive_mail():
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context) as server:
        server.login(MAIL_ADDRESS, MAIL_PASSWORD)
        server.select("INBOX")
        status, messages = server.search(None, 'ALL')
        if status == 'OK' and messages[0]:
            message_numbers = messages[0].split()
            last_message_number = message_numbers[-1]
            # Fetch the last message
            status, msg_data = server.fetch(last_message_number, '(RFC822)')
            if status == 'OK':
                return msg_data[0][1].decode()
            # Close the connection
        mail.logout()


def parse_link(message):
    pattern = r"hdrezka[a-z0-9]+\.org"
    match = re.search(pattern, message)
    if match:
        link = match.group()
        return link


if __name__ == '__main__':
    send_mail()
    time.sleep(3)
    mail = receive_mail()
    hd_link = parse_link(mail)
    print(hd_link)
