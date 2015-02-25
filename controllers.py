import webapp2
import json
import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import mail


import handler
import cashing

### CONTROLLERS ###
class MainPage(handler.Handler):
    """ This is the main page which uses server-side templating
    to display all items. Use this in emergency by changing routing 
    mappings. Currently mapped to /mainpage"""
    def get(self):
        #tshirts = get_tshirts(update = True)
        items = list(db.GqlQuery("SELECT * FROM Item"))
        self.render("main.html", items = items[:20], items_size = len(items[:20])-1)#, tshirts = tshirts)

class AnotherMainPage(handler.Handler):
    """ This is the main page which uses client-side handlebars 
    for templating. Currently mapped to /"""
    def get(self):
        self.render("main2.html")


class JSONHandler(handler.Handler):
    def get(self):
        tshirts = cashing.get_tshirts(True)
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
        tshirt = cashing.get_one_tshirt(item_id)
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