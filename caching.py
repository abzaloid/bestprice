import logging

from google.appengine.ext import db
from google.appengine.api import memcache

import models
import pickle

def store(key, value, chunksize=950000):
    serialized = pickle.dumps(value, 2)
    values = {}
    for i in xrange(0, len(serialized), chunksize):
        values['%s.%s' % (key, i//chunksize)] = serialized[i : i+chunksize]
    return memcache.set_multi(values)

def retrieve(key):
    result = memcache.get_multi(['%s.%s' % (key, i) for i in xrange(32)])
    if result:
        serialized_data = ''.join([i for key, i in sorted(result.items()) if key in result and i is not None])
        return pickle.loads(serialized_data)
    else:
        return None

### CACHING ###
def get_tshirts(update = False):
    key = "tee"
    tshirts = retrieve(key)
    if tshirts is None or update:
        logging.error("DB QUERY FOR TSHIRTS")
        tshirts = db.GqlQuery("SELECT * FROM Tshirt ORDER BY tshirt_id")
        tshirts = list(tshirts)
        store(key, tshirts)
    return tshirts


def get_one_tshirt(item_id, update = False):
    key = item_id 
    tshirt = retrieve(key)
    if tshirt is None or update:
        logging.error("DB QUERY FOR SINGLE TSHIRT")
        tshirt = models.Tshirt.all().filter("tshirt_id =", int(item_id)).get()
        store(key, tshirt)
    return tshirt


def get_one_item(item_name, update = False):
    key = item_name
    item = retrieve(key)
    if item is None or update:
        logging.error("DB QUERY FOR SINGLE ITEM")
        #item = models.Item.all().filter("name =", item_name).get()
        item = db.GqlQuery("SELECT * FROM Item WHERE name = :item_name", item_name = item_name)
        store(key, item)
    return list(item)


def get_items_with_category(category_id, update = False):
    categories = list(get_categories())
    category_name = ""
    for category in categories:
        if category._id == int(category_id):
            category_name = category.name
            logging.error("ok!")
            break
    key = category_name
    items = retrieve(key)
    if items is None or update:
        logging.error("DB QUERY FOR SINGLE category")
        #item = models.Item.all().filter("name =", item_name).get()
        items = db.GqlQuery("SELECT * FROM Item WHERE category = :category_name", category_name = category_name)
        temp_items_names = []
        temp_items = []
        logging.error("initial length %s" % str(len(list(items))))
        for item in items:
            if item.name not in temp_items_names:
                temp_items.append(item)
                temp_items_names.append(item.name) 

        logging.error("final length %s" % str(len(temp_items)))
        items = temp_items
        store(key, items)
    return list(items)


def get_items(update = False):
    key = "my_items"
    items = retrieve(key)
    if items is None or update:
        logging.error("DB QUERY FOR ITEMS")
        items = list(db.GqlQuery("SELECT * FROM Item"))
        store(key, items)
    return items


def get_categories(update = False):
    key = "my_categories"
    categories = retrieve(key)
    if categories is None or update:
        logging.error("DB QUERY FOR CATEGORIES")
        categories = list(db.GqlQuery("SELECT * FROM Category"))
        store(key, categories)
    return categories


def get_stores(update = False):
    key = "my_stores"
    stores = retrieve(key)
    if stores is None or update:
        logging.error("DB QUERY FOR STORES")
        stores = list(db.GqlQuery("SELECT * FROM Store"))
        store(key, stores)
    return stores
