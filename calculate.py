import webapp2
import logging

import json

from google.appengine.ext import db
from google.appengine.api import users
from webapp2_extras import sessions

import handler
import models
import caching


class addItemToCart(handler.Handler):
	def post(self):
		if users.get_current_user():
			data = json.loads(self.request.body)
			item = data['item']
			quantity = int(data['quantity'])
			self.session['items'][item] = quantity
			if quantity == 0:
				del self.session['items'][item]

			total_sum = 0
			for m_item, m_quantity in self.session['items'].items():
				total_sum += m_quantity

			self.session['item_count'] = total_sum	
			self.response.out.write(json.dumps({"status" : 1, "number": total_sum}))
			
		else:
			self.response.out.write(json.dumps({"status" : 0}))

