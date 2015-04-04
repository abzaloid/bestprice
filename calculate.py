# coding=utf-8

import webapp2
import logging

import json

from google.appengine.ext import db
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import memcache


import handler
import models
import caching
import search

prev_qnt = {}

class addItemToCart(handler.Handler):
	def post(self):
		if self.user_info:
			data = json.loads(self.request.body)
			item = data['item']
			price = float(data['price'])
			quantity = int(data['quantity'])
			last_quantity = int(data['last_quantity'])
			self.session['items'][item] = quantity * price

			stores = caching.get_stores()

			if not self.session.get('store_total'):
				for store in stores:
					self.session['store_total'][str(store._id)] = 0

			items_list = caching.get_one_item(item)

			if item not in self.session['quantity']:
				self.session['quantity'][item] = 0


			last_quantity = self.session['quantity'][item]

			for cur_item in items_list:
				self.session['store_total'][str(cur_item.store)] += cur_item.price * (quantity - last_quantity)


			if quantity == 0:
				del self.session['items'][item]

			total_sum = 0
			for m_item, m_cost in self.session['items'].items():
				total_sum += m_cost

			self.session['quantity'][item] = quantity

			response = {}
			response["status"] = 1
			response["number"] = total_sum

			for store in stores:
				response[str(store._id)] = self.session['store_total'][str(store._id)]

			self.session['item_count'] = total_sum	
			self.response.out.write(json.dumps(response))
			
		else:
			self.response.out.write(json.dumps({"status" : 0}))
			logging.error("%s not found" % self.user_info.name)



class delItemFromCart(handler.Handler):
	def post(self):
		if self.user_info:
			data = json.loads(self.request.body)
			item = data['item']
			last_quantity = self.session['quantity'][item]

			del self.session['quantity'][item]
			del self.session['items'][item]

			total_sum = 0
			for m_item, m_cost in self.session['items'].items():
				total_sum += m_cost



			items_list = caching.get_one_item(item)
			for cur_item in items_list:
				self.session['store_total'][str(cur_item.store)] -= cur_item.price * last_quantity

			stores = caching.get_stores()

			if not self.session.get('store_total'):
				for store in stores:
					self.session['store_total'][str(store._id)] = 0

			response = {}
			response["status"] = 1
			response["number"] = total_sum

			for store in stores:
				response[str(store._id)] = self.session['store_total'][str(store._id)]

			self.session['item_count'] = total_sum	
			self.response.out.write(json.dumps(response))
			
		else:
			self.response.out.write(json.dumps({"status" : 0}))
			logging.error("%s not found" % self.user_info.name)


class ShowShoppingList(handler.Handler):
    def get(self):

        current_store = self.request.get('store')
        if current_store is None or current_store == "":
            if memcache.get('current_store'):
                current_store = memcache.get('current_store')
            else:
                if self.user_info:
                    my_user=self.user
                    user_name = my_user.auth_ids[0]
                    current_store = caching.get_store_with_id(caching.get_user(user_name).store_id)
                else:
                    current_store = 0
                memcache.set('current_store', current_store)
        else:
            current_store = caching.get_store_with_id(int(current_store))
            memcache.set('current_store', current_store)

        data = self.request.get('subcat')
        subcat = data.split(' ')
        result = []
        for s in subcat:
            if s is not None:
                logging.error(s)
                cur_s = search.getSubCategory(s)
                result.append(cur_s)

        result = list(set(result))

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

        best_subcats_list = []
        best_items_list = []

        for subcategory in result:
        	if subcategory:
	        	best_subcats_list.append(subcategory)
	        	best_items_list.append(caching.get_items_with_subcategory(subcategory._id))



        self.render('shopping_list.html', 
            subcategories=subcategories,
            categories=categories,
            item_cart=item_cart,
            store_total=store_total,
            store_sum=store_sum,
            store_list=store_list,
            item_list=item_list,
            current_store=current_store,
            best_subcats_list=best_subcats_list,
            best_items_list=best_items_list,)

