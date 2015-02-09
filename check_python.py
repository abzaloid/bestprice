import json

f = open("items.json", "r")
items = json.loads(''.join(line for line in f))
f.close()

print items