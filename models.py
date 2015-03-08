from google.appengine.ext import db

### MODELS ###
class Item(db.Model):
    name = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    image = db.LinkProperty(required=True)
    storeid = db.IntegerProperty(required=True)
    price = db.FloatProperty(required=True)
    barcode = db.StringProperty()
    description = db.TextProperty()
    added_date = db.DateTimeProperty(auto_now_add=True)
    weight = db.FloatProperty()

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
    
class User(db.Model):
    name = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    favorite_csv = db.TextProperty()
    saved = db.FloatProperty()
    used_service = db.IntegerProperty(required=True)

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
