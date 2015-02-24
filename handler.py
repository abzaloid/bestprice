import webapp2

from google.appengine.api import users
from webapp2_extras import sessions

import main

### BASE HANDLER CLASS ###
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = main.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, 
                    logged_in = users.get_current_user(),
                    item_count = self.session.get('item_count'),**kw))

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
        item_list = []
        cart_count = self.session.get('add_to_cart_count')
        if not cart_count: return None;
        for i in range(1, cart_count+1):
            item = self.session.get(str(i))
            if item:
                item_list.append(item)
        return item_list
