import handler
import caching

from webapp2_extras import sessions

import logging

class ItemViewer(handler.Handler):
	def get(self):

		item_name = self.request.get('name')

		item = caching.get_one_item(item_name)
		first_item = None
		dates = {}

		if not item or len(item) == 0:
			item = None
		else:
			first_item = item[0]
			for i in item:
				dates[i._id] = i.added_date.strftime('%d-%m-%y %H:%M:%S')




		logging.error(item)

		categories = list(caching.get_categories())
		subcategories = list(caching.get_subcategories())
		item_cart = self.session.get('items')
		store_list = list(caching.get_stores())

		self.render("item_viewer.html", {
			'item_name': item_name,
			'items': item,
			'item': first_item,
			'categories': categories,
			'subcategories': subcategories,
			'store_list': store_list,
			'item_cart': item_cart,
			'dates': dates,
			'is_home': 1
			})