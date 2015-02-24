

import os
import sys
import webapp2
import json
import jinja2
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import mail


import databaseOperations
import search
import handler
import models

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
### Configuration ###
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}



### CACHING ###
def get_tshirts(update = False):
    key = "tee"
    tshirts = memcache.get(key)
    if tshirts is None or update:
        logging.error("DB QUERY FOR TSHIRTS")
        tshirts = db.GqlQuery("SELECT * FROM Tshirt ORDER BY tshirt_id")
        tshirts = list(tshirts)
        memcache.set(key, tshirts)
    return tshirts

def get_one_tshirt(item_id, update = False):
    key = item_id 
    tshirt = memcache.get(key)
    if tshirt is None or update:
        logging.error("DB QUERY FOR SINGLE TSHIRT")
        tshirt = Tshirt.all().filter("tshirt_id =", int(item_id)).get()
        memcache.set(key, tshirt)
    return tshirt

### CONTROLLERS ###
class MainPage(handler.Handler):
    """ This is the main page which uses server-side templating
    to display all items. Use this in emergency by changing routing 
    mappings. Currently mapped to /mainpage"""
    def get(self):
        #tshirts = get_tshirts(update = True)
        self.render("main.html")#, tshirts = tshirts)

class AnotherMainPage(handler.Handler):
    """ This is the main page which uses client-side handlebars 
    for templating. Currently mapped to /"""
    def get(self):
        self.render("main2.html")


class JSONHandler(handler.Handler):
    def get(self):
        tshirts = get_tshirts(True)
        self.response.headers['Content-type'] = 'application/json'
        tshirt_json = []
        for t in tshirts:
            tshirt_json.append({"id": t.tshirt_id, "title": t.title})
        self.write(json.dumps(tshirt_json))

class LoginHandler(handler.Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.session["item_count"] = 0
            self.session["add_to_cart_count"] = 0
            self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ShowItemHandler(handler.Handler):
    def get(self, item_id):
        tshirt = get_one_tshirt(item_id)
        self.render("show_tshirt.html", tshirt = tshirt)

class AboutHandler(handler.Handler):
    def get(self):
        self.render("about.html")

class SecureHandler(handler.Handler):
    def get(self):
        if users.get_current_user():
            self.write("Welcome to secure page. session value= %s" % self.session.get("foo"))
        else:
            self.write("you need to login to see this page")

class LogoutHandler(handler.Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.redirect(users.create_logout_url('/'))

class AddToCartHandler(handler.Handler):
    def get(self):
        if users.get_current_user():
            self.response.headers['Content-type'] = 'application/json'
            get_current_add_count = int(self.session.get('add_to_cart_count'))
            tshirt_id = self.request.get("tshirt_id")
            item_title = self.request.get("item_title")
            qty = self.request.get("qty")
            size = self.request.get("size")
            price = 325
            get_current_add_count += 1
            self.session[get_current_add_count] = { "qty" : qty, "size" : size ,
                                                    "item_title": item_title, 
                                                    "tshirt_id" : tshirt_id,
                                                    "cost" : price * int(qty)}

            current_cart_items = int(self.session.get("item_count"))
            updated_cart_items = current_cart_items + int(qty)
            self.session["item_count"] = updated_cart_items
            self.session["add_to_cart_count"] = get_current_add_count
            self.write(json.dumps({"status" : 1, "msg" : "Order added. <a href='/cart'><span class='label label-success'>View Cart</span></a>"}))
        else:
            self.write(json.dumps({"status" : 0, "msg" : "Please <a href='/login'><span class='label label-important'>login</span> </a>to start shopping!"}))


class CartHandler(handler.Handler):
    def get(self):
        item_list = self.get_items_from_cart()
        self.render('show_cart.html', item_list = item_list)

class CheckoutHandler(handler.Handler):
    def get(self):
        item_list = self.get_items_from_cart()
        user = users.get_current_user()
        if user:
            user_email = user.email()
            if item_list:
                for i in item_list:
                    order = Order(qty = int(i["qty"]), 
                                  user_email = user_email,
                                  size = i["size"],
                                  tshirt_id = int(i["tshirt_id"]))
                    order.put()
                    logging.error("Attempt to put in database")
            else:
                logging.error("Updation to Order Model missed")
        else:
            self.redirect('/')
        logging.error("Order Added for user: %s" % user.email())
        self.session["add_to_cart_count"] = 0
        self.redirect('/done')

class DoneHandler(handler.Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.write("Your order has been recorded. You shortly hear from us regarding payment and delivery details. Thanks for ordering. <a href='/'>Continue shopping</a>")
        
### ADMIN FUNCTIONS ### - Not protected currently
class AddItemHandler(handler.Handler):
    def get(self):
        self.render("items_form.html")

    def post(self):
        self.item_id = self.request.get('item_id')
        self.item_title = self.request.get('title')
        self.item_price = self.request.get('price')
        self.item_content = self.request.get('content')
        
        t = Tshirt(tshirt_id = int(self.item_id), 
                   title = self.item_title, 
                   price = int(self.item_price), 
                   content = self.item_content)
        t.put()
        self.redirect('/item/add')

class EditItemHandler(handler.Handler):
    def get(self):
        tshirts = get_tshirts()
        self.render("items_form.html", tshirts = tshirts)

    def post(self):
        self.item_id = self.request.get('item_id')
        self.item_title = self.request.get('title')
        self.item_price = self.request.get('price')
        self.item_content = self.request.get('content')

        tshirt = Tshirt.all().filter("tshirt_id =", int(self.item_id)).get()
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


class ListOrdersHandler(handler.Handler):
    def get(self):
        orders = db.GqlQuery("SELECT * FROM Order ORDER BY time_of_order")
        self.response.headers['Content-type'] = 'text/plain'
        self.render("list_orders.html", orders = orders)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/logout', LogoutHandler),
                               ('/login', LoginHandler), 
                               ('/item/add', AddItemHandler), 
                               ('/item/edit', EditItemHandler), 
                               ('/cart/add', AddToCartHandler),
                               ('/about', AboutHandler),
                               ('/done', DoneHandler),
                               ('/mainpage', MainPage),
                               ('/cart', CartHandler),
                               ('/all.json', JSONHandler),
                               ('/checkout', CheckoutHandler),
                               ('/sendmail', EmailHandler),
                               ('/listorders', ListOrdersHandler),
                               ('/secure', SecureHandler),
                               ('/tshirt/(\d+)', ShowItemHandler),
                               ('/update_database', databaseOperations.UpdateDatabase),
                               ('/show_database', databaseOperations.ShowDatabase),
                               ('/search', search.SearchItem)], config=config, debug=True)
