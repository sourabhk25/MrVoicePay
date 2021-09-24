import MySQLdb

def verify(mobile,password):
    temp =[]
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """SELECT * FROM EMP WHERE MOBILENO="""+str(mobile)+""" AND PASSWORD='"""+str(password)+"""' ;"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        i = 0
        for row in results:
            temp.append({'result':0,'empid':row[0],'name':row[1]})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at verify() in ydatabase")
        db.rollback()
    db.close()
    if len(temp)==0:
    	temp.append({'result':1})
    return temp

def addFarm(owner,mobileno,address,gps,prime,empid):
    temp={}
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """INSERT INTO FARM(OWNER,MOBILENO,ADDRESS,GPS,PRIME,EMPID) VALUES('"""+str(owner)+"""',"""+str(mobileno)+""",'"""+str(address)+"""','"""+str(gps)+"""','"""+str(prime)+"""',"""+str(empid)+""");"""
    sql2 = """SELECT LAST_INSERT_ID();"""
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        result = cursor.fetchone()
        temp['result'] = 0
        temp['farmid']=result[0]
        db.commit()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at addFarm in ydatabase")
        temp['result'] = 1
        db.rollback()
    db.close()
    return temp

def addAnimal(farmid,name,category,empid):
    temp={}
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """INSERT INTO ANIMAL(FARMID,NAME,CATEGORY,EMPID) VALUES('""" + str(farmid) + """','""" + str(
        name) + """','""" + str(category) + """',""" + str(empid) + """ );"""
    sql2 = """SELECT LAST_INSERT_ID();"""
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        result = cursor.fetchone()
        temp['result'] = 0
        temp['animalid'] = result[0]
        db.commit()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("--- at addAnimal in ydatabase")
        temp['result'] = 1
        db.rollback()
    db.close()
    return temp

def addData(values):
    x = values.split("&")
    temp = {}
    if (len(x)!=7):
        temp['result'] = 'fail'
        return temp
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    try:
        lsb = int(x[4])
        msb = int(x[5])
        if (lsb<0):
            lsb = 256-abs(lsb)
        if (msb<0):
            msb = 256-abs(msb)
        msb = msb<<8
        step = msb+lsb
        sql = """INSERT INTO DATA(ANIMALID,X,Y,Z,AX,AY,AZ) VALUES (""" + str(x[0]) + """,""" + str(x[1]) + """,""" + str(x[2]) + """,""" + str(x[3]) + """,""" + str(step) + """,""" + str(x[6]) + """,""" + str(x[6]) + """)"""
        sql2 = """UPDATE LAT SET TS= CURRENT_TIMESTAMP(),STEP = """+str(step)+""" WHERE ANIMALID="""+str(x[0])+""" AND RECEIVERID="""+str(x[3])+""";"""
        sql3 = """UPDATE ANIMAL SET LATTEST=CURRENT_TIMESTAMP() WHERE ANIMALID="""+str(x[0])+""";"""
        cursor.execute(sql)
        cursor.execute(sql2)
        cursor.execute(sql3)
        db.commit()
        temp['result']='success'
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("--- at addData in ydatabase")
        temp['result']='fail'
        db.rollback()
    db.close()
    return temp

def getAllData():
    temp =[]
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """select * from DATA"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            ANIMALID = row[0]
            TS  = row[1]
            X = row[2]
            Y = row[3]
            Z = row[4]
            AX = row[5]
            AY = row[6]
            AZ = row[7]
            #temp.append({'ANIMALID':ANIMALID,'TS':TS,'X':X,'Y':Y,'Z':Z,'AX':AX,'AY':AY,'AZ':AZ})
            temp.append({'ANIMALID':ANIMALID,'TS':TS,'RECEIVER TAG':Z,'STEP COUNT':AX,})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getAllData in ydatabase")
        db.rollback()
    db.close()
    return temp

def getData(animal):
    temp =[]
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """SELECT * FROM DATA WHERE ANIMALID="""+str(animal)+""" ;"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            ANIMALID = row[0]
            TS  = row[1]
            X = row[2]
            Y = row[3]
            Z = row[4]
            AX = row[5]
            AY = row[6]
            AZ = row[7]
            temp.append({'ANIMALID':ANIMALID,'TS':TS,'RECEIVER TAG':Z,'STEP COUNT':AX,})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at getData in ydatabase")
        db.rollback()
    db.close()
    return temp

def getSpecificData(animalid,hours):
    temp = []
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """SELECT * FROM DATA WHERE ANIMALID=""" + str(animalid) + """ AND DATA.TS > SUBDATE(CURRENT_TIMESTAMP,INTERVAL """+str(hours)+""" HOUR);"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            ANIMALID = row[0]
            TS = row[1]
            X = row[2]
            Y = row[3]
            Z = row[4]
            AX = row[5]
            AY = row[6]
            AZ = row[7]
            temp.append(
                { 'ANIMALID': ANIMALID, 'TS': TS, 'X': X, 'Y': Y, 'Z': Z, 'AX': AX, 'AY': AY, 'AZ': AZ})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("--- at getSpecificData in ydatabase")
        print ("Error")
        db.rollback()
    db.close()
    return temp

def deleteData(animalid,start,end):
    temp = {}
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """DELETE FROM DATA WHERE ANIMALID = """+str(animalid)+""" AND TS >='"""+str(start)+"""' AND TS<= '"""+str(end)+"""' ;"""
    try:
        res = cursor.execute(sql)
        temp["result"] = res
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at deleteData in ydatabase")
        temp['result'] = -1
        db.rollback()
    db.close()
    return temp

def deleteAllData(start,end):
    temp = {}
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """DELETE FROM DATA WHERE TS >='"""+str(start)+"""' AND TS<= '"""+str(end)+"""' ;"""
    try:
        res = cursor.execute(sql)
        temp["result"] = res
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at deleteData in ydatabase")
        temp['result'] = -1
        db.rollback()
    db.close()
    return temp

def getReceiverData():
    temp =[]
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """select * from LAT"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            ANIMALID = row[0]
            RECEIVERID  = row[1]
            TS = row[2]
            STEP = row[3]
            temp.append({'ANIMALID':ANIMALID,'RECEIVERID':RECEIVERID,'TS':TS,'STEP':STEP})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("at getThreshold in ydatabase")
        db.rollback()
    db.close()
    return temp


def updateThresholdTH(animalid,th):
    temp = {}
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """UPDATE DP SET TH="""+str(th)+""" , DATE=CURRENT_TIMESTAMP() WHERE ANIMALID = """+str(animalid)+""";"""
    try:
        res = cursor.execute(sql)
        temp["result"] = res
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at updateThresholdTH in ydatabase")
        temp['result'] = -1
        db.rollback()
    db.close()
    return temp

def updateThresholdSTATUS(animalid,status):
    temp = {}
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """UPDATE DP SET STATUS="""+str(status)+""" WHERE ANIMALID = """+str(animalid)+""";"""
    try:
        res = cursor.execute(sql)
        temp["result"] = res
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at updateThresholdSTATUS in ydatabase")
        temp['result'] = -1
        db.rollback()
    db.close()
    return temp

def getLatestData():
    temp =[]
    db = MySQLdb.connect("localhost", "root", "root", "ydatabase")
    cursor = db.cursor()
    sql = """SELECT ANIMALID, LATTEST FROM ANIMAL;"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            ANIMALID = row[0]
            LATEST  = row[1]
            temp.append({'ANIMALID':ANIMALID,'LATEST':LATEST})
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print (e)
        print ("---at getLattestData in ydatabase")
        db.rollback()
    db.close()
    return temp
