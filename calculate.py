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
			if self.session['items'] is None:
				self.session['items'] = {}
			else:
				self.session['items'][item] = quantity
				if quantity == 0:
					del self.session['items'][item]
			self.response.out.write(json.dumps({"status" : 1, "number": len(self.session['items'])}))
		else:
			self.response.out.write(json.dumps({"status" : 0}))

