import check_arbitrage
import time

users = [('7247416248',['bitfenix','cexio'],.025),
         ('7248144801',['btce','bitstamp','cexio'], .017),
         ('1800999783',['bitfinex','bitstamp','cexio'], .010),
         ('4129383450',['bitstamp','kraken','cexio'], .017),

         ('7245381363',['kraken','bitfenix'], .017)]

EXCHANGELIST = ["bitfinex", "bitstamp", "cexio", "kraken"]
def loop():
    # Update list of arbitrage opportunities
    arbitrage_opportunities = check_arbitrage.handler(EXCHANGELIST)

    # Look through user list and alert users if a market they are interested in is above threshold
    for user in users:
        new_suggestions = []
        for opportunity in arbitrage_opportunities:
            if set(opportunity[0:2]).issubset(set(user[1])):
                if (opportunity[2] >= user[2]):
                    new_suggestions.append(opportunity)
        if(len(new_suggestions) > 0):
            print(user[0])
            for opportunity in new_suggestions:
                print("\t", str(opportunity[0]), " ", str(opportunity[1]), " ", str(opportunity[2]))
        # Message user with phone # = user[0] new_suggestions list if its len > 0

for i in check_arbitrage.handler(EXCHANGELIST):
    print i

while(True):
    print("CHECKING ARBITRAGE OPPORTUNITIES...")
    loop()
    print("...SLEEPING")
    time.sleep(5
