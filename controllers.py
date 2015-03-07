import webapp2
import json
import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import mail


import handler
import caching

### CONTROLLERS ###
class MainPage(handler.Handler):
    """ This is the main page which uses server-side templating
    to display all items. Use this in emergency by changing routing 
    mappings. Currently mapped to /mainpage"""
    def get(self):
        #tshirts = get_tshirts(update = True)
        items = list(caching.get_items())
        items = items[:20]
        categories = list(caching.get_categories())
        item_cart = self.session.get('items')
        self.render("main.html", items=items, items_size=len(items)-1, categories=categories, item_cart=item_cart)

class AnotherMainPage(handler.Handler):
    """ This is the main page which uses client-side handlebars 
    for templating. Currently mapped to /"""
    def get(self):
        self.render("main2.html")


class LoginHandler(handler.Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.session["item_count"] = 0
            self.session["add_to_cart_count"] = 0
            self.session["items"] = {}
            self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ShowItemHandler(handler.Handler):
    def get(self, item_id):
        tshirt = caching.get_one_tshirt(item_id)
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
