
import json
import logging

from google.appengine.ext import db

import handler
import models
import cashing

class DeleteItemDatabase(handler.Handler):
    def get(self):
        items = db.GqlQuery("SELECT * FROM Item")
        if items:
            for item in items:
                item.delete()

class UpdateDatabase(handler.Handler):
    def get(self):
        if db.Query(models.Item).count() <= 0:
            logging.debug("Created Item model")
            f = open("parse/items.json", "r")
            items = json.loads(''.join(line for line in f))
            f.close()
            for item in items:
                t = models.Item(name = item["name"], 
                           category = item["category"],
                           price = item["price"],
                           description = item["description"],
                           image = item["image"],
                           store = item["store"])
                t.put()
        
        if db.Query(models.Store).count() <= 0:
            logging.debug("Created Store model")
            f = open("parse/stores.json", "r")
            stores = json.loads(''.join(line for line in f))
            f.close()
            for store in stores:
                t = models.Store(name = store["name"], 
                           description = store["description"])
                t.put()

        if db.Query(models.Category).count() <= 0:
            logging.debug("Created Category model")
            f = open("parse/categories.json")
            logging.debug("Created  Item model")
            categories = json.loads(''.join(line for line in f))
            f.close()
            for category in categories:
                t = models.Category(name = category["name"])
                t.put()
                
        self.redirect('/')

