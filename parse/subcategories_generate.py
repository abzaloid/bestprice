# coding=utf-8

import random
import json
categories = [u'Бакалея',
			u'Чай. Кофе. Какао',
			u'Молочные продукты',
			u'Напитки']

subcategories = {}
subcategories[u'Бакалея'] = [u'Крупы',u'Макаронные Изделия',u'Соль',u'Сахар']
subcategories[u'Чай. Кофе. Какао'] = [u'Чай']
subcategories[u'Напитки'] = [u'Напитки']
subcategories[u'Молочные продукты'] = [u'Молоко',u'Майонез']


subcategories_ = [u'Соль',
			u'Молоко',
			u'Майонез',
			u'Крупы',
			u'Макаронные Изделия',
			u'Чай',
			u'Напитки']

subcategories_json = []
for category in categories:
	for subcat in subcategories[category]:
		cur = {}
		cur["name"] = subcat
		cur["category"] = category
		subcategories_json.append(cur)

f = open("subcategories.json", "w")

f.write(json.dumps(subcategories_json))

f.close()
