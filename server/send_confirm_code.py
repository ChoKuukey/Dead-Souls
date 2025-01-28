import smtplib
import sys
import os
import yaml
from email.mime.text import MIMEText
import os

here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, "D:/Programming/Python\Dead-Souls/server/mail_conf.yaml")

mail_conf = "D:/Programming/Python\Dead-Souls/server/mail_conf.yaml"

def get_settings(src: str) -> dict:
    try:
        with open(src, 'r') as settings_file:
            content = settings_file.read()
            # print("YAML file content:\n", content)  # Debugging output
            settings = yaml.load(content, Loader=yaml.FullLoader)
            if not settings:
                raise ValueError("YAML file is empty or not properly formatted.")
            return settings
    except FileNotFoundError:
        print(f"Error: The file '{src}' was not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")
    except ValueError as ve:
        print(f"Error: {ve}")
    return {}

__SMTP_SERVER = get_settings(mail_conf)['server']
__PORT = get_settings(mail_conf)['port']
__EMAIL = get_settings(mail_conf)['email']
__PASSWORD = get_settings(mail_conf)['password']

def main(email: str, code: str) -> str:
    """ Отправка кода подтверждения на почту """
    try:
        server = smtplib.SMTP(__SMTP_SERVER, __PORT)
        server.starttls()
        server.ehlo()
        server.login(__EMAIL, __PASSWORD)
    except smtplib.SMTPAuthenticationError as e:
        print(f">> Не удалось подключиться к почте\n{e}")
        return

    subject = "Код подтверждения"
    message = f"Ваш код подтверждения - {code}.\n\nС уважением команда Chokuukey!"

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = __EMAIL
    msg['To'] = email

    try:
        server.sendmail(__EMAIL, email, msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        print(">> Не удалось отправить код подтверждения на почту")
        return
    finally:
        print(">> Код подтверждения отправлен")
        server.quit()
    

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])