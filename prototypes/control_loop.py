import check_arbitrage
import time
import global_data
import handle_messages

'''
users = {'7247416248':(['bitfenix','cexio'],.025),
         '7248144801':(['btce','bitstamp','cexio'], .017),
         '1800999783':(['bitfinex','bitstamp','cexio'], .010),
         '4129383450':(['bitstamp','kraken','cexio'], .017),
         '7245381363':(['kraken','bitfenix'], .017)}
EXCHANGELIST = ["bitfinex", "bitstamp", "cexio", "kraken"]
'''
active_suggestions = {}
def loop():
    # Update list of arbitrage opportunities

    arbitrage_opportunities = check_arbitrage.handler(global_data.EXCHANGE_LIST)
    for i in arbitrage_opportunities:
        print i

    # Look through user list and alert users if a market they are interested in is above threshold
    for phoneNum, info in global_data.USER_DICT.iteritems():
        new_suggestions = []
        for opportunity in arbitrage_opportunities:
            if set(opportunity[0:2]).issubset(set(info[0])) and (opportunity[2] >= info[1]) and info[0] > 0:

                if(phoneNum in active_suggestions):
                    users_active_suggestions = active_suggestions[phoneNum]
                else:
                    users_active_suggestions = []
                matched = 0
                for active_suggestion in users_active_suggestions:
                    if (active_suggestion[0] == opportunity[0] and active_suggestion[1] == opportunity[1]):
                        matched = 1
                        break
                if(matched == 0):
                    new_suggestions.append(opportunity)

        # Add new suggestions to active list and display
        if(len(new_suggestions) > 0):
            if(phoneNum in active_suggestions):
                active_suggestions[phoneNum] = active_suggestions[phoneNum] + new_suggestions
            else:
                active_suggestions[phoneNum] = new_suggestions
            # Message user with phone # = user[0] new_suggestions list if its len > 0
            print(phoneNum)
            print("\tNEW:")
            for opportunity in new_suggestions:
                print("\t\t" + "  ".join(str(i) for i in opportunity))
            print("\tACTIVE:")
            for active in active_suggestions[phoneNum]:
                print("\t\t" + "  ".join(str(i) for i in active))

        if phoneNum in active_suggestions:
            expired_opportunities = []
            for active_opportunity in active_suggestions[phoneNum]:
                matched = 0
                for current_opportunity in arbitrage_opportunities:
                    if current_opportunity[0] == active_opportunity[0] and current_opportunity[1] == active_opportunity[1] and current_opportunity[2] >= (global_data.USER_DICT[phoneNum][1]*.97):
                        matched = 1
                        break
                if matched == 0:
                    expired_opportunities.append(active_opportunity)
            active_suggestions[phoneNum] = list(set(active_suggestions[phoneNum]) - set(expired_opportunities))


    print("ACTIVE OPPORTUNITIES")
    print(active_suggestions)



while(True):
    print("Getting new messages...")
    global_data.currentSid = handle_messages.get_next_message(global_data.currentSid)
    print("\n\n\nCHECKING ARBITRAGE OPPORTUNITIES...\n")
    loop()
    print("\n...SLEEPING")
    time.sleep(10)
