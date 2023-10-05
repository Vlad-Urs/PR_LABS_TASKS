import json

with open('LAB4/products.json', 'r') as json_file:
	json_load = json.load(json_file)

for product in json_load:
    print(product['name'])