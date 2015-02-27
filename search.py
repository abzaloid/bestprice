import webapp2
import logging

import json

from google.appengine.ext import db

import handler
import models
import caching

max_items = 5
min_len = 1
max_distance = 2

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
        cur_distance = levenshtein(item.name, m_item)
        if cur_distance == 0:
            exact_item.append(item)
        elif m_item in item.name:
            submatch_items.append(item)
        elif cur_distance <= max_distance:
            similar_items.append((item, cur_distance))
        if len(similar_items) + len(exact_item) >= max_items:
           break

    similar_items.sort(key=lambda tup: tup[1])
    submatch_items.sort(key=lambda p: len(p.name))
    found_items = exact_item + submatch_items + list(tup[0] for tup in similar_items)
    
    return found_items


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
        logging.info("searching")
        data = json.loads(self.request.body)
        item = data['item']
        if len(item) < min_len:
            items = []
        else:
            items = getItem(item)
        if len(items) > max_items:
            items = items[:max_items]
        logging.info(item)    
        found_items = []
        for item in items:
            found_items.append(item.name)
        self.response.out.write(json.dumps({"items": found_items}))
        for item in items:
            logging.info(item.name)