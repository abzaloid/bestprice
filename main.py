# coding=utf-8

import os
import sys
import webapp2
import jinja2
import logging
import re

import database
import search
import controllers
import admin
import cart
import calculate
import caching
import models
import user_controllers
import ItemViewer

from handler import Handler
from Forum import *

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

### Configuration ###
config = {}
config = {
      'webapp2_extras.auth': {
            'user_model': 'models.User',
            'user_attributes': ['name']
            },
      'webapp2_extras.sessions': {
            'secret_key': 'my secret key which you dont know'
      }
}

class ShowProfileHandler(Handler):
    def get(self, profile):
        logging.error(profile)
        asked_user = list(db.GqlQuery('SELECT * FROM UserData WHERE login = :login', login = profile))
        if asked_user:
            asked_user = asked_user[0]
            self.write(u"Name:{}, Surname:{}, blablabla".format(asked_user.first_name, asked_user.last_name))
        else:
            self.write("Not found!")
    def post(self):
        pass

class ProfileHandler(Handler):
    def get(self):
        user = self.user
        if not user:
            self.redirect('/login')
        user = user.to_dict()
        logging.error(user)
        stores_list = list(caching.get_stores())
        cur_user = list(db.GqlQuery('SELECT * FROM UserData WHERE login = :login', login = user['auth_ids']))[0]


        self.render('user_profile_change.html',{'m_user': cur_user, 
                                                'is_home':1,
                                                'first_name' : user['name'],
                                                'last_name' : user['last_name'],
                                                'stores_list':stores_list,
                                                'address': cur_user.address if cur_user.address else "",
                                                'telephone': cur_user.telephone if cur_user.telephone else "",
                                                'status': ""})
    def post(self):
        status = "ok"
        user = self.user
        if not user:
            self.redirect('/login')
        store_name = self.request.get('choose_market')
        logging.error(store_name)
        address = self.request.get('address')
        telephone = self.request.get('telephone')
        stores_list = list(caching.get_stores())
        t = db.GqlQuery('SELECT * FROM UserData WHERE login = :login', login = user.auth_ids)
        new_user = models.UserData()
        new_user = list(t)[0]
        db.delete(t)
        new_user.store_id = int(store_name)
        new_user.address = address
        if re.match('^\+(?:[0-9] ?){6,14}[0-9]$', telephone):
            new_user.telephone = telephone
        else:
            status = "telephone"
        new_user.put()
        memcache.set('current_store', None)
        memcache.set('current_store' + user.auth_ids[0], None)

        self.render('user_profile_change.html',{'m_user': new_user, 
                                                'is_home':1,
                                                'first_name' : user.name,
                                                'last_name' : user.last_name,
                                                'stores_list': stores_list,
                                                'address': new_user.address if new_user.address else "",
                                                'telephone': new_user.telephone if new_user.telephone else "",
                                                'status': status})

app = webapp2.WSGIApplication([('/?', controllers.MainPage),
                                ('/logout/?', user_controllers.LogoutHandler),
                                ('/login/?', user_controllers.LoginHandler), 
                                ('/signup/?', user_controllers.SignupHandler),
                                ('/password/?', user_controllers.SetPasswordHandler),
                                webapp2.Route('/forgot/', user_controllers.ForgotPasswordHandler, name='forgot'),
                                webapp2.Route('/authenticated/', user_controllers.AuthenticatedHandler, name='authenticated'),
                                webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', user_controllers.VerificationHandler, name='verification'),
                                ('/cart/add/?', cart.AddToCartHandler),
                                ('/about/?', controllers.AboutHandler),
                                ('/change_profile/?', user_controllers.ChangeProfile),
                                ('/done/?', cart.DoneHandler),
                                ('/mainpage/?', controllers.MainPage),
                                ('/forum/(\w+)/?', ForumHandler),
                                ('/forum/(\w+)/(\w+)/?', ForumCommentHandler),
                                ('/vote/?', VoteHandler),
                                ('/profile/?', ProfileHandler),
                                ('/forum/?', ForumViewer),
                                ('/forum/?', ForumViewer),
                                ('/item/?', ItemViewer.ItemViewer),
                                ('/cart/?', cart.CartHandler),
                                ('/checkout/?', cart.CheckoutHandler),
                                ('/sendmail/?', admin.EmailHandler),
                                ('/submit/?', SubmissionHandler),
                                ('/listorders/?', cart.ListOrdersHandler),
                                ('/secure/?', controllers.SecureHandler),
                                ('/update_database/?', database.UpdateDatabase),
                                ('/update_forum/?', database.UpdateForum),
                                ('/search/?', search.SearchItem),
                                ('/lookfor/?', search.LookForItem),
                                ('/shopping_list/?', calculate.ShowShoppingList),
                                ('/additem/?', calculate.addItemToCart),
                                ('/delitem/?', calculate.delItemFromCart),
                                ('/all-subcategory/(\d+)/?', controllers.SubCategoryAJAX),
                                ('/all-subcategory-except/(\d+)/?', controllers.SubCategoryAJAXExcept),
                                ('/empty_cart/?', cart.EmptyCart),
                                ('/deleteitem/?', database.DeleteItemDatabase),
                                ('/category/(\d+)/?', controllers.ShowCategoryHandler),
                                ('/category/(\d+)/(\d+)/?', controllers.ShowCategoryWithPaginationHandler),
                                ('/subcategory/(\d+)/(\d+)/?', controllers.ShowSubCategoryHandler),
                                ('/subcategory/(\d+)/(\d+)/(\d+)/?', controllers.ShowSubCategoryWithPaginationHandler),
                                ('/show_profile/(\w+)/?', ShowProfileHandler),], 
                                config=config, debug=True)
