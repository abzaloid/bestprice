import handler
from webapp2_extras import sessions

import caching

class ItemViewer(handler.Handler):
	def get(self):

		item_name = self.request.get('name')

		item = caching.get_one_item(item_name)
		item_cart = self.session.get('items')

		categories = list(caching.get_categories())
		subcategories = list(caching.get_subcategories())

		self.render("item_viewer.html", {
			'items': item,
			'categories': categories,
			'subcategories': subcategories,
			'item_cart': item_cart,
			'is_home': 1
			})