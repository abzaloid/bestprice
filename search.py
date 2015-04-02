# coding=utf-8

import webapp2
import logging

import json

from difflib import SequenceMatcher as SM

from google.appengine.ext import db

import handler
import models
import caching

max_items = 4
min_len = 1
max_distance = 1

### LEVENSHTEIN DISTANCE ###
# returns levenshtein distance (if same then 0, otherwise greater than 0)
def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]


def getItem(m_item):
    items = caching.get_items()

    similar_items = []
    submatch_items = []
    exact_item = []

    for item in items:
        cur_name = item.name
        cur_name = cur_name.lower()
        cur_distance = levenshtein(cur_name, m_item)
        if cur_name == m_item:
            exact_item.append(item)
        elif m_item in cur_name:
            submatch_items.append(item)
        elif cur_distance <= max_distance:
            similar_items.append((item, cur_distance))
        if len(exact_item) > 0:
            break
        if len(exact_item) > 0 and len(similar_items) + len(exact_item) >= max_items:
            break

    similar_items.sort(key=lambda tup: tup[1])
    submatch_items.sort(key=lambda p: len(p.name))
    found_items = exact_item + submatch_items + list(tup[0] for tup in similar_items)
    
    return found_items


def getSubCategory(m_subcat):
    subcategories = caching.get_subcategories()

    similar_subcats = []
    submatch_subcats = []
    exact_subcat = []

    for subcategory in subcategories:
        cur_name = subcategory.name
        cur_name = cur_name.lower()
        cur_distance = levenshtein(cur_name, m_subcat)
        if cur_name == m_subcat:
            exact_subcat.append(subcategory)
        elif m_subcat in cur_name:
            submatch_subcats.append(subcategory)
        elif cur_distance <= max_distance:
            similar_subcats.append((subcategory, cur_distance))
        if len(exact_subcat) > 0:
            break
        if len(exact_subcat) > 0 and len(similar_subcats) + len(exact_subcat) >= max_items:
            break

    similar_subcats.sort(key=lambda tup: tup[1])
    submatch_subcats.sort(key=lambda p: len(p.name))
    found_subcats = exact_subcat + submatch_subcats + list(tup[0] for tup in similar_subcats)

    return "" if len(found_subcats)==0 else found_subcats[0]

class SearchItem(handler.Handler):
    def get(self):
        self.render("search.html")

    def post(self):
        self.searching_object = self.request.get('searching_object')
        items = getItems(self.searching_object)
        self.render("search.html", searching_object = self.searching_object,
                                items = items)


class LookForItem(handler.Handler):
    def post(self):
        data = json.loads(self.request.body)
        item = data['item']
        logging.info("searching " + item)
        if len(item) < min_len:
            items = []
        else:
            items = getItem(item)
        if len(items) > max_items:
            items = items[:max_items]
        found_items = []
        for item in items:
            found_items.append(item.name)
        self.response.out.write(json.dumps({"items": found_items}))
        for item in items:
            logging.info(item.name)

class LookForSubCategory(handler.Handler):
    def post(self):
        data = json.loads(self.request.body)
        subcat = data['subcategory']
        subcat = subcat.split(' ')
        result = []
        for s in subcat:
            if s != "":
                logging.error(s)
                cur_s = getSubCategory(s)
                result.append(cur_s)


        categories = list(caching.get_categories())
        subcategories = list(caching.get_subcategories())

        item_cart = self.session.get('items')

        item_list = self.get_items_from_cart()
        store_sum = {}
        if item_list:
            for items_, cost in item_list:
                logging.error(len(items_))
                if items_:
                    quantity = int(round(cost / items_[0].price))
                    for item in items_:
                        if item.store not in store_sum:
                            store_sum[item.store] = 0
                        store_sum[item.store] += int(round(item.price * quantity))

        store_list = list(caching.get_stores())
        store_total = self.session.get('store_total')

        self.render('shopping_list.html', 
            subcategories=subcategories,
            categories=categories,
            item_cart=item_cart,
            store_total=store_total,
            store_sum=store_sum,
            store_list=store_list,
            item_list=item_list,
            best_list=result,)


