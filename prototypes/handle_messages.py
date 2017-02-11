from twilio.rest import TwilioRestClient

CUSTOMER_DICT = {'+11234567890':{"markets":["market1","market2"],"minArbitrage":0.02}} #customer dictionary. format "number":{"markets":[marketList],"minArgbitrage":float}
MARKET_LIST = ["market1","market2"] #list of markets
RESPONSE_LIST = ["Welcom to BAO. Choose the bitcoin markets you currently have assets in: 1)market1 2)market2"]

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
def handle_message(phoneNumber,message):
    if(CUSTOMER_DICT.get(phoneNumber) == None): #new customer
        sendMessage(phoneNumber,responses[0]) #new customer message
    elif(CUSTOMER_DICT.get(phoneNumber) == ""): #retreive markets to enter from user
        for i in range(len(message)):
            CUSTOMER_DICT[phoneNumber].append(i) #add each market to user profile
    elif(message.lower() == "yes"):
        return True
    elif(message.lower() == "no"):
        return False


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
currentMessage = {"index":-1,"sid":0,"from_":"+11111111111","body":"Some message"} #index of last message handled to check if there's a new message

while(get_next_message() == True):
    print currentMessage["body"]
