import webapp2
import logging

from google.appengine.ext.webapp import template

from google.appengine.api import users
from webapp2_extras import sessions

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

import main
import caching



### BASE HANDLER CLASS ###
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = main.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, params=None, **kw):
        if not params:
            params = {}
        user = self.user_info
        params['user'] = user

        do_not_touch = 0
        for i,j in kw.items():
            if 'pagination_count' in str(i) and '-1' in str(j):
                do_not_touch = 1
                break

        if do_not_touch == 0:
            logging.error('EMPTY!')
            self.session['used_category'] = []
        self.write(self.render_str(template, 
                    logged_in = users.get_current_user(),
                    item_count = self.session.get('item_count'),
                    user=user, **kw))

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def get_items_from_cart(self):
        """ Fetches items from sessions cart"""
        items = self.session.get('items')
        if not items: return None;
        item_list = []
        for item_name, item_count in items.items():
            item_list.append((caching.get_one_item(item_name), item_count))
        return item_list

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        return self.auth.store.user_model

    def display_message(self, message):
        self.render('message.html', message=message)
