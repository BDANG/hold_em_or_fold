from bs4 import BeautifulSoup
import requests
headers = {'User-Agent': 'Mozilla/5.0'}
BITFINEX_URL = "https://www.bitfinex.com"
def get_bitfinex():
    print "okay"
    r = requests.get(BITFINEX_URL, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    spans = soup.select("span")
    print spans
    return 0.0
#The method will return the current market price for a given exchange
#exchangeName - a string that specifies the exchange
#returns the current market price as a float
def handler(exchangeName):
    if (exchangeName == "bitfinex"):
        x = get_bitfinex()
        return 0.0
    elif (exchangeName == ""):
        return 0.0
    elif (exchangeName == "okcoin"):
        return 0.0
    else:
        print "Unrecognized exchange"
        return 0.0

handler("bitfinex")
