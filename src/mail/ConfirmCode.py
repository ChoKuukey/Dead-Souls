import smtplib
import yaml
import string
import secrets
import sys
import os
from email.mime.text import MIMEText

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from data.dataFuncs import get_settings

from widgets.label import Label

__CHARS = string.ascii_letters + string.digits
__LENGTH = 6

__SMTP_SERVER = get_settings("../data/mail/settings.yaml")['server']
__PORT = get_settings("../data/mail/settings.yaml")['port']
__EMAIL = get_settings("../data/mail/settings.yaml")['email']
__PASSWORD = get_settings("../data/mail/settings.yaml")['password']

def generate_code() -> str:
    """ Генерация кода подтверждения """
    return "".join(secrets.choice(__CHARS) for _ in range(__LENGTH))

def send_confirm_code(email: str, error_label: Label) -> str:
    """ Отправка кода подтверждения на почту """
    sent_code = generate_code()

    try:
        server = smtplib.SMTP(__SMTP_SERVER, __PORT)
        server.starttls()
        server.ehlo()
        server.login(__EMAIL, __PASSWORD)
    except smtplib.SMTPAuthenticationError as e:
        print(f">> Не удалось подключиться к почте\n{e}")
        error_label.set_text(">> error 500")
        return

    subject = "Код подтверждения"
    message = f"Ваш код подтверждения - {sent_code}.\n\nС уважением команда Chokuukey!"

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = __EMAIL
    msg['To'] = email

    try:
        server.sendmail(__EMAIL, email, msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        print(">> Не удалось отправить код подтверждения на почту")
        error_label.set_text(">> error 500")
        return
    finally:
        print(">> Код подтверждения отправлен")
        server.quit()
        return sent_code
    