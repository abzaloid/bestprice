import random
import json


def generate_items():
	f = open("items.txt", "r")

	items = []

	for item in f:
		items.append(item[:-1])


	f.close()

	category = ['First Type', 'Second Type', 
				'Third Type', 'Fourth Type']

	stores = ['Green', 'Anvar', 'Gross', 'Ramstore', 'Galomart']

	items_json = []

	for item in items:
		cur_item = {}
		for store_id in range(len(stores)):
			cur_item["name"] = item
			cur_item["category"] = random.choice(category)
			cur_item["store_id"] = store_id
			cur_item["price"] = random.uniform(50, 1000)
			cur_item["image"] = "http://velocityagency.com/wp-content/uploads/2013/08/go.jpg"
			cur_item["description"] = "description goes here"
		items_json.append(cur_item)

	f = open("items.json", "w")

	f.write(json.dumps(items_json))

	f.close()

def get_with_commas():
	f = open("dict.txt", 'r')
	my_list = ''.join(line[:-1] for line in f).split(' ')
	f.close()
	f = open('items.txt', 'w')
	for item in my_list:
		if len(item[:-1]) > 0:
			f.write("%s\n" % item[:-1])
	f.close()


get_with_commas()
generate_items()