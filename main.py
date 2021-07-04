import json, re, requests, time, urllib3, sys, codecs
import winsound
# import os
from termcolor import colored
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

IN_STOCK = 'IN STOCK'
OUT_OF_STOCK = 'OUT OF STOCK'
DOWN = 'DOWN'

headers = {'User-Agent': 'pricestockbot'}

fakeHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def pccomponentes(item, response):
    id_search = re.search('idarticle=\"\d*\"', response.text, re.IGNORECASE)
    if id_search:
        idArticle = id_search.group(0).split('"')[1]
        item['articleId'] = idArticle
        item['addToCart'] = 'https://www.pccomponentes.com/cart/addItem/' + idArticle
        pccomponentesStockUrl = 'https://www.pccomponentes.com/ajax_nc/articles/price_and_availability?idArticle=' + idArticle
        pccomponentesStockResponse = requests.get(pccomponentesStockUrl, verify=False, headers=fakeHeaders)
        pccomponentesJson = json.loads(pccomponentesStockResponse.text)
        if pccomponentesJson['availability']['status'] == 'outOfStock':
            item['status'] = OUT_OF_STOCK
        else:
            item['status'] = IN_STOCK
    price_search = re.search('data-price=\"[\d,\.]*\"', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('"')[1]
    
def coolmod(item, response):
    stock_search = re.search('button-not-buy', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('\"price\": [\d.\.]*,', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split(' ')[1].split(',')[0]

def vsgamers(item, response):
    stock_search = re.search('outOfStock', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('itemprop=\"price\" content=\"[\d.\.]*\"', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('"')[3]
    
def neobyte(item, response):
    stock_search = re.search('label-danger', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('itemprop=\"price\" content=\"[\d.\.]*\">', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('"')[3]

def aussar(item, response):
    stock_search = re.search('OutOfStock', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('itemprop=\"price\" content=\"[\d.\.]*\">', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('"')[3]

def siabyte(item, response):
    stock_search = re.search('var quantityAvailable = 0;', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('class=\"price new\" itemprop=\"price\">[\d,]* €', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('>')[1].split(' ')[0]

def lifeinformatica(item, response):
    stock_search = re.search('https://schema.org/OutOfStock', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('content=\"[\d.\.]*\" itemprop=\"price\"', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('"')[1]

def izarmicro(item, response):
    stock_search = re.search('OutOfStock', response.text, re.IGNORECASE)
    if stock_search:
        item['status'] = OUT_OF_STOCK
    else: 
        item['status'] = IN_STOCK
    price_search = re.search('itemprop=\"price\">[\d.\.]* <', response.text, re.IGNORECASE)
    if price_search:
        item['price'] = price_search.group(0).split('>')[1].split(' ')[0]

def beep():
    frequency = 2500
    duration = 100
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency, duration)

# def beep():
#     os.system('say "Alerta, alerta, he encontrado stock!"')


def telegram(text):
    requests.post('https://api.telegram.org/******:******/sendMessage',
              data={'chat_id': '*****', 'text': text})

def stillAlive():
    requests.get('http://192.168.0.99:1880/pricestockbot/stillalive', verify=False, headers=headers)

storeProcessors = {
    'pccomponentes': pccomponentes,
    'vsgamers': vsgamers,
    'neobyte': neobyte,
    'coolmod': coolmod,
    'aussar': aussar,
    'siabyte': siabyte,
    'lifeinformatica': lifeinformatica,
    'izarmicro': izarmicro
}

filename = sys.argv[1]

while True:
    stillAlive()
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    for item in data:
        try:
            header = headers if item['store'] == 'coolmod' else fakeHeaders
            response = requests.get(item['url'], verify=False, headers=header)
            if response.status_code == 200: 
                newTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                storeProcessors.get(item['store'])(item, response)
                
                if item['status'] == IN_STOCK:
                    if ((datetime.now() - datetime.strptime(item['lastStockTs'], "%d/%m/%Y %H:%M:%S")).seconds>3600):
                        beep()
                        logString = newTime + ' -> ' + '#' + item['id'] + ' ' + item['name'] + ' ' + '@' + item['store'] + ' ' + item['price'] + '€' + ' \n'
                        text_file = codecs.open("last_drops.log", "a+", "utf-8")
                        text_file.write(logString)
                        text_file.close()
                    item['lastStockTs'] = newTime
                    if ('3060' in item['name'] and float(item['price'])<450):
                        telegram(item['name'] + ' ' + item['price'] + '€ ' + item['url'])
            else: 
                item['status'] = DOWN
            formattedString = newTime + ' -> ' + colored('#'+item['id'],'yellow') + ' ' + colored(item['name'],'cyan' if item['status'] == IN_STOCK else 'white') + ' ' + colored('@' + item['store'],'blue' if item['status'] == IN_STOCK else 'white') + ' ' + colored(item['price'] + '€', 'yellow' if item['status'] == IN_STOCK else 'white') + ' :: ' + colored(item['status'],'green' if item['status'] == IN_STOCK else 'red')
            print(formattedString)
        except:
            logString = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' -> ' + str(item) + ' \n' 
            text_file = codecs.open("errors.log", "a+", "utf-8")
            text_file.write(logString)
            text_file.close()
        time.sleep(0.2)

    with open(filename, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)