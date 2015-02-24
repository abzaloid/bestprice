import logging

from google.appengine.ext import db
from google.appengine.api import memcache

import models

### CACHING ###
def get_tshirts(update = False):
    key = "tee"
    tshirts = memcache.get(key)
    if tshirts is None or update:
        logging.error("DB QUERY FOR TSHIRTS")
        tshirts = db.GqlQuery("SELECT * FROM Tshirt ORDER BY tshirt_id")
        tshirts = list(tshirts)
        memcache.set(key, tshirts)
    return tshirts

def get_one_tshirt(item_id, update = False):
    key = item_id 
    tshirt = memcache.get(key)
    if tshirt is None or update:
        logging.error("DB QUERY FOR SINGLE TSHIRT")
        tshirt = models.Tshirt.all().filter("tshirt_id =", int(item_id)).get()
        memcache.set(key, tshirt)
    return tshirt