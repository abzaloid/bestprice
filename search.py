import webapp2
import logging

from google.appengine.ext import db

import handler
import models
import caching

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
        max_distance = 1
        self.searching_object = self.request.get('searching_object')
        items = caching.get_items()
        
        similar_items = []
        submatch_items = []
        exact_item = []


        for item in items:
            cur_distance = levenshtein(item.name, self.searching_object)
            if cur_distance <= max_distance and cur_distance > 0:
                similar_items.append((item, cur_distance))
            elif cur_distance == 0:
                exact_item.append(item)
            elif self.searching_object in item.name:
                submatch_items.append(item)

        similar_items.sort(key=lambda tup: tup[1])
        found_items = exact_item + submatch_items + list(tup[0] for tup in similar_items)

        self.render("search.html", searching_object = self.searching_object,
                                items = found_items)