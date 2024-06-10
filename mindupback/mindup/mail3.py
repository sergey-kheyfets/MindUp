import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Введите свои данные для входа в почту Gmail
email = 'mind777up777noreply@gmail.com'
password = 'mindup777mindup'

# Создаем объект для отправки писем
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(email, password)

# Создаем письмо
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = "recipient@example.com"
msg['Subject'] = "Тема письма"

body = "Текст письма"
msg.attach(MIMEText(body, 'plain'))

# Отправляем письмо
server.send_message(msg)

# Закрываем соединение
server.quit()