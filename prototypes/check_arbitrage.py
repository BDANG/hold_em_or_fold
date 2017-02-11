#WIP / TO DO LIST
#include timer delays / multiproc the requests
#include withdraw / transaction fees

import itertools
import requests
import get_market_prices
import time

BUY_FEES_DICT = {'bitfinex': .002,
                 'bitstamp': .0025,
                 'btce': .005,
                 'cexio': .002,
                 'kraken': .0026} #fees represented as a decimal

SELL_FEES_DICT = {'bitfinex': .002,
                 'bitstamp': .0025,
                 'btce': .005,
                 'cexio': .002,
                 'kraken': .0026} #fees represented as a decimal

#The function calculates the arbritrage including fees from the exchanges
#marketPriceDict - a dictionary that maps exchange name to current market price
#exchange1 - an exchange that user is BUYING BTC on
#exchange2 - an exchange that user is SELLING BTC on
#!!!CURRENTLY ASSUMES FEE IS APPLIED TO CURRENCY RECIEVED (RECIEVE LESS THAN EXPECTED)
def arbitrage_difference_withfees(marketPriceDict, exchange1, exchange2):
    fee1 = BUY_FEES_DICT[exchange1]
    fee2 = SELL_FEES_DICT[exchange2]

    price1 = marketPriceDict[exchange1]
    price2 = marketPriceDict[exchange2]

    #%profit difference = (price sold - price bought) / price bought
    if (price1 < price2):
        #price1 is buy
        price1 *= (1.0+fee1)
        price2 *= (1.0-fee2)
        return (exchange1, exchange2, ((price2 - price1) / price1))
    else:
        #price2 is buy
        price1 *= (1.0-fee1)
        price2 *= (1.0+fee2)
        return (exchange2, exchange1, ((price1 - price2) / price2))


#The handler to find potential arbitrage opportunities using a list of exchanges to check
#listOfExchanges - a list of exchanges (strings) to check for opportunity
#listOfExchanges is like ["bitfinex", "btce"] (all lowercase)
#threshold - a DECIMAL specifying the minimum arbitrage desired
def handler(listOfExchanges):
    marketPriceDict = {} #dictionary that maps exchange name to current market price

    #populating market prices
    for exch, name in listOfExchanges.iteritems():
        successful_crawl = 0
        attempt_count = 0
        while(successful_crawl == 0 and attempt_count < 3):
            attempt_count+=1
            try:
                marketPriceDict[exch] = get_market_prices.handler(exch)
                successful_crawl = 1
            except:
                time.sleep(1)
                pass

    #obtain possible combinations
    arbitrage_opportunities = []
    combos = itertools.combinations(marketPriceDict.keys(), 2) #pick every possible combination of a pair of exchanges
    for exchange in combos: #iterate through the combinations
        arbitrage = arbitrage_difference_withfees(marketPriceDict, exchange[0], exchange[1])
        arbitrage_opportunities.append(arbitrage)

    return arbitrage_opportunities
