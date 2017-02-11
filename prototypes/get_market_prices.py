from bs4 import BeautifulSoup
import requests
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
            if ("\n" not in nextSiblingElement.text):
                marketPrice = float(nextSiblingElement.text)

    #print spans
    #print r

    return marketPrice
#The method will return the current market price for a given exchange
#exchangeName - a string that specifies the exchange
#returns the current market price as a float
def handler(exchangeName):
    marketPrice = 0.0
    if (exchangeName == "bitfinex"):
        marketPrice = get_bitfinex()
        return marketPrice
    elif (exchangeName == ""):
        return 0.0
    elif (exchangeName == "okcoin"):
        return 0.0
    else:
        print "Unrecognized exchange"
        return 0.0

print("Bitfinex market price: "+str(handler("bitfinex")))
