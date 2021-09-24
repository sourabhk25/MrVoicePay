import MySQLdb
import credential
import json
from decimal import Decimal

def getAllUser():
    response_text =[]
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    sql = """select * from user"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            userid = row[0]
            username  = row[1]
            firstname = row[2]
            lastname = row[3]
            mobile = row[4]
            address = row[5]
            response_text.append({'USERID':userid,'USERNAME':username,'FIRSTNAME':firstname,'LASTNAME':lastname,'MOBILE':mobile,'ADDRESS':address})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getAllUser in ",credential.database)
        db.rollback()
    db.close()
    return response_text

def getPassCode(userid):
    response_text = {}
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    sql = """select * from quicklogin where userid = """+str(userid)+""";"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 1:
            for row in results:
                userid = row[0]
                passcode  = row[1]
                response_text = {'MESSAGE':'VALID USER','USERID':userid,'PASSCODE':passcode}
        else:
            response_text = {'MESSAGE':'INVALID USER', 'USERID': userid, 'PASSCODE': 'NA'}
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getPassCode in ",credential.database)
        db.rollback()
    db.close()
    return response_text

def getUserid(username):
    response_text = {'MESSAGE':'SOMETHING WENT WRONG', 'USERID': "NA","USERNAME":"NA" , 'FLAG': "False"}
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    sql = """select * from user where username = '""" + str(username) + """';"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 1:
            for row in results:
                userid = row[0]
                response_text = {'MESSAGE':'VALID USER','USERID':userid,'usename':username,'FLAG':"True"}
        else:
            response_text = {'MESSAGE':'INVALID USER', 'USERID': "NA","USERNAME":"NA" , 'FLAG': "False"}
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getUserid in ",credential.database)
        db.rollback()
    db.close()
    return response_text

def checkBalance(userid):
    response_text = {'MESSAGE': 'SOMETHING WENT WRONG','FLAG': "False"}
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    try:
        sql = """select * from account where userid = """ + str(userid) + """;"""
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 1:
            for row in results:
                balance = row[2]
                response_text = {"MESSAGE":"VALID USERID","BALANCE":balance,"FLAG":"True"}
        else:
            response_text = {'MESSAGE': 'USERID NOT FOUND INSIDE ACCOUNT','FLAG': "False"}
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at checkBalance in ", credential.database)
        db.rollback()
    db.close()
    return response_text

def checkBalanceUsername(username):
    response_text = json.loads(json.dumps(getUserid(username)))
    if(response_text["FLAG"]=="True"):
        return checkBalance(response_text["USERID"])
    return response_text

def performTransaction(from_username,to_username,amount):
    check_from_user = getUserid(from_username)
    check_from_user = json.loads(json.dumps(check_from_user))
    if(check_from_user["FLAG"]=="False"):
        print (check_from_user["MESSAGE"])
        return {"MESSAGE":"FROM USER NAME DOSE NOT EXISTS","FLAG":"False"}
    from_userid = check_from_user["USERID"]
    check_to_user = getUserid(to_username)
    check_to_user = json.loads(json.dumps(check_to_user))
    if (check_to_user["FLAG"]=="False"):
        print (check_to_user["MESSAGE"])
        return {"MESSAGE":"USER NAME DOES NOT EXISTS","FLAG":"False"}
    to_userid = check_to_user["USERID"]
    return debitAmount(from_userid,to_userid,amount)

def debitAmount(fromUserID,toUserID,amount):
    response_text = {'MESSAGE': 'SOMETHING WENT WRONG', 'FLAG': "False"}
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    try:
        sql = """select * from account where userid = """ + str(fromUserID) + """;"""
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 1:
            for row in results:
                balance = row[2]
                if (Decimal(balance) >= Decimal(amount)):
                    balance = Decimal(Decimal(balance)-Decimal(amount))
                    sql = """update account set balance = """+str(balance)+""" where userid = """+str(fromUserID)+""";"""
                    cursor.execute(sql)
                    sql = """select * from account where userid = """ + str(toUserID) + """;"""
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    if len(results) == 1:
                        for row in results:
                            balance = row[2]
                            balance = Decimal(Decimal(balance) + Decimal(amount))
                            sql = """update account set balance = """ + str(balance) + """ where userid = """ + str(toUserID) + """;"""
                            cursor.execute(sql)
                            sql = """insert into transaction(fromUid,toUid,amount) values ("""+str(fromUserID)+""","""+str(toUserID)+""","""+str(amount)+""");"""
                            cursor.execute(sql)
                    response_text = {'MESSAGE': 'PAYMENT SUCCESS', 'FLAG': "True"}
                else:
                    response_text = {'MESSAGE': 'INSUFFICIENT ACCOUNT BALANCE', 'FLAG': "False"}
        else:
            response_text = {'MESSAGE': 'USERID NOT FOUND INSIDE ACCOUNT', 'FLAG': "False"}
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at debitAmount in ", credential.database)
        db.rollback()
    db.commit()
    db.close()
    return response_text

def getTransaction(userid):
    response_text = []
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    sql = """select username, amount,ts from ( (select * from transaction where fromUid="""+str(userid)+""" order by ts desc limit 5) as a join (select * from user) as b on (a.toUid=b.userid))"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            username = row[0]
            amount = row[1]
            time = row[2]
            response_text.append({"USERNAME":username,"AMOUNT":amount,"TIME":time})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getTransaction in ", credential.database)
        db.rollback()
    db.close()
    return response_text

def getSentences(userid):
    response_text = []
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    sql = """select * from sentences where userid="""+str(userid)+""";"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            userid = row[0]
            question = row[1]
            answer = row[2]
            response_text.append({"USERID": userid, "QUESTION": question, "ANSWER": answer})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getTransaction in ", credential.database)
        db.rollback()
    db.close()
    return response_text

def checkTransaction(userid):
    response_text = {'MESSAGE': 'SOMETHING WENT WRONG', 'FLAG': "False","BALANCE":"0"}
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    try:
        sql = """select sum(amount) as sum from transaction where ts>=now()-interval 24 hour and fromUid="""+str(userid)+""" group by fromUid;"""
        cursor.execute(sql)
        results = cursor.fetchall()
        print (results,len(results))
        if len(results) == 0:
            response_text = {'MESSAGE': 'USERID NOT FOUND INSIDE ACCOUNT', 'FLAG': "True","BALANCE":"0"}
        else:
            for row in results:
                balance = row[0]
                response_text = {"MESSAGE": "VALID USERID", "BALANCE": balance, "FLAG": "True"}
            # response_text = {'MESSAGE': 'USERID NOT FOUND INSIDE ACCOUNT', 'FLAG': "True"}
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at checkBalance in ", credential.database)
        db.rollback()
    db.close()
    return response_text

#print (getTransaction(5629290))

#print (performTransaction('sourabh','dhruv',15))
#print (checkBalanceUsername("dhruv"))

#select username, amount,ts from ( (select * from transaction where fromUid=5629290 order by ts desc limit 5) as a join (select * from user) as b on (a.toUid=b.userid));
