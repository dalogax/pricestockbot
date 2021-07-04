import json

id = 1
with open('./source.json', 'r') as jsonFile:
    data = json.load(jsonFile)
    for item in data:
        item['id']=str(id)
        id = id + 1

with open('./source.json', 'w') as jsonFile:
    json.dump(data, jsonFile, indent=4)