# coding=utf-8

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

def get_one_item(item_name, update = False):
    key = item_name
    item = retrieve(key)
    if item is None or update:
        logging.error("DB QUERY FOR SINGLE ITEM")
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
    key = 'my category ' + category_name
    items = retrieve(key)
    if items is None or update:
        logging.error("DB QUERY FOR SINGLE category")
        items = list(db.GqlQuery("SELECT * FROM Item WHERE category = :category_name", category_name = category_name))
        store(key, items)
    return list(items)


def get_items_from_store(store_id, update=False):
    stores = list(get_stores())
    key = 'my store ' + store_id
    items = retrieve(key)
    if items is None or update:
        logging.error("DB QUERY FOR SINGLE stores")
        items = list(db.GqlQuery("SELECT * FROM Item WHERE store = :store", store=store_id))
        store(key, items)
    return items     

def get_items_with_subcategory(subcategory_id, update = False):
    subcategories = list(get_subcategories())
    subcategory_name = ""
    for subcategory in subcategories:
        if subcategory._id == int(subcategory_id):
            subcategory_name = subcategory.name
            break
    key = 'my subcategory ' + subcategory_name
    items = retrieve(key)
    if items is None or update:
        logging.error("DB QUERY FOR SINGLE subcategory")
        items = list(db.GqlQuery("SELECT * FROM Item WHERE subcategory = :subcategory_name", subcategory_name = subcategory_name))
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


def get_subcategories(update = False):
    key = "my subcategories"
    subcategories = retrieve(key)
    if subcategories is None or update:
        logging.error("DB QUERY FOR subcategories")
        subcategories = list(db.GqlQuery("SELECT * FROM SubCategory"))
        store(key, subcategories)
    return subcategories

def get_stores(update = False):
    key = "my_stores"
    stores = retrieve(key)
    if stores is None or update:
        logging.error("DB QUERY FOR STORES")
        stores = list(db.GqlQuery("SELECT * FROM Store"))
        store(key, stores)
    return stores

def get_store_with_id(store_id, update = False):
    stores = get_stores()
    for store in stores:
        if store._id == store_id:
            return store
    return None

def get_store_of_user(user):
    logging.error(type(user))
    for key,val in user.items():
        logging.error(str(key) + " " + str(val))
    return 1