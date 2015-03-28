import webapp2
import logging

import json

from google.appengine.ext import db
from google.appengine.api import users
from webapp2_extras import sessions

import handler
import models
import caching

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

			res_response = {}
			res_response["status"] = 1
			res_response["number"] = total_sum

			for store in stores:
				res_response[str(store._id)] = self.session['store_total'][str(store._id)]

			self.session['item_count'] = total_sum	
			self.response.out.write(json.dumps(res_response))
			
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

			res_response = {}
			res_response["status"] = 1
			res_response["number"] = total_sum

			for store in stores:
				res_response[str(store._id)] = self.session['store_total'][str(store._id)]

			self.session['item_count'] = total_sum	
			self.response.out.write(json.dumps(res_response))
			
		else:
			self.response.out.write(json.dumps({"status" : 0}))
			logging.error("%s not found" % self.user_info.name)

