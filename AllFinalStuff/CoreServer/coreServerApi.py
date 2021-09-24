
import coreServerDb
import random
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/getpasscode',methods=['POST'])
def getpasscode():
    response_return = {}
    try:
        userid = request.json['USERID']
        response_return = coreServerDb.getPassCode(userid)
    except (Exception) as e:
        print(str(e))
        response_return = {'MESSAGE':'REQUIRES USERID, NOT FOUND'}
    return jsonify(response_return)

@app.route('/performTransaction',methods=['POST'])
def carryOutTransaction():
    response_return = {"MESSAGE":"Something went wrong. Please try it again.","FLAG":"False"}
    try:
        from_user = request.json['FROM_USERNAME']
        to_user = request.json['TO_USERNAME']
        amount = request.json['AMOUNT']
        response_return = coreServerDb.performTransaction(from_user,to_user,amount)
    except (Exception) as e:
        print(str(e))
        response_return = {'MESSAGE':"REQUIRES USERID, NOT FOUND","FLAG":"False"}
    return jsonify(response_return)

@app.route('/checkBalance',methods=['POST'])
def checkBalance():
    response_return = {"MESSAGE":"Something went wrong. Please try it again.","FLAG":"False"}
    try:
        username = request.json['USERNAME']
        response_return = coreServerDb.checkBalanceUsername(username)
    except (Exception) as e:
        print(str(e))
        response_return = {'MESSAGE':"REQUIRES USERNAME, NOT FOUND","FLAG":"False"}
    return jsonify(response_return)

@app.route('/transaction',methods=['POST'])
def getTransaction():
    response_return =  {}
    try:
        userid = request.json['USERID']
        response_return = coreServerDb.getTransaction(userid)
        response_return = {"MESSAGE":"found last transaction","FLAG":"True","DATA":response_return}
    except (Exception) as e:
        print(str(e))
        response_return = {'MESSAGE':'REQUIRES USERID, NOT FOUND',"FLAG":"False"}
    return jsonify(response_return)


@app.route('/sentences',methods=['POST'])
def getSentences():
    response_return =  {}
    try:
        userid = request.json['USERID']
        response_return = coreServerDb.getSentences(userid)
        if(len(response_return)>0):
            response_return = {"MESSAGE":"Question found","FLAG":"True","DATA":response_return[int(random.randrange(0, len(response_return)))]}
        else:
            response_return = {"MESSAGE":"Question not found","FLAG":"False"}
    except (Exception) as e:
        print(str(e))
        response_return = {'MESSAGE':'REQUIRES USERID, NOT FOUND',"FLAG":"False"}
    return jsonify(response_return)

@app.route('/checkTransaction',methods=['POST'])
def checkTransaction():
    response_return = {"MESSAGE":"Something went wrong. Please try it again.","FLAG":"False"}
    try:
        userid = request.json['USERID']
        response_return = coreServerDb.checkTransaction(userid)
    except (Exception) as e:
        print(str(e))
        response_return = {'MESSAGE':"REQUIRES USERID, NOT FOUND","FLAG":"False"}
    return jsonify(response_return)

@app.route('/sourabh',methods=['GET'])
def sourabh():
    return jsonify({'sourabh':'hi'})

if __name__=='__main__':
    app.run(threaded=True,debug=True,port = 5000,host='0.0.0.0')
