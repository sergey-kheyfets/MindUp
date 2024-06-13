import imaplib
#
# Учетные данные для подключения к почте Gmail
email = 'mind777up777noreply@gmail.com'
password = 'mindup777mindup'

# Подключение к почте Gmail через IMAP
mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login(email, password)


"""import imaplib
#
# Учетные данные для подключения к почте Gmail
email = 'mindup@tutamail.com'
password = 'mind777up777noreply'
# password = 'mindup777mindup'

# Подключение к почте Gmail через IMAP
#mail = imaplib.IMAP4_SSL('imap.app.tuta.com')
#print(1)
#mail.login(email, password)
#print(1)
import smtplib
smtpObj = smtplib.SMTP('smtp.app.tuta.com', 587)
smtpObj.starttls()
smtpObj.login(email,password)
smtpObj.sendmail(email, "ilyarybin2018@gmail.com", "go to bed!")"""