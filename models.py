from google.appengine.ext import db

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
    qty = db.IntegerProperty(required = True)
    size = db.StringProperty(required = True)
    tshirt_id = db.IntegerProperty(required = True)
    user_email = db.StringProperty(required = True)
    time_of_order = db.DateTimeProperty(auto_now_add = True)
