import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('mind777up777noreply@gmail.com','mindup777mindup')
smtpObj.sendmail("mind777up777noreply@gmail.com", "ilyarybin2018@gmail.com", "go to bed!")
