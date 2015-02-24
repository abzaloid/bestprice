from google.appengine.api import users
from google.appengine.api import mail


import cashing
import handler
import models

### ADMIN FUNCTIONS ### - Not protected currently
class AddItemHandler(handler.Handler):
    def get(self):
        self.render("items_form.html")

    def post(self):
        self.item_id = self.request.get('item_id')
        self.item_title = self.request.get('title')
        self.item_price = self.request.get('price')
        self.item_content = self.request.get('content')
        
        t = models.Tshirt(tshirt_id = int(self.item_id), 
                   title = self.item_title, 
                   price = int(self.item_price), 
                   content = self.item_content)
        t.put()
        self.redirect('/item/add')

class EditItemHandler(handler.Handler):
    def get(self):
        tshirts = cashing.get_tshirts()
        self.render("items_form.html", tshirts = tshirts)

    def post(self):
        self.item_id = self.request.get('item_id')
        self.item_title = self.request.get('title')
        self.item_price = self.request.get('price')
        self.item_content = self.request.get('content')

        tshirt = models.Tshirt.all().filter("tshirt_id =", int(self.item_id)).get()
        tshirt.title = self.item_title
        tshirt.content = self.item_content
        tshirt.price = int(self.item_price)

        tshirt.put()
        self.redirect('/item/edit')

class EmailHandler(handler.Handler):
    def get(self):
        sender_address = "prakhar1989@gmail.com"
        user_address = "kumarar2013@iimcal.ac.in"
        subject = "Hi, from Jokastore"
        body = "Thanks for purchasing from Jokastore"
        mail.send_mail(sender_address, user_address, subject, body)