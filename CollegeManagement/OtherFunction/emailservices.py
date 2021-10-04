import smtplib
def sendMail(message,reciever,sender,password):
    try:
        session=smtplib.SMTP('smtp.gmail.com',587)
        session.starttls()
        session.login(sender,password)
        session.sendmail(sender,reciever,message)
        session.quit()
        session.close()
    except Exception as e:
        print(e)