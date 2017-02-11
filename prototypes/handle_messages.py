from twilio.rest import TwilioRestClient
import global_data
import time

#possible responses to user input
RESPONSE_DICT = {"newCust":"Welcom to BAO.","exchanges": "Choose the bitcoin markets you currently have assets in (ex: 1234 for all): ","minArb":"What would you like your minimum arbitrage threshold to be?(percentage)","thank":"Thank you for using BOA. You will be receiving alerts when there is a valid arbitrage available. Reply 'stop' to opt out","invalidExchange":"Enter the exchanges as one number (ex: 1234 for all)","invalidArb":"Enter the percentage like 1.5% = 1.5","invalidCommand":"The command you entered is invalid. Valid commands are: reset or stop."}

accountSid = "AC410618cdbef7d152a5b5b265e70d06cb" # test account sid
authToken  = "fcb8105a8fe161a207d7d87680ee63bc"  # test auth token
client = TwilioRestClient(accountSid, authToken)

def load_exchange_response():
    i=0
    for j in global_data.EXCHANGE_LIST:
        RESPONSE_DICT["exchanges"]+= "\n"+str(i+1)+") "+j[1]
        print i
        i += 1


#send message to a user
def send_message(userNumber,message):

    connected = 0
    while(connected == 0):
        try:
            message = client.messages.create(to=userNumber,
            from_="+17248061286",
            body=message)
            connected = 1
        except:
            time.sleep(1)

    return message.status

#parse user message
#phoneNumber and message are strings
def handle_message(message):
    if(message.body.lower() == "reset"): #user wants to select new markets
        print "Reset"
        global_data.USER_DICT[message.from_] = ([],0.0) #reset values
        send_message(message.from_,RESPONSE_DICT["exchanges"])
        return

    elif(message.body.lower() == "stop"): #twilio handles unsubscribe message
        print "Stop"
        if(message.from_ in global_data.USER_DICT):
            del global_data.USER_DICT[message.from_] #remove customer from dictionary
        return

    elif(message.from_ not in global_data.USER_DICT): #new customer
        print "New user"
        global_data.USER_DICT[message.from_] = ([],0.0)

        send_message(message.from_,RESPONSE_DICT["newCust"]+RESPONSE_DICT["exchanges"]) #new customer message
        return

    elif(global_data.USER_DICT[message.from_][0] == []): #user message contains markets to follow
        print "Get exchanges"
        exchanges = [] #temp list of exchanges from message
        valid = True

        for i in range(len(message.body)):
            try:
                int(message.body[i])
            except ValueError:
                send_message(message.from_,RESPONSE_DICT["invalidExchange"])
                return

            if(int(message.body[i])-1 < 0 or int(message.body[i])-1 >= len(global_data.EXCHANGE_LIST)): #invalid number entry
                send_message(message.from_,RESPONSE_DICT["invalidExchange"]) #let user know
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
            send_message(message.from_,RESPONSE_DICT["invalidArb"])
            return

        if(float(message.body)>100 or float(message.body<0)):
            send_message(message.from_,RESPONSE_DICT["invalidArb"])
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
def get_next_message():
    f = open("last_sid.txt", "r")
    lastSid = f.read()
    f.close()
    try:
        messages = client.messages.list(to="+17248061286") #get messages
    except:
        return

    i=0
    print "message sid: "+messages[i].sid+"last sid:    "+lastSid
    while(messages[i].sid != lastSid.rstrip('\n')): #check if there is at least 1 new message
        m = messages[i] #get next message
        print "current sid: "+m.sid
        print "last sid:    "+lastSid
        # print m.body
        # print m.from_
        handle_message(m)
        time.sleep(1.5)
        i += 1

    lastSid = messages[0].sid
    f = open("last_sid.txt", "w")
    f.write(lastSid)
    f.close()
    print "lastSid: "+lastSid
    #return currentSid

#testing
# print RESPONSE_DICT["exchanges"]
# load_exchange_response()
# print RESPONSE_DICT["exchanges"]
#
# while (True):
#     currentSid = get_next_message() #new phone number
#     print global_data.USER_DICT
