'''
Created on Mar 7, 2017

@author: patrick
'''
#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, request, jsonify, render_template, redirect, Response
from flask_login import current_user, LoginManager, login_user, logout_user, login_required 
import json
from DynamoDB.itemDefinition import User, Talk, Audio
from DynamoDB.databaseManager import databaseWebUserManager, databaseTalksManager
from S3.s3Manager import S3Manager
from time import sleep, time
from sys import getsizeof
from flask.helpers import url_for


app = Flask(__name__,static_url_path='')
app.secret_key = '123456' 
##init login manager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'loadLoginPage'

@login_manager.user_loader
def load_user(userId):
    dbUserManager=databaseWebUserManager()
    usr=dbUserManager.getUser(int(userId))
    return usr

#log in
@app.route('/api/v1/login', methods=['POST'])
def login():
#     print('LOGIN PRINT')
#     print(request.data)
    info = request.get_json()
    userId = info.get('userId', '-1')
    password = info.get('password', '')
    
    dbUserManager=databaseWebUserManager()
    user=dbUserManager.getUser(int(userId))
    print("USER!!")
    print(json.dumps(user.toDictionary()))
    if user and user.getPassword()==password:
        login_user(user)
        return jsonify({"userId": user.get_id(),
                        "password": user.getPassword()})
    else:
        return jsonify({"status": 401,
                        "reason": "UserId or Password Error"})

#logout current user
@app.route('/api/v1/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('loadPublicSquarePage'))
#     return jsonify(**{'result': 200,
#                       'data': {'message': 'logout success'}})


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
    info=request.get_json()
    userManager=databaseWebUserManager()
    userId=userManager.createNewUser()
    sleep(0.5)
    userManager.updateEmail(userId, info.get('email','example.com'))
    sleep(0.5)
    userManager.updatePassword(userId, info.get('password','123456'))
    sleep(0.5)
    return jsonify(**{'userId': userId})


#get the public talks
@app.route('/api/v1/alltalks',methods=['GET'])
def getAllTalks():
    dbManager=databaseTalksManager()
    talks=dbManager.getAllTalks()
    talkDic={}
    for talk in talks:
#         print("TALK:")
#         print(talk.toDictionary())
        talkDic[str(talk.getTalkId())]=talk.toDictionary()
#     print("JSONIFY:jsonify(**talkDic)")
#     print(jsonify(**talkDic).get_data())
    return jsonify(**talkDic)

#get all personal talks to show
@app.route('/api/v1/personaltalks',methods=['GET'])
@login_required
def getPersonalTalks():
    user=current_user
    userId=user.getUserId()
    userManager=databaseWebUserManager()
    talkIds=userManager.getTalksFromUser(userId)
    if talkIds==[0]:
        return jsonify(**{})
    talkManager=databaseTalksManager()
    talkDic={}
    for talkId in talkIds:
        if talkId!=0:
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
    
    pagetype='SQUARE'
    jsonifyTalks=getAllTalks()
    talks=json.loads(jsonifyTalks.get_data())
    for talk in talks:
#         print("TALK IN TALKS")
#         print(talk)
#         print(talks[talk])
        talks[talk]['talkString']=json.dumps(talks[talk])
    talkList=[]
    for talk in sorted(talks):
        talkList.append(talks[talk])
    return render_template('talksPage.html',talkList=talkList,pagetype=pagetype)
#     return app.send_static_file('index.html')

@app.route('/api/v1/private',methods=['GET'])
@login_required
def loadPrivateMomentsPage():
    user=current_user
    pagetype='MOMENTS'
    print("CURRENT USER")
    print(user.get_id())
    jsonifyTalks=getPersonalTalks()
    talks=json.loads(jsonifyTalks.get_data())
    for talk in talks:
        talks[talk]['talkString']=json.dumps(talks[talk])
    
    talkList=[]
    for talk in sorted(talks):
        talkList.append(talks[talk])
    return render_template('talksPage.html',talkList=talkList, pagetype=pagetype)

@app.route('/api/v1/newtalk',methods=['GET'])
def loadNewTalkPage():
    return render_template('newTalkPage.html')
#     return app.send_static_file('index.html')



#create a new talk 
@app.route('/api/v1/talk',methods=['PUT'])
@login_required
def createNewTalk():
    
    info=request.get_json()
    title=info.get('title','unknown')
    description=info.get('description','unknown')
    tags=info.get('tags',['default'])
    talkManager=databaseTalksManager()
    talkId=talkManager.createNewTalk(title,tags,description)
#     talk=Talk()
#     talk.setTalkId(talkId)
#     talk.setTitle(title)
#     talk.setDescription(description)
#     talk.setTags(tags)
#     sleep(0.5)
#     talkManager.updateTalk(talkId, talk)
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
    audSpi=audioName.split('s')
    if audSpi[2]=="default":
        return jsonify(**{'info':'error'})
    s3=S3Manager()
    f=s3.getFile(str(audioName))
#     return jsonify(**{'info':f})
    return Response(f)

#get a audio talk 
@app.route('/api/v1/audio',methods=['POST'])
@login_required
def createAudio():
#     print("REQUEST!!")
#     print(request.form.to_dict())
#     print(request.files.to_dict())
    preDic=request.form.to_dict()
    preAudioName=preDic.get('preName','default')
    fileDic=request.files.to_dict()
    soundFile=fileDic.get('audioData','default')

#     print("PREAUDIONAME!")
#     print(preAudioName)
    
    if preAudioName=='default':
        return jsonify({'info':'error: no prename'})
    
    tmp=preAudioName.split('s')
    talkId=int(tmp[1])
    userId=int(current_user.get_id())
    
#     preAudioName=request.args.get('preAudioName',default="default",type=str)
#     if talkId=="default":
#         return"error: you should specify an preAudioName"
#     info=json.load(request.data)
    talkManager=databaseTalksManager()
    talk=talkManager.getTalk(talkId)
    if userId not in talk.talkerIds:
        usrManager=databaseWebUserManager()
        usrManager.addTalkToUser(userId, talkId)
        
    audio=Audio()
    audioName=str(userId)+"s"+str(talkId)+"s"+str(talk.getAudioCount()+1)
    audio.setAudioName(audioName)
    audio.setPreAudioName(preAudioName)
    audio.setPosterId(userId)
    audio.setPostTime(str(time()))
    audio.setFileSize(getsizeof(soundFile))
    audio.setTimeLength('1.0')
#     tags=talkManager.createAudioTags(soundFile)
    s3=S3Manager()
    s3.storeFile(audioName,soundFile)
    talkManager.addAudio(talkId, audio)
    
    return jsonify({'info':'success'})



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)    
    

