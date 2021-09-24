# importing the requests library
import requests
import json
# api-endpoint
# URL = "http://35.240.203.4:5000/getpasscode"
# r = requests.post(url=URL,json = json.loads(json.dumps({"userid":"5629290"})))
# data = r.json()
# # print (data["PASSCODE"])
# code = 730685
# to_username = "dhruv"
# amount = 500
#
# URL = "http://35.240.203.4:5000/getpasscode"
# r = requests.post(url=URL, json=json.loads(json.dumps({"USERID": "5629290"})))
# data = r.json()
# #logger.info("************")
# correct_passcode = data["PASSCODE"]
# if str(code) == str(correct_passcode):
#     URL = "http://35.240.203.4:5000/performTransaction"
#     r = requests.post(url=URL, json=json.loads(
#         json.dumps({"FROM_USERNAME": "sourabh", "TO_USERNAME": to_username, "AMOUNT": amount})))
#     data = r.json()
#     #logger.info("+++++++++++++")
#     speech_text = data["MESSAGE"]
# else:
#     speech_text = "Passcode dose not match please try it once again."
#
# print(speech_text)
# s = "datetime.datetime(2019, 9, 18, 8, 12, 38)"
# ss = s.split("(")[1].split(")")[0].split(", ")
# for e in ss:
#     print(e,"n")
def createSpeechForTransaction(data):
    speech_text = ""
    for o in data:
        speech_text = speech_text + (createSpeechForTransactionFromObject(o))
    return speech_text

def createSpeechForTransactionFromObject(o):
    username = o["USERNAME"]
    amount = o["AMOUNT"]
    timestamp = o["TIME"]
    speech_text = str(amount)+" rupees to "+str(username)+", on "+str(speakTime(str(timestamp)))
    return speech_text

month = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}

def speakTime(time):
    ss = time.split("(")[1].split(")")[0].split(", ")
    spech_text = ss[2]+" "+month[ss[1]]+" "+ss[0]+" on "+ss[3]+" hours, "+ss[4]+" minutes and "+ss[5]+" second GMT."
    return spech_text

print (createSpeechForTransaction(json.loads(json.dumps([{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"}]))))

print (len(json.loads(json.dumps([{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"},{"USERNAME":"DHRUV","AMOUNT":78,"TIME":"datetime.datetime(2019, 9, 18, 8, 12, 38)"}]))))
