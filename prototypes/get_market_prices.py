from bs4 import BeautifulSoup
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0'}
BITFINEX_URL = "https://www.bitfinex.com/stats"

def get_bitfinex():
    marketPrice = 0.0
    r = requests.get(BITFINEX_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")

    #btc price within a <td> element
    tdList = soup.select("td")
    for tdElement in tdList: #iterate the list of <td>
        if tdElement.text == "BTCUSD": #there are two: <td>BTCUSD</td>
            nextSiblingElement = tdElement.next_sibling.next_sibling
            if ("\n" not in nextSiblingElement.text): #the desired element does not have a newline character in the next
                marketPrice = float(nextSiblingElement.text)

    return marketPrice

BTCE_URL = "https://btc-e.com"
def get_btce():
    r = requests.get(BTCE_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    strongList = soup.select("strong")
    price = re.findall("[0-9]+.[0-9]+", str(strongList[0]))
    return price[0]

BITSTAMP_URL = "https://bitcoinwisdom.com"
def get_bitstamp():
    r = requests.get(BITSTAMP_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    span = soup.find("span", {"id": "market_bitstampbtcusd"})
    price = re.findall("[0-9]+.[0-9]+", str(span))
    return price[0]

#The method will return the current market price for a given exchange
#exchangeName - a string that specifies the exchange
#returns the current market price as a float
def handler(exchangeName):
    if (exchangeName == "bitfinex"):
        return get_bitfinex()
    elif (exchangeName == "btce"):
        return get_btce()
    elif (exchangeName == "bitstamp"):
        return get_bitstamp()
    else:
        print "Unrecognized exchange"
        return 0

print("Bitfinex market price: "+str(handler("bitfinex")))
print("BTC-e market price: "+str(handler("btce")))
print("Bitstamp market price: "+str(handler("bitstamp")))
