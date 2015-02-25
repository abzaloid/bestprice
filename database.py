
import json
import logging

from google.appengine.ext import db

import handler
import models
import cashing

class UpdateDatabase(handler.Handler):
    def get(self):
        if db.Query(models.Item).count() <= 0:
            logging.debug("Created  Item model")
            f = open("parse/items.json", "r")
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
        
        if db.Query(models.Store).count() <= 0:
            logging.debug("Created  Item model")
            f = open("parse/stores.json", "r")
            stores = json.loads(''.join(line for line in f))
            f.close()
            for store in stores:
                t = models.Store(name = item["name"], 
                           description = item["description"])
                t.put()

        if db.Query(models.Category).count() <= 0:
            f = open("parse/categories.json")
            logging.debug("Created  Item model")
            categories = json.loads(''.join(line for line in f))
            f.close()
            for category in categories:
                t = models.Category(name = category["name"])
                t.put()
                
        self.redirect('/')

