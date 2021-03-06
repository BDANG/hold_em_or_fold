from bs4 import BeautifulSoup
import requests
import re
import json
import krakenex

headers = {'User-Agent': 'Mozilla/5.0'}

k = krakenex.API()
k.load_key('kraken.key')



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

    return float(marketPrice)

BTCE_URL = "https://btc-e.com"
def get_btce():
    r = requests.get(BTCE_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    strongList = soup.select("strong")
    price = re.findall("[0-9]+.[0-9]+", str(strongList[0]))
    return float(price[0])

BITSTAMP_URL = "https://bitcoinwisdom.com"
def get_bitstamp():
    r = requests.get(BITSTAMP_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    span = soup.find("span", {"id": "market_bitstampbtcusd"})
    price = re.findall("[0-9]+.[0-9]+", str(span))
    return float(price[0])

CEXIO_URL = "https://cex.io"
def get_cexio():
    r = requests.get(CEXIO_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    span = soup.find("span", {"id": "ticker-BTC-USD-price"})
    price = re.findall("[0-9]+.[0-9]+", str(span))
    return float(price[0])

ITBIT_URL = "https://www.itbit.com"
def get_itbit():
    r = requests.get(ITBIT_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    span = soup.find("span", {"id": "last"})
    print(span)
    price = re.findall("[0-9]+.[0-9]+", str(span))
    return float(price[0])

def get_kraken():
    json_string = k.query_public('Ticker', {'pair': 'XXBTZUSD'})
    ticker_list = re.findall("[0-9]+.[0-9]+", str(json_string))
    return float(ticker_list[2])

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
    elif (exchangeName == "cexio"):
        return get_cexio()
    elif (exchangeName == "itbit"):
        return get_itbit()
    elif (exchangeName == "kraken"):
        return get_kraken()
    else:
        print "Unrecognized exchange"
        return 0


#print("Bitfinex market price: "+str(handler("bitfinex")))
#print("BTC-e market price: "+str(handler("btce")))
#print("Bitstamp market price: "+str(handler("bitstamp")))
#print("CEX.io market price: "+str(handler("cexio")))
#print("itBit market price: "+str(handler("itbit")))
#print("Kraken market price: "+str(handler("kraken")))
