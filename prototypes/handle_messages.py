from twilio.rest import TwilioRestClient

#USER_DICT = {'+11234567890':([0,1],0.0)} #customer dictionary. format "number":{"markets":[marketList],"minArgbitrage":float}
USER_DICT = {}
EXCHANGE_LIST = ["bitfinex", "bitstamp", "cexio", "kraken"]
RESPONSE_DICT = {"newCust":"Welcom to BAO. Choose the bitcoin markets you currently have assets in: 1)bitfinex 2)bitstamp 3)cexio 4)kraken. Reply 'stop' to opt out","minArb":"What would you like your minimum arbitrage threshold to be?(percentage) Reply 'stop' to opt out","thank":"Thank you for using BOA. You will be receiving alerts when there is a valid arbitrage available","stop":"Thank you for using BOA. Text 'Join' to 724-806-1286 if you would like to join again.","invalidNum":"You must enter a number. Please try again","invalidCommand":"The command you entered is invalid. Valid commands are: reset or stop."}

accountSid = "AC410618cdbef7d152a5b5b265e70d06cb" # test account sid
authToken  = "fcb8105a8fe161a207d7d87680ee63bc"  # test auth token
client = TwilioRestClient(accountSid, authToken)

#send message to a user
def send_message(userNumber,message):
    message = client.messages.create(to=userNumber,
    from_="+17248061286",
    body=message)
    return message.status

#lists all messages
def receive_messages():
    messages = client.messages.list(to="+17248061286") #only get messages sent to us
    return messages

#parse user message
#phoneNumber and message are strings
def handle_message(phoneNumber,message):
    if(message.lower() == "reset"): #user wants to select new markets
        print "Reset"
        #del USER_DICT[phoneNumber]
        USER_DICT[phoneNumber] = ([],0.0) #reset values
        send_message(phoneNumber,RESPONSE_DICT["newCust"])
        return

    elif(message.lower() == "stop"):
        print "Stop"
        del USER_DICT[phoneNumber] #remove customer from dictionary
        send_message(phoneNumber,RESPONSE_DICT["stop"])
        return

    elif(phoneNumber not in USER_DICT): #new customer
        print "New user"
        USER_DICT[phoneNumber] = ([],0.0)
        send_message(phoneNumber,RESPONSE_DICT["newCust"]) #new customer message
        return

    elif(USER_DICT[phoneNumber][0] == []): #user message contains markets to follow
        print "Get exchanges"
        exchanges = [] #temp list of exchanges from message
        valid = True
        for i in range(len(message)):
            if(int(message[i])-1 < 0 or int(message[i])-1 >= len(EXCHANGE_LIST)): #invalid number entry
                send_message(phoneNumber,RESPONSE_DICT["invalidNum"]) #let user know
                valid = False
                break
            else:
                exchanges.append(EXCHANGE_LIST[int(message[i])-1]) #add each exchange to list
        #user has sent valid message
        if(valid):
            USER_DICT[phoneNumber] = (exchanges,USER_DICT[phoneNumber][1])
            send_message(phoneNumber,RESPONSE_DICT["minArb"])
        return

    elif(USER_DICT[phoneNumber][1] == 0.0):
        print "get arbitrage"
        if(float(message)>100 or float(message<0)):
            send_message(phoneNumber,RESPONSE_DICT["invalidNum"])
        else:
            USER_DICT[phoneNumber] = (USER_DICT[phoneNumber][0],float(message)/100.0) #set customers min arb value
            send_message(phoneNumber,RESPONSE_DICT["thank"])
        return

    else:
        print "invalid command"
        send_message(phoneNumber,RESPONSE_DICT["invalidCommand"])
        return



#Returns True if there is a new message
def get_next_message():
    messages = receive_messages() #get messages
    if(len(messages) > currentMessage["index"]+1): #check if there is a new message
        currentMessage["index"] += 1 #set new index for currentMessage
        m = messages[currentMessage["index"]] #get next message

        #update currentMessage info
        currentMessage["from"] = m.from_
        currentMessage["body"] = m.body
        return True

#testing
'''
currentMessage = {"index":-1,"sid":0,"from_":"+11111111111","body":"Some message"} #index of last message handled to check if there's a new message

while(get_next_message() == True):
    print currentMessage["body"]
'''
handle_message("+17248417560","Hello") #new phone number
print USER_DICT
handle_message("+17248417560","12") #set markets
print USER_DICT

handle_message("+17248417560","2") #set arbitrage
print USER_DICT

handle_message("+17248417560","reset") #reset values
print USER_DICT
"""
handle_message("+17248417560","12") #set markets
print USER_DICT
handle_message("+17248417560","2") #set arbitrage
print USER_DICT
"""
handle_message("+17248417560","stop") #delete user
print USER_DICT
