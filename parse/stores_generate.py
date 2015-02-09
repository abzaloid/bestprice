import random
import json

stores = ['Green', 'Anvar', 'Gross', 'Ramstore', 'Galomart']

stores_json = []
for store in stores:
	cur_store = {}
	cur_store["name"] = store
	cur_store["phone"] = "222212"
	cur_store["description"] = "description goes here"
	stores_json.append(cur_store)

f = open("stores.json", "w")

f.write(json.dumps(stores_json))

f.close()
