import json

out = []
downs = []
with open('./source.json', 'r') as jsonFile:
    data = json.load(jsonFile)
    for item in data:
        if item['status']!='DOWN':
            out.append(item)
        else:
            downs.append(item)  

with open('./source.json', 'w') as jsonFile:
    json.dump(out, jsonFile, indent=4)

with open('./downs.json', 'w') as jsonFile:
    json.dump(downs, jsonFile, indent=4)