# coding=utf-8

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
    store = db.IntegerProperty()
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
    _id = db.IntegerProperty()
    
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

class UserData(db.Model):
    login = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.EmailProperty()
    store_id = db.IntegerProperty()

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

class Comment(ndb.Model):
    sender_key = ndb.KeyProperty()
    recipient_key = ndb.KeyProperty()
    sender = ndb.StringProperty()
    recipient = ndb.StringProperty()
    text = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    vote_count = ndb.IntegerProperty(default = 0)
    root = ndb.BooleanProperty(default = True)
    parent = ndb.KeyProperty()
    children = ndb.KeyProperty(kind="Comment", repeated=True)
    offset = ndb.IntegerProperty(default = 0)

class Message(ndb.Model):
    sender = ndb.StringProperty()
    recipient = ndb.StringProperty()
    subject = ndb.StringProperty()
    text = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class ForumPost(ndb.Model):
    forum_name = ndb.StringProperty()
    forumnyn_aty = ndb.StringProperty()
    url = ndb.StringProperty()
    url_host = ndb.StringProperty()
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    reference = ndb.StringProperty()
    vote_count = ndb.IntegerProperty(default = 0)
    comment_count = ndb.IntegerProperty(default = 0)
    time = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.TextProperty()
    categories = ndb.KeyProperty(kind= "ForumCategory", repeated=True)
    up_voters = ndb.KeyProperty(kind = "User", repeated=True)
    down_voters = ndb.KeyProperty(kind = "User", repeated=True)

class Forum(ndb.Model):
    name = ndb.StringProperty()
    aty = ndb.StringProperty()
    posts = ndb.IntegerProperty()

class ForumCategory(ndb.Model):
    name = ndb.StringProperty()

