
import json


from google.appengine.ext import db

import handler
import models

class UpdateDatabase(handler.Handler):
    def get(self):
        f = open("items.json", "r")
        items = json.loads(''.join(line for line in f))
        f.close()
        for item in items:
            t = models.Item(name = item["name"], 
                       category = item["category"],
                       price = item["price"],
                       description = item["description"],
                       image = item["image"],
                       storeid = item["store_id"])
            t.put()
        
        f = open("stores.json", "r")
        stores = json.loads(''.join(line for line in f))
        f.close()
        for store in stores:
            t = models.Store(name = item["name"], 
                       description = item["description"])
            t.put()

class ShowDatabase(handler.Handler):
    def get(self):
        items = list(db.GqlQuery("SELECT * FROM Item"))
        self.render("main.html", items = items, items_size = len(items)-1)