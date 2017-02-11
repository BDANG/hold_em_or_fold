import pickle
import numpy
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
FUTURE_CHECK = 3600 #how many seconds into the future to check if the sell exchange upheld price
SAVE_DATAFRAME_AND_ARB_LIST = False #True if you want to pickle the data frame and Arbitrage list
LOAD_DATAFRAME_AND_ARB_LIST = False #True if you HAVE the pickled data frame and Arbitrage list


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
#Method is only called if LOAD_DATAFRAME_AND_ARB_LIST == False
#df1 - a pandas.DataFrame() of past bitcoin prices for a given exchange
#df1Exchange the exchange name of df1
#df2 - a pandas.DataFrame() of past bitcoin prices for a given exchange
#df2Exchange the exchange name of df2
#threshold - the minimum arbitrage opportunity that should be reported
def find_arbitrage(df1, df1Exchange, df2, df2Exchange, threshold):
    innerJoined = pandas.merge(df1, df2, on='unixtime', how='inner') #combine the exchange dataframes based on time
    marketPriceDict = {} #use df data to populate for arbitrage_difference_withfees()

    global TOTAL_ARB #appending to the list in the for loop
    for index, row in innerJoined.iterrows():#iterate through the entries of the same time
        marketPriceDict[df1Exchange] = float(row["price_x"]) #populate dict for method call
        marketPriceDict[df2Exchange] = float(row["price_y"])
        arbData = arbitrage_difference_withfees(marketPriceDict, df1Exchange, df2Exchange)
        if (threshold<arbData[2]): #report arbitrage greater than threshold
            TOTAL_ARB.append(Arbitrage(
                                int(row["unixtime"]),
                                buyExch = arbData[0],
                                buyExchPrice = marketPriceDict[arbData[0]],
                                sellExch = arbData[1],
                                sellExchPrice = marketPriceDict[arbData[1]],
                                arb = arbData[2]))

#Method checks the forward/future price from an arbitrage opportunity
#Profit is secured when the BTC on a buy exchange is moved to the sell exchange
#and then sold
#arbObject an Arbitrage object holding an arbitrage opportunity
#pandaDF - the pandas.DataFrame() corresponding to the historical exchange data for the arbObject.sellExch
#time in SECONDS of how far into the future to look
def check_forward_price(arbObject, pandaDF, time):
    allowableWindow = 240 #+/- the seconds for (arbObject.unixtime+time)
    previousPrice = arbObject.sellExchPrice
    futureTime = arbObject.unixtime+time
    #timewindow = numpy.linspace(futureTime-allowableWindow, futureTime+allowableWindow, ((futureTime+allowableWindow)-((futureTime-allowableWindow))))
    #print len(timewindow)
    #print pandaDF.loc[pandaDF["unixtime"].isin(timewindow)]

    minTimeDF = pandaDF['unixtime'] > futureTime-allowableWindow
    #print minTimeDF
    maxTimeDF = pandaDF['unixtime'] < futureTime+allowableWindow
    #print timeDF
    timeDF = pandaDF[minTimeDF & maxTimeDF]
    try:
        futurePrice = timeDF.iloc[0]['price']
    except:
        return False
    if previousPrice<=futurePrice:
        return True
    else:
        return False

def load():
    fTotalArbList = open("list_of_total_arbitrageobjects.dat", "rb")
    totalArbList = pickle.load(fTotalArbList)
    fTotalArbList.close()

    fpandaDFdict = open("dict_of_pandaDF.dat", "rb")
    pandaDFdict = pickle.load(fpandaDFdict)
    fpandaDFdict.close()
    return totalArbList, pandaDFdict


def save(totalArbList, pandaDFdict):
    fTotalArbList = open("list_of_total_arbitrageobjects.dat", "wb")
    pickle.dump(totalArbList, fTotalArbList)
    fTotalArbList.close()

    fpandaDFdict = open("dict_of_pandaDF.dat", "wb")
    pickle.dump(pandaDFdict, fpandaDFdict)
    fpandaDFdict.close()


#Iterate through each exchange combination and find the arbitrage
#that existed between pair in the past
def main():
    global TOTAL_ARB
    pandaDFdict = {} #dictionary mapping exchange name to its dataframe
    if (not LOAD_DATAFRAME_AND_ARB_LIST):
        #populate a pandas.DataFrame() for each exchange
        for exch in EXCHANGE_LIST:
            #dataframes have duplicate unixtime removed and have a skipping measure
            pandaDFdict[exch] = pandas.read_csv(CSV_DIR+exch+"USD.csv",
                                    header=0,
                                    names=["unixtime", "price", "volume"]).drop_duplicates(subset="unixtime").iloc[::SKIPS, :]

        combos = itertools.combinations(EXCHANGE_LIST, 2) #pick 2 at a time
        for combo in combos:
            find_arbitrage(pandaDFdict[combo[0]], combo[0], pandaDFdict[combo[1]], combo[1], THRESHOLD)

        TOTAL_ARB.sort(key=lambda x: x.unixtime)
    else:
        TOTAL_ARB, pandaDFdict = load()


    if (SAVE_DATAFRAME_AND_ARB_LIST):
        save(TOTAL_ARB, pandaDFdict)

    #report the arbitrage that had chances of securing profit
    for arbObject in TOTAL_ARB:
        if (check_forward_price(arbObject, pandaDFdict[arbObject.sellExch], FUTURE_CHECK)):
            print arbObject.toString()
            print arbObject.sellExch+" maintained price for secured profit.\n"

    #DESIRED DATA example
    #for arbObject in TOTAL_ARB:
        #print arbObject.toString() #total history of arbitrage



main()
