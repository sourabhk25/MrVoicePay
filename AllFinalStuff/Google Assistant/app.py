import requests
import json
from decimal import Decimal

USERNAME = "dhruv"
USERID = 5629291
MAX_PAYMENT=2000

def verifyPasscode(code):
    speech_text = ""
    temp = getFileContent()

    if "USERNAME" in temp:
        to_username = temp["USERNAME"]
        amount = temp["AMOUNT"]
        
        URL = "http://35.240.203.4:5000/getpasscode"
        r = requests.post(url=URL,json = json.loads(json.dumps({"USERID":USERID})))
        data = r.json()
        correct_passcode = data["PASSCODE"]
        print ("*************",str(code),str(correct_passcode),"*************")
        temp = str(int(code)).replace(" ","")
        if temp==str(correct_passcode):
            URL = "http://35.240.203.4:5000/performTransaction"
            r = requests.post(url=URL,json = json.loads(json.dumps({"FROM_USERNAME":USERNAME,"TO_USERNAME":to_username,"AMOUNT":amount})))
            data = r.json()
            speech_text = data["MESSAGE"]
            clearTheFile()
        else:
            speech_text = "Passcode dose not match, please try it once again."
    else:
        speech_text = "At present there is no requirement of passcode."
    return speech_text

def payToOtherUser(to_username,amount):
    clearTheFile()
    speech_text  =  ""
    to_username.lower()
    URL = "http://35.240.203.4:5000/checkTransaction"
    r = requests.post(url=URL,json = json.loads(json.dumps({"USERID":USERID})))
    data = r.json()
    if (data["FLAG"]=="True"):
        debited_amount = data["BALANCE"]
        if (Decimal(amount)+Decimal(debited_amount)<=MAX_PAYMENT):
            URL = "http://35.240.203.4:5000/performTransaction"
            r = requests.post(url=URL,json = json.loads(json.dumps({"FROM_USERNAME":USERNAME,"TO_USERNAME":to_username,"AMOUNT":amount})))
            data = r.json()
            speech_text = data["MESSAGE"]
        else:
            # handler_input.attributes_manager.session_attributes["FROM_USERNAME"] = to_username
            # handler_input.attributes_manager.session_attributes["AMOUNT"] = amount
            # save username and amount into files
            writeInFile(to_username,amount)
            speech_text = "Your last 24 hour transaction will be greater than decided limit. It will require passcode now for processing."
    else:
        speech_text = "Something is not right with checking transaction way. please try again later."
    return speech_text

def clearTheFile():
    temp = {"temp":"temp"}
    file1 = open("myfile.txt", "w")
    file1.write(str(temp))
    file1.close()

def writeInFile(to_username,amount):
    temp = {"USERNAME":str(to_username),"AMOUNT":str(amount)}
    file1 = open("myfile.txt", "w")
    file1.write(str(temp))
    file1.close()

def getFileContent():
    file1 = open("myfile.txt", "r+")
    string_value = file1.read()
    temp = eval(string_value)
    return temp


def checkBalance():
    clearTheFile()
    speech_text  =  ""

    URL = "http://35.240.203.4:5000/checkBalance"
    r = requests.post(url=URL,json = json.loads(json.dumps({"USERNAME":USERNAME})))
    data = r.json()

    if ( data["FLAG"]=="True" ):
        balance = data["BALANCE"]
        balance = float("{0:.2f}".format(Decimal(balance)))
        speech_text = "your account balance is "+str(balance)
    else:
        message = data["MESSAGE"]
        speech_text = str(message)

    return speech_text

def checkTransaction():
    clearTheFile()
    speech_text  =  ""
    URL = "http://35.240.203.4:5000/transaction"
    r = requests.post(url=URL,json = json.loads(json.dumps({"USERID":USERID})))
    data = r.json()

    if ( data["FLAG"]=="True" ):
        trans = data["DATA"]
        speech_text = createSpeechForTransaction(trans)
    else:
        message = data["MESSAGE"]
        speech_text = str(message)
    if len(speech_text)==0:
        speech_text="There are no previous transactions"
    return speech_text

def createSpeechForTransaction(data):
    speech_text = ""
    for o in data:
        speech_text = speech_text + (createSpeechForTransactionFromObject(o))
    return speech_text

def createSpeechForTransactionFromObject(o):
    username = o["USERNAME"]
    amount = o["AMOUNT"]
    timestamp = o["TIME"]
    speech_text = " "+str(amount)+" rupees to "+str(username)+", on "+str(timestamp)+". "
    return speech_text
