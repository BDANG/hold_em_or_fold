import pandas
import itertools
import csv
CSV_DIR = "/Users/briandang/Downloads/"
EXCHANGE_LIST = ["bitfinex", "bitstamp", "btce", "kraken"]
THRESHOLD = .02

#Method finds previous arbitrage opportunities using pandas.DataFrame()
#threshold - the minimum arbitrage opportunity that should be reported
def find_arbitrage(df1, df1Exchange, df2, df2Exchange, threshold):
    innerJoined = pandas.merge(df1, df2, on='unixtime', how='inner')
    for index, row in innerJoined.iterrows():

        print str(index)+" "+str(row["price_x"])+" "+str(row["price_y"])




def main():
    #get the possible combinations of exchanges
    pandaDFdict = {} #dictionary mapping exchange name to its dataframe
    for exch in EXCHANGE_LIST:
        pandaDFdict[exch] = pandas.read_csv(CSV_DIR+exch+".csv", header=0, names=["unixtime", "price", "volume"])


    combos = itertools.combinations(EXCHANGE_LIST, 2) #pick 2 at a time
    for combo in combos:
        find_arbitrage(pandaDFdict[combo[0]], combo[0], pandaDFdict[combo[1]], combo[1], THRESHOLD)

main()
