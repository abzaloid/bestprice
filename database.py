# coding=utf-8

import json
import logging
import csv

from google.appengine.ext import db

import handler
import models
import caching

store_id = {}

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
    f = open("parse/subcategories.json", "r")
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

    my_stores = list(db.GqlQuery("SELECT * From Store"))
    for store in my_stores:
        store_id[store.name] = store._id


    db.delete(db.GqlQuery('SELECT * From Item'))
    f = open('parse/shop_items.csv', 'rb')
    with f as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        p = 0
        for row in spamreader:
            if row[0] == 'Name':
                continue
            for i in range(len(row)):
                row[i] = row[i].decode('cp1251')
            cur_item = models.Item(name = row[0],
                subcategory = row[1],
                category = row[2],
                image = "/static" + row[3],
                store = store_id[row[4]],
                price = int(row[5]),
                description = row[6],
                weight = row[7],
                _id = p)
            p += 1
            cur_item.put()


class UpdateForum(handler.Handler):
    def get(self):
        p = models.Forum(name="news", posts=0, aty="Новости")
        p.put()
        p = models.Forum(name="feedback", posts=0, aty = "Фидбэк")
        p.put()
        p = models.Forum(name="offtopic", posts=0, aty ="Оффтопик")
        p.put()


class UpdateDatabase(handler.Handler):
    def get(self):
        generateSubCategories()
        self.write('SubCategories is done')
        generateStores()
        self.write('Stores is done')
        generateCategories()
        self.write('Categories is done')
        generateItems()
        self.write('Items is done')
        self.write('Updated!')