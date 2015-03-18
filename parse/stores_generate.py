import random
import json

stores = ['Green', 'Magnum', 'Galmart', 'Ramstore']

stores_json = []
for store in stores:
	cur_store = {}
	cur_store["name"] = store
	stores_json.append(cur_store)

f = open("stores.json", "w")

f.write(json.dumps(stores_json))

f.close()
