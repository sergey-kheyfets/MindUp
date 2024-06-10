import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Путь к JSON-ключу вашего сервисного аккаунта
KEY_PATH = 'path/to/your/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Авторизация
credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
service = build('gmail', 'v1', credentials=credentials)

# Создаем письмо
message = MIMEMultipart()
message['to'] = 'recipient@example.com'
message['subject'] = 'Тема письма'
body = 'Текст письма'
message.attach(MIMEText(body, 'plain'))
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

# Отправляем письмо
try:
    service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
    print('Письмо успешно отправлено!')
except Exception as e:
    print('Произошла ошибка:', e)
