import itertools
import requests
import get_market_prices

BUY_FEES_DICT = {} #fees represented as a decimal
BUY_FEES_DICT["bitfinex"] = .002
BUY_FEES_DICT["bitstamp"] = .0025
BUY_FEES_DICT["btce"] = .005
BUY_FEES_DICT["cexio"] = .002

SELL_FEES_DICT = {} #fees represented as a decimal
SELL_FEES_DICT["bitfinex"] = .002
SELL_FEES_DICT["bitstamp"] = .0025
SELL_FEES_DICT["btce"] = .005
SELL_FEES_DICT["cexio"] = .002

#The function calculates the arbritrage including fees from the exchanges
#marketPriceDict - a dictionary that maps exchange name to current market price
#exchange1 - an exchange that user is BUYING BTC on
#exchange2 - an exchange that user is SELLING BTC on
#!!!CURRENTLY ASSUMES FEE IS APPLIED TO CURRENCY RECIEVED (RECIEVE LESS THAN EXPECTED)
def arbitrage_difference_withfees(marketPriceDict, exchange1, exchange2):
    buyFee = BUY_FEES_DICT[exchange1]
    sellFee = SELL_FEES_DICT[exchange2]

    buyPrice = marketPriceDict[exchange1] * (1.0+buyFee)
    sellPrice = marketPriceDict[exchange2] * (1.0-sellFee)

    #%profit difference = (price sold - price bought) / price bought
    arbitragePercent = (sellPrice - buyPrice) / buyPrice
    return arbitragePercent



#The function calculates the potential arbritrage between two exchanges
#marketPriceDict - a dictionary that maps exchange name to current market price
#exchange1 - an exchange represented as a string
#exchange2 - an exchange represented as a string
#returns ??? something about arbritrage opportunity
def calculate_arbitrage(marketPriceDict, exchange1, exchange2):
    buyExchange = None #the exchange to buy btc on
    sellExchange = None #the change to sell btc on

    market1 = marketPriceDict[exchange1]
    market2 = marketPriceDict[exchange2]
    arbDiff = 0.0 # a percent representing the arbritrage
    arbitragePercentWithFee = 0.0
    maxMarket = max(market1, market2)
    if (maxMarket == market1): #market1 and exchange1 is the larger price and SOLD
        arbDiff = market1/market2 #WIP change to include fees
        arbitragePercentWithFee = arbitrage_difference_withfees(marketPriceDict, exchange2, exchange1)
        buyExchange = exchange2
        sellExchange = exchange1
    else: #market2 and exchange2 is the larger price
        arbDiff = market2/market1 #WIP change to include fees
        arbitragePercentWithFee = arbitrage_difference_withfees(marketPriceDict, exchange1, exchange2)
        buyExchange = exchange1
        sellExchange = exchange2

    print "\nThe arbitrage difference is: "+str((arbDiff-1)*100.0)
    print "Including fee, the difference is: "+str(arbitragePercentWithFee*100.0)
    print "Buy on exchange: "+buyExchange+" ("+str(marketPriceDict[buyExchange])+")"
    print "Sell on exchange: "+sellExchange+" ("+str(marketPriceDict[sellExchange])+")\n"


#The handler to find potential arbitrage opportunities using a list of exchanges to check
#listOfExchanges - a list of exchanges (strings) to check for opportunity
#listOfExchanges is like ["bitfinex", "btce"] (all lowercase)
def handler(listOfExchanges):
    marketPriceDict = {} #dictionary that maps exchange name to current market price

    #populating market prices
    for exch in listOfExchanges:
        marketPriceDict[exch] = get_market_prices.handler(exch)

    #obtain possible combinations
    combos = itertools.combinations(marketPriceDict.keys(), 2) #pick every possible combination of a pair of exchanges
    for exchange in combos: #iterate through the combinations
        calculate_arbitrage(marketPriceDict, exchange[0], exchange[1])



TESTLIST = ["bitfinex", "btce", "bitstamp", "cexio", "kraken"]
handler(TESTLIST)
