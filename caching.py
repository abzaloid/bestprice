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


def get_items(update = False):
    key = "my_items"
    items = memcache.get(key)
    if items is None or update:
        logging.error("DB QUERY FOR ITEMS")
        items = list(db.GqlQuery("SELECT * FROM Item"))
        memcache.set(key, items)
    return items


def get_categories(update = False):
    key = "my_categories"
    categories = memcache.get(key)
    if categories is None or update:
        logging.error("DB QUERY FOR CATEGORIES")
        categories = list(db.GqlQuery("SELECT * FROM Category"))
        memcache.set(key, categories)
    return categories

def get_stores(update = False):
    key = "my_stores"
    stores = memcache.get(key)
    if stores is None or update:
        logging.error("DB QUERY FOR STORES")
        stores = list(db.GqlQuery("SELECT * FROM Store"))
        memcache.set(key, stores)
    return stores
