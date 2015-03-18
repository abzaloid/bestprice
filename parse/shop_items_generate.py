dbase = db.GqlQuery('SELECT * From Item')
for p in dbase:
	p.delete()
f = open('shop_items.csv', 'rb')
with f as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
    	if row[0] == 'Name':
    		continue
    	logging.error(len(row))
    	for i in range(len(row)):
    		row[i] = row[i].decode('cp1251')
    		logging.error(row[i])
    		logging.error("-----")
    	cur_item = Item(name = row[0],
    		subcategory = row[1],
    		category = row[2],
    		image = row[3],
    		store = row[4],
    		price = int(row[5]),
    		description = row[6].replace('\n',' '),
    		weight = row[7])
    	cur_item.put()
    	logging.debug("added")
