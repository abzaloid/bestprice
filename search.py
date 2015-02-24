import webapp2
from google.appengine.ext import db

import handler
import models

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


class SearchItem(handler.Handler):
    def get(self):
        self.render("search.html")

    def post(self):
        max_distance = 2
        self.searching_object = self.request.get('searching_object')
        items = list(db.GqlQuery("SELECT * FROM Item"))
        stores = list(db.GqlQuery("SELECT * FROM Store"))
        found_items = []
        for item in items:
            cur_distance = levenshtein(item.name, self.searching_object)
            if cur_distance <= max_distance:
                logging.debug(cur_distance)
                logging.debug(item.name)
                found_items.append((item, cur_distance))
        found_items.sort(key=lambda tup: tup[1])

        found_stores = []
        for store in stores:
            if store.name == self.searching_object:
                found_stores.append(store)
        self.render("search.html", searching_object = self.searching_object,
                                items = list(tup[0] for tup in found_items), 
                                stores = found_stores)