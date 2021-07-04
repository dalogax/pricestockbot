import json, random

id = 73
with open('./source.json', 'r') as jsonFile:
    data = json.load(jsonFile)
    random.shuffle(data)

with open('./source.json', 'w') as jsonFile:
    json.dump(data, jsonFile, indent=4)