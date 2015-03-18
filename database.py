
import json
import logging
import csv

from google.appengine.ext import db

import handler
import models
import caching

class DeleteItemDatabase(handler.Handler):
    def get(self):
        db.delete(db.GqlQuery("SELECT * FROM Item"))

def generateStores():
    db.delete(db.GqlQuery("SELECT * From Store"))
    f = open("parse/stores.json", "r")
    stores = json.loads(''.join(line for line in f))
    f.close()
    p = 0
    for store in stores:
        t = models.Store(name = store["name"], _id=p)
        p += 1
        t.put()


def generateSubCategories():
    db.delete(db.GqlQuery("SELECT * From SubCategory"))
    f = open("parse/subcategories.json")
    subcategories = json.loads(''.join(line for line in f))
    f.close()
    p = 0
    for subcategory in subcategories:
        t = models.SubCategory(name = subcategory["name"], 
                            category = subcategory["category"],
                            _id = p)
        p += 1
        t.put()


def generateCategories():
    db.delete(db.GqlQuery("SELECT * From Category"))
    f = open("parse/categories.json")
    categories = json.loads(''.join(line for line in f))
    f.close()
    p = 0
    for category in categories:
        t = models.Category(name = category["name"], _id = p)
        p += 1
        t.put()


def generateItems():
    db.delete(db.GqlQuery('SELECT * From Item'))
    f = open('parse/shop_items.csv', 'rb')
    with f as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if row[0] == 'Name':
                continue
            logging.error(len(row))
            for i in range(len(row)):
                row[i] = row[i].decode('cp1251')
            cur_item = models.Item(name = row[0],
                subcategory = row[1],
                category = row[2],
                image = "/static" + row[3],
                store = row[4],
                price = int(row[5]),
                description = row[6],
                weight = row[7])
            cur_item.put()


class UpdateDatabase(handler.Handler):
    def get(self):
        generateSubCategories()
        generateStores()
        generateItems()
        generateCategories()
        self.write('Updated!')