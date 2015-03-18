# coding=utf-8

import random
import json
categories = [u'Бакалея',
			u'Чай. Кофе. Какао',
			u'Молочные Продукты',
			u'Напитки']

subcategories = {}
subcategories[u'Бакалея'] = [u'Крупы',u'Макаронные Изделия',u'Соль',u'Сахар']
subcategories[u'Чай. Кофе. Какао'] = [u'Чай']
subcategories[u'Напитки'] = [u'Напитки']
subcategories[u'Молочные Продукты'] = [u'Молоко',u'Майонез']


subcategories_ = [u'Соль',
			u'Молоко',
			u'Майонез',
			u'Крупы',
			u'Макаронные Изделия',
			u'Чай',
			u'Напитки']

categories_json = []
for category in categories:
	cur = {}
	cur["name"] = category
	categories_json.append(cur)

f = open("categories.json", "w")

f.write(json.dumps(categories_json))

f.close()
