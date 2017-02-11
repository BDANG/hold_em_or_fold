from twilio.rest import TwilioRestClient
import global_data
import time

global currentSid

#possible responses to user input
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

#parse user message
#phoneNumber and message are strings
def handle_message(message):
    if(message.body.lower() == "reset"): #user wants to select new markets
        print "Reset"
        global_data.USER_DICT[message.from_] = ([],0.0) #reset values
        send_message(message.from_,RESPONSE_DICT["newCust"])
        return

    elif(message.body.lower() == "stop"): #twilio handles unsubscribe message
        print "Stop"
        del global_data.USER_DICT[message.from_] #remove customer from dictionary
        return

    elif(message.from_ not in global_data.USER_DICT): #new customer
        print "New user"
        global_data.USER_DICT[message.from_] = ([],0.0)

        send_message(message.from_,RESPONSE_DICT["newCust"]) #new customer message
        return

    elif(global_data.USER_DICT[message.from_][0] == []): #user message contains markets to follow
        print "Get exchanges"
        exchanges = [] #temp list of exchanges from message
        valid = True

        for i in range(len(message.body)):
            try:
                int(message.body[i])
            except ValueError:
                send_message(message.from_,RESPONSE_DICT["invalidNum"])
                return

            if(int(message.body[i])-1 < 0 or int(message.body[i])-1 >= len(global_data.EXCHANGE_LIST)): #invalid number entry
                send_message(message.from_,RESPONSE_DICT["invalidNum"]) #let user know
                valid = False
                break
            else:
                exchanges.append(global_data.EXCHANGE_LIST[int(message.body[i])-1]) #add each exchange to list
        #user has sent valid message
        if(valid):
            global_data.USER_DICT[message.from_] = (exchanges,global_data.USER_DICT[message.from_][1])
            send_message(message.from_,RESPONSE_DICT["minArb"])
        return

    elif(global_data.USER_DICT[message.from_][1] == 0.0):
        print "get arbitrage"
        try:
            float(message.body)
        except ValueError:
            send_message(message.from_,RESPONSE_DICT["invalidNum"])
            return

        if(float(message.body)>100 or float(message.body<0)):
            send_message(message.from_,RESPONSE_DICT["invalidNum"])
        else:
            global_data.USER_DICT[message.from_] = (global_data.USER_DICT[message.from_][0],float(message.body)/100.0) #set customers min arb value
            send_message(message.from_,RESPONSE_DICT["thank"])
        return

    else:
        print "invalid command"
        send_message(message.from_,RESPONSE_DICT["invalidCommand"])
        return



#Returns True if there is a new message
#False otherwise
def get_next_message(currentSid):
    messages = client.messages.list(to="+17248061286") #get messages

    i=0
    while(messages[i].sid != currentSid): #check if there is at least 1 new message
        m = messages[i] #get next message
        print "new sid "+m.sid
        print "current sid "+currentSid
        # print m.body
        # print m.from_
        handle_message(m)
        time.sleep(1.5)
        i += 1

    currentSid = messages[0].sid
    print "currentSid "+currentSid
    return currentSid
#testing
currentSid = "SMceb52e964476d36ac11bbae9f0361a23"

while (True):
    currentSid = get_next_message(currentSid) #new phone number
    print global_data.USER_DICT
