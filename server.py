'''
Created on Mar 7, 2017

@author: patrick
'''
#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, request, jsonify, render_template, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required 
import json
from DynamoDB.itemDefinition import User, Talk, Audio
from DynamoDB.databaseManager import databaseWebUserManager, databaseTalksManager
from S3 import s3Manager
from time import sleep, time
from sys import getsizeof
from flask.helpers import url_for


app = Flask(__name__,static_url_path='')
##init login manager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'url_for(login)'

@login_manager.user_loader
def load_user(userId):
    dbUserManager=databaseWebUserManager()
    usr=dbUserManager.getUser(int(userId))
    return usr

#log in
@app.route('/api/v1/login', methods=['POST'])
def login():
    info = json.loads(request.data)
    userId = info.get('userId', '-1')
    password = info.get('password', '')
    
    dbUserManager=databaseWebUserManager()
    user=dbUserManager.getUser(int(userId))

    if user and user.getPassword()==password:
        login_user(user)
        return jsonify({"userId": user.get_id(),
                        "password": user.getPassword()})
    else:
        return jsonify({"status": 401,
                        "reason": "UserId or Password Error"})

#logout current user
@app.route('/api/v1/login', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'logout success'}})


#get login page
@app.route('/api/v1/login', methods=['GET'])
def loadLoginPage():
    return render_template('login.html')


#get current user information
@app.route('/api/v1/current_user', methods=['GET'])
@login_required
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user.toDictionary()}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    return jsonify(**resp)


#register 
@app.route('/api/v1/register',methods=['GET'])
def loadRegisterPage():
    print("loading register.html")
    return render_template('register.html')


#register 
@app.route('/api/v1/css',methods=['GET'])
def getCss():
    print("loading css")
    return app.send_static_file('style.css')



#submit register information 
@app.route('/api/v1/register',methods=['PUT'])
def createUser():
    info=json.load(request.data)
    userManager=databaseWebUserManager()
    userId=userManager.createNewUser()
    userManager.updateEmail(userId, info.get('email','example.com'))
    userManager.updatePassword(userId, info.get('password','123456'))
    return jsonify(**{'userId': userId})


#get the public talks
@app.route('/api/v1/alltalks',methods=['GET'])
def getAllTalks():
    dbManager=databaseTalksManager()
    talks=dbManager.getAllTalks()
    talkDic={}
    for talk in talks:
        talkDic[str(talk.getTalkId())]=talk.toDictionary()
    return jsonify(**talkDic)

#get all personal talks to show
@app.route('/api/v1/personaltalks',methods=['GET'])
@login_required
def getPersonalTalks():
    user=current_user
    userId=user.getUserId()
    userManager=databaseWebUserManager()
    talkIds=userManager.getTalksFromUser(userId)
    talkManager=databaseTalksManager()
    talkDic={}
    for talkId in talkIds:
        talkDic[str(talkId)]=talkManager.getTalk(talkId).toDictionary()
        sleep(0.5)
    return jsonify(**talkDic)

#get the home page 
@app.route('/api/v1/home',methods=['GET'])
def loadHomePage():
    return redirect(url_for('loadPublicSquarePage'))
#     return render_template('home.html')

@app.route('/api/v1/public',methods=['GET'])
def loadPublicSquarePage():
    jsonTalks=getAllTalks()
    talks=json.load(jsonTalks)
    
    return render_template('talksPage.html',talks=talks)
#     return app.send_static_file('index.html')

@app.route('/api/v1/private',methods=['GET'])
@login_required
def loadPrivateMomentsPage():
    user=current_user
    if user.is_authenticated():
        jsonTalks=getPersonalTalks()
        talks=json.load(jsonTalks)
        return render_template('talksPage.html',talks=talks)
    else:
        return redirect(url_for('loadRegisterPage'))
#     return app.send_static_file('index.html')

# @app.route('/api/v1/talkpage',methods=['GET'])
# def loadTalkPage():
#     jsonTalk=getTalk()
#     talk=json.load(jsonTalk)
#     
#     return render_template('talk.html')
# #     return app.send_static_file('index.html')


#create a new talk 
@app.route('/api/v1/talk',methods=['PUT'])
@login_required
def createNewTalk():
    
    info=request.get_json()
    title=info.get('title','unknown')
    description=info.get('description','unknown')
    tags=info.get('tags',['empty'])
    talkManager=databaseTalksManager()
    talkId=talkManager.createNewTalk()
    talk=Talk()
    talk.setTalkId(talkId)
    talk.setTitle(title)
    talk.setDescription(description)
    talk.setTags(tags)
    sleep(0.5)
    talkManager.updateTalk(talkId, talk)
    return jsonify(**{'talkId':talkId})
#  
#     data=request.get_json()
#     print(data)
#     features=[data['info']]
#     res=classifier.decideStatusAndSpeed(features)
#     print(res)
#     return jsonify(**res)

#get a new talk 
@app.route('/api/v1/talk',methods=['GET'])
def getTalk():
    talkId=request.args.get('talkId',default=0,type=int)
    if talkId==0:
        return "error: you should specify a talkId"
    talkManager=databaseTalksManager()
    talk=talkManager.getTalk(talkId)
    return jsonify(**(talk.toDictionary()))
    
#get a audio talk 
@app.route('/api/v1/audio',methods=['GET'])
def getAudio():
    audioName=request.args.get('audioName',default="default",type=str)
    if audioName=="default":
        return "error: you should specify an audioId"
    s3=s3Manager()
    f=s3.getFile(str(audioName))
    return jsonify(**{'info':f})
    

#get a audio talk 
@app.route('/api/v1/audio',methods=['PUT'])
def createAudio():
    userId=request.args.get('userId',default=0,type=int)
    if userId==0:
        return "error: you should specify an userId"
    talkId=request.args.get('talkId',default=0,type=int)
    if talkId==0:
        return"error: you should specify an talkId"
    preAudioName=request.args.get('preAudioName',default="default",type=str)
    if talkId=="default":
        return"error: you should specify an preAudioName"
    info=json.load(request.data)
    talkManager=databaseTalksManager()
    talk=talkManager.getTalk(talkId)
    audio=Audio()
    audioName=str(userId)+"_"+str(talkId)+"_"+str(talk.getAudioCount()+1)
    audio.setAudioName(audioName)
    audio.setPreAudioName(preAudioName)
    audio.setPosterId(userId)
    audio.setPostTime(time())
    audio.setFileSize(getsizeof(info.get('data','default',type=str)))
    audio.setTimeLength(1.0)
    
    s3=s3Manager()
    s3.storeFile(audioName,info.get('data','default',type=str))
    talkManager.addAudio(talkId, audio)
    
    return jsonify({'info':'create audio success'})



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)    
    

