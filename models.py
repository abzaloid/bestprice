import time

from google.appengine.ext import db

from webapp2_extras import security

import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb


### MODELS ###
class Item(db.Model):
    name = db.StringProperty(required=True)
    category = db.StringProperty()
    subcategory = db.StringProperty()
    image = db.StringProperty()
    store = db.StringProperty()
    price = db.IntegerProperty()
    barcode = db.StringProperty()
    description = db.StringProperty(multiline=True)
    added_date = db.DateTimeProperty(auto_now_add=True)
    weight = db.StringProperty()
    _id = db.IntegerProperty()

class Store(db.Model):
    name = db.StringProperty(required=True)
    geo_address = db.GeoPtProperty()
    phone = db.PhoneNumberProperty()
    email = db.EmailProperty()
    address = db.StringProperty()
    city = db.StringProperty()
    website = db.LinkProperty()
    description = db.TextProperty()
    working_hours = db.StringProperty()
    image = db.LinkProperty()
    
class Tshirt(db.Model):
    tshirt_id = db.IntegerProperty(required = True)
    title = db.StringProperty(required = True)
    price = db.IntegerProperty()
    content = db.TextProperty()

class Order(db.Model):
    quantity = db.IntegerProperty(required = True)
    name = db.StringProperty(required = True)
    cost = db.FloatProperty(required = True)
    time_of_order = db.DateTimeProperty(auto_now_add = True)
    user_email = db.EmailProperty(required = True)

class Category(db.Model):
    name = db.StringProperty(required=True)
    image = db.LinkProperty()
    description = db.TextProperty()
    _id = db.IntegerProperty()

class SubCategory(db.Model):
    name = db.StringProperty(required=True)
    image = db.LinkProperty()
    description = db.TextProperty()
    category = db.StringProperty()
    _id = db.IntegerProperty()

class User(webapp2_extras.appengine.auth.models.User):
    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None