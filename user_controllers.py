# coding=utf-8


import webapp2
import json
import logging
import re

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import mail

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.ext.webapp import template


from google.appengine.api import mail


import handler
import caching
import models

def user_required(m_handler):
    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
          self.redirect(self.uri_for('login'), abort=True)
        else:
          return m_handler(self, *args, **kwargs)

class SignupHandler(handler.Handler):
    def get(self):
        stores_list = list(caching.get_stores())
        self.render('signup.html',is_home=1, stores_list=stores_list)
    def post(self):
        email = self.request.get('email')
        user_name = self.request.get('name')
        password = self.request.get('password')
        check_password = self.request.get('check_password')
        last_name = self.request.get('lastname')
        first_name = self.request.get('firstname')
        store_name = self.request.get('choose_market')
        stores_list = list(caching.get_stores())

        logging.error(store_name)

        form_result = ""

        if password != check_password:
            form_result = "Two passwords do not match"
            self.render("signup.html", is_home=1,
                form_result=form_result,
                firstname=first_name,
                email=email,
                lastname=last_name,
                name=user_name,
                stores_list=stores_list,
                my_market=store_name)
            return

        if len(password) < 5:
            form_result = "Password length MUST be more than 4 characters"
            self.render("signup.html", is_home=1,
                form_result=form_result,
                firstname=first_name,
                email=email,
                lastname=last_name,
                name=user_name,
                stores_list=stores_list,
                my_market=store_name)
            return

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
            unique_properties,
            email_address=email, name=first_name, password_raw=password,
            last_name=last_name, verified=False)
        if not user_data[0]: #user_data is a tuple
            form_result = "User with such username or e-mail already exists"
            self.render("signup.html", is_home=1,
                form_result=form_result,
                firstname=first_name,
                email=email,
                lastname=last_name,
                name=user_name,
                stores_list=stores_list,
                my_market=store_name)
            return
    
        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)

        t = models.UserData(first_name = first_name, last_name = last_name, login = user_name, store_id = caching.get_store_id_with_name(store_name), email = email)
        t.put()

        verification_url = self.uri_for('verification', type='v', user_id=user_id,
          signup_token=token, _full=True)

        msg = u"""
Сәлем {name}!

Осы пошта арқылы abzaloid.appspot.com сайтында біреу тіркелді.

Егер өзіңіз болсаңыз, онда келесі үзбе арқылы электронды поштаңызды растауыңызды өтінеміз:
{url}

Сіздің логиніңіз: {login}

Kazakh Shop-ты қолданғаңызға рақмет!

Ізгі тілекпен,
Kazakh Shop!

"""

        # self.display_message(msg.format(url=verification_url))

        message = mail.EmailMessage()
        message.sender = "Kazakh Shop <abzal.serekov@gmail.com>"
        message.to = email
        message.subject = "abzaloid.appspot.com тіркелу"
        message.body = msg.format(url=verification_url,name=first_name,login=user_name)
        message.send()

        

        try:
            u = self.auth.get_user_by_password(user_name, password, remember=True,
                save_session=True)
            self.session["item_count"] = 0
            self.session["add_to_cart_count"] = 0
            self.session["items"] = {}
            self.session["store_total"] = {}
            self.session['quantity'] = {}
            self.redirect("/")
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', user_name, type(e))


class ForgotPasswordHandler(handler.Handler):
    def get(self):
        self._serve_page()

    def post(self):
        username = self.request.get('username')

        user = self.user_model.get_by_auth_id(username)
        
        user_data = list(db.GqlQuery("SELECT * FROM UserData WHERE login = :login", login = username))

        if user_data:
            name = user_data[0].first_name
            email = user_data[0].email
            
            user_id = user.get_id()
            token = self.user_model.create_signup_token(user_id)

            verification_url = self.uri_for('verification', type='p', user_id=user_id,
              signup_token=token, _full=True)

            msg = u"""
    Сәлем, {name}!

    Егер өзіңіз болсаңыз, онда келесі үзбе арқылы құпия сөзіңіді қайта қалпына келтіре аласыз:
    {url}

    Сіздің логиніңіз: {login}

    Kazakh Shop-ты қолданғаңызға рақмет!

    Ізгі тілекпен,
    Kazakh Shop!

    """

            message = mail.EmailMessage()
            message.sender = "Kazakh Shop <abzal.serekov@gmail.com>"
            message.to = email
            message.subject = "abzaloid.appspot.com құпия сөз"
            message.body = msg.format(url=verification_url,login=username,name=name)
            message.send()

        self.render('home.html',is_home=1,message="Password reset is sent to your email")
  
    def _serve_page(self, not_found=False):
        username = self.request.get('username')
        params = {
          'username': username,
          'not_found': not_found
        }
        self.render('forgot.html', params)


class VerificationHandler(handler.Handler):
    def get(self, *args, **kwargs):
        user = None
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']

        # it should be something more concise like
        # self.auth.get_user_by_token(user_id, signup_token)
        # unfortunately the auth interface does not (yet) allow to manipulate
        # signup tokens concisely
        user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token,
          'signup')

        if not user:
            logging.info('Could not find any user with id "%s" signup token "%s"',
                user_id, signup_token)
            self.abort(404)
        
        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        if verification_type == 'v':
            # remove signup token, we don't want users to come back with an old link
            self.user_model.delete_signup_token(user.get_id(), signup_token)

            if not user.verified:
                user.verified = True
                user.put()
                self.display_message('User email address has been verified.')
                return
        elif verification_type == 'p':
            self.render('resetpassword.html', token=signup_token,is_home=1)
        else:
            logging.info('verification type not supported')
            self.abort(404)

class SetPasswordHandler(handler.Handler):

    @user_required
    def post(self):
        password = self.request.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.get('confirm_password'):
          self.display_message('passwords do not match')
          return

        user = self.user
        user.set_password(password)
        user.put()

        # remove signup token, we don't want users to come back with an old link
        self.user_model.delete_signup_token(user.get_id(), old_token)
        
        self.display_message('Password updated')

class LoginHandler(handler.Handler):
    def get(self):
        self._serve_page()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        try:
            u = self.auth.get_user_by_password(username, password, remember=True,
                save_session=True)
            self.session["item_count"] = 0
            self.session["add_to_cart_count"] = 0
            self.session["items"] = {}
            self.session["store_total"] = {}
            self.session['quantity'] = {}

            self.redirect("/")
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', username, type(e))
            self._serve_page(True)

    def _serve_page(self, failed=False):
        username = self.request.get('username')
        params = {
          'username': username,
          'failed': failed
        }
        self.render('login.html', is_home=1,username=username,failed=failed)

class LogoutHandler(handler.Handler):
    def get(self):
        self.auth.unset_session()
        self.response.headers.add_header('Set-Cookie', 'session=; Path=/')
        self.redirect("/")

class AuthenticatedHandler(handler.Handler):
    @user_required
    def get(self):
        self.render('authenticated.html',is_home=1,)

