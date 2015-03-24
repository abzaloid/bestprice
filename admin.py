from google.appengine.api import users
from google.appengine.api import mail


import handler

class EmailHandler(handler.Handler):
    def get(self):
        sender_address = "Abzal Serekov"
        user_address = "aserekov@nu.edu.kz"
        subject = "Hi, from kazakhshop"
        body = "Thanks for purchasing "
        mail.send_mail(sender_address, user_address, subject, body)