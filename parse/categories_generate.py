import random
import json

categories = ['Household', 
			'Pets', 
			'Mom & Baby', 
			'Personal Care', 
			'Beauty',
			'Health',
			'Beverages',
			'Snacks',
			'Breakfast & Cereals',
			'Pantry',
			'Baking']

categories_json = []
for category in categories:
	cur = {}
	cur["name"] = category
	categories_json.append(cur)

f = open("categories.json", "w")

f.write(json.dumps(categories_json))

f.close()
