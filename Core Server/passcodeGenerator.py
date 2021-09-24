import time
import random
import MySQLdb
import credential

def start():
    while True:
        userids = []
        db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
        cursor = db.cursor()
        sql = """select userid from user"""
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                userid = row[0]
                userids.append(userid)
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print (e)
            print ("at getAllUser in ", credential.database)
            db.rollback()
        print (userids)
        db.commit()
        for userid in userids:
            updateDetails(userid)
        time.sleep(10)


def updateDetails(userid):
    db = MySQLdb.connect(credential.ip, credential.username, credential.password, credential.database)
    cursor = db.cursor()
    try:
        sql = """update quicklogin set passcode = """ + str(getNewCode()) + """ where userid=""" + str(userid) + """;"""
        print (sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getAllUser in ", credential.database)
        db.rollback()
    db.commit()

def getNewCode():
    return int(random.randrange(100000, 999999))


start()
