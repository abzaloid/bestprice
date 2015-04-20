# coding=utf-8

import os
import sys
import webapp2
import jinja2
import logging

import database
import search
import controllers
import admin
import cart
import calculate
import caching
import models

import user_controllers

from handler import Handler
from Forum import *


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


class ProfileHandler(Handler):
    def get(self):
        user = self.user
        if not user:
            self.redirect('/login')
        user = user.to_dict()
        logging.error(user)
        stores_list = list(caching.get_stores())
        self.render('user_profile_change.html',{'m_user': user, 
                                                'is_home':1,
                                                'first_name' : user['name'],
                                                'last_name' : user['last_name'],
                                                'stores_list':stores_list,})
    def post(self):
        user = self.user
        if not user:
            self.redirect('/login')
        store_name = self.request.get('choose_market')
        stores_list = list(caching.get_stores())
        t = db.GqlQuery('SELECT * FROM UserData WHERE login = :login', login = user.auth_ids)
        new_user = models.UserData()
        new_user = list(t)[0]
        db.delete(t)
        new_user.store_id = caching.get_store_id_with_name(store_name)
        new_user.put()
        self.redirect('/')

app = webapp2.WSGIApplication([('/', controllers.MainPage),
                               webapp2.Route('/logout', user_controllers.LogoutHandler, name='logout'),
                               webapp2.Route('/login', user_controllers.LoginHandler, name='login'), 
                               ('/signup', user_controllers.SignupHandler),
                               ('/password', user_controllers.SetPasswordHandler),
                               webapp2.Route('/forgot', user_controllers.ForgotPasswordHandler, name='forgot'),
                               webapp2.Route('/authenticated', user_controllers.AuthenticatedHandler, name='authenticated'),
                               webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', user_controllers.VerificationHandler, name='verification'),
                               ('/cart/add', cart.AddToCartHandler),
                               ('/about', controllers.AboutHandler),
                               ('/change_profile', user_controllers.ChangeProfile),
                               ('/done', cart.DoneHandler),
                               ('/mainpage', controllers.MainPage),
                               ('/forum/(\w+)', ForumHandler),
                               ('/forum/(\w+)/(\w+)', ForumCommentHandler),
                               ('/vote', VoteHandler),
                               ('/profile', ProfileHandler),
                               ('/forum', ForumViewer),
                               ('/forum/', ForumViewer),
                               ('/cart', cart.CartHandler),
                               ('/checkout', cart.CheckoutHandler),
                               ('/sendmail', admin.EmailHandler),
                               ('/submit', SubmissionHandler),
                               ('/listorders', cart.ListOrdersHandler),
                               ('/secure', controllers.SecureHandler),
                               ('/update_database', database.UpdateDatabase),
                               ('/update_forum', database.UpdateForum),
                               ('/search', search.SearchItem),
                               ('/lookfor', search.LookForItem),
                               ('/shopping_list', calculate.ShowShoppingList),
                               ('/additem', calculate.addItemToCart),
                               ('/delitem', calculate.delItemFromCart),
                               ('/all-subcategory/(\d+)', controllers.SubCategoryAJAX),
                               ('/all-subcategory-except/(\d+)', controllers.SubCategoryAJAXExcept),
                               ('/empty_cart', cart.EmptyCart),
                               ('/deleteitem', database.DeleteItemDatabase),
                               ('/category/(\d+)', controllers.ShowCategoryHandler),
                               ('/category/(\d+)/(\d+)', controllers.ShowCategoryWithPaginationHandler),
                               ('/subcategory/(\d+)/(\d+)', controllers.ShowSubCategoryHandler),
                               ('/subcategory/(\d+)/(\d+)/(\d+)', controllers.ShowSubCategoryWithPaginationHandler)], 
                               config=config, debug=True)
