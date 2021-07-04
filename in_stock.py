import json, sys, time
from termcolor import colored
from os import system, name

IN_STOCK = 'IN STOCK'

filename = sys.argv[1]


def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

while True:
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    for item in data:
        if item['status'] == IN_STOCK:
            formattedString = '#' + item['id'] + ' ' + item['name'] + ' ' + '@' + item['store'] + ' ' + item['price'] + '€'
            print(formattedString)
            time.sleep(5)