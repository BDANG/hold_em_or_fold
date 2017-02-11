import datetime
import pandas
import itertools
import csv
import sys

#!!! See README.txt in the same directory
#!!! CHANGEABLE
CSV_DIR = "/Users/briandang/Downloads/" #location of csv data
EXCHANGE_LIST = ["bitfinex", "bitstamp", "btce", "kraken"] #make sure you have csv for each exchange
THRESHOLD = .07 #a decimal representing the percent of the arbitrage
SKIPS = 4 #skip every nth row in each exchange pandas.DataFrame()


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


TOTAL_ARB = [] #a list of Arbitrage() objects, sorted by unixtime

class Arbitrage:
    def __init__(self, unixtime, buyExch, buyExchPrice, sellExch, sellExchPrice, arb):
        self.unixtime = unixtime
        self.buyExch = buyExch
        self.buyExchPrice = buyExchPrice
        self.sellExch = sellExch
        self.sellExchPrice = sellExchPrice
        self.arb = arb #in decimal
    def toString(self):
        fmtDate = datetime.datetime.fromtimestamp(self.unixtime).strftime('%Y-%m-%d %H:%M:%S')
        return str(fmtDate)+" BUY: "+self.buyExch+" ("+str(self.buyExchPrice)+") | SELL: "+self.sellExch+" ("+str(self.sellExchPrice)+") | ARB: "+str(self.arb*100.0)


#code from ../prototypes/check_arbitrage.py
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

#Method finds previous arbitrage opportunities using pandas.DataFrame()
#df1 - a pandas.DataFrame() of past bitcoin prices for a given exchange
#df1Exchange the exchange name of df1
#df2 - a pandas.DataFrame() of past bitcoin prices for a given exchange
#df2Exchange the exchange name of df2
#threshold - the minimum arbitrage opportunity that should be reported
def find_arbitrage(df1, df1Exchange, df2, df2Exchange, threshold):
    innerJoined = pandas.merge(df1, df2, on='unixtime', how='inner')
    marketPriceDict = {}
    for index, row in innerJoined.iterrows():
        marketPriceDict[df1Exchange] = float(row["price_x"])
        marketPriceDict[df2Exchange] = float(row["price_y"])
        arbData = arbitrage_difference_withfees(marketPriceDict, df1Exchange, df2Exchange)
        if (threshold<arbData[2]):
            TOTAL_ARB.append(Arbitrage(
                            int(row["unixtime"]),
                            arbData[0],
                            marketPriceDict[arbData[0]],
                            arbData[1],
                            marketPriceDict[arbData[1]],
                            arbData[2]))

            #fmtDate = datetime.datetime.fromtimestamp(int(row["unixtime"])).strftime('%Y-%m-%d %H:%M:%S')
            #print str(fmtDate)+" BUY: "+arbData[0]+" ("+str(marketPriceDict[arbData[0]])+") | SELL: "+arbData[1]+" ("+str(marketPriceDict[arbData[1]])+") | ARB: "+str(arbData[2]*100.0)
            #print "\n"








def main():
    #get the possible combinations of exchanges
    pandaDFdict = {} #dictionary mapping exchange name to its dataframe

    #get a pandas.DataFrame() for each exchange
    for exch in EXCHANGE_LIST:

        #dataframes have duplicate unixtime removed
        #dataframes have a skipping measure
        pandaDFdict[exch] = pandas.read_csv(CSV_DIR+exch+"USD.csv",
                                header=0,
                                names=["unixtime", "price", "volume"]).drop_duplicates(subset="unixtime").iloc[::SKIPS, :]

    combos = itertools.combinations(EXCHANGE_LIST, 2) #pick 2 at a time
    for combo in combos:
        find_arbitrage(pandaDFdict[combo[0]], combo[0], pandaDFdict[combo[1]], combo[1], THRESHOLD)

    TOTAL_ARB.sort(key=lambda x: x.unixtime)

    #DESIRED DATA
    startingPortfolio = 100
    for arbObject in TOTAL_ARB:
        #print arbObject.toString() #history of arbitrage
        startingPortfolio *= (arbObject.arb+1)
    print startingPortfolio
    print TOTAL_ARB[0].toString()

main()
