'''
Created on Mar 7, 2017

@author: patrick
'''
import time



defaultUser={"userId":0, "email":"default", "password":"default", "talks":[0]}
class User(object):
#     """docstring for user"""
#     userId=0
#     email="default"
#     password="default"
#     talks=[0]

    def __init__(self, arg=defaultUser):
        self.userId=arg["userId"]
        self.email=arg["email"]
        self.password=arg["password"]
        self.talks=arg["talks"]

    def getUserId(self):
        return self.userId
    def getEmail(self):
        return self.email
    def getPassword(self):
        return self.password
    def getTalks(self):
        return self.talks
     
    def setUserId(self,userId):
        self.userId=userId
        return True
    def setEmail(self,email):
        self.email=email
        return True
    def setPassword(self,password):
        self.password=password
        return True
    
    def addTalkToTalks(self,talkId):
        if talkId not in self.talks:
            self.talks.append(talkId)
        return True
    def flushTalks(self):
        self.talks=[0]
        return True
    def deleteTalkFromTalks(self,talkId):
        while talkId in self.talks:
            self.talks.remove(talkId)
        return True

    def toDictionary(self):
        dic={}
        dic["userId"]=self.userId
        dic["email"]=self.email
        dic["password"]=self.password
        
        dic["talks"]=self.talks
        return dic
    #define functions for login manager
#     def to_json(self):
#         return {"name": self.name,
#                 "email": self.email}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.userId)


defaultAudio={"audioName":"default", "tags":["default"],"preAudioName":"default", "nextAudioNames":["default"], "postTime":0.0, "timeLength":0.0, "fileSize":0, "posterId":0}
class Audio(object):
#     """docstring for audio"""
#     audioName="default"
#     preAudioName="default"
#     nextAudioNames=["default"]
#     postTime=0.0
#     timeLength="default"
#     fileSize=0
#     posterId=0
#     sourceLink=""
    def __init__(self, arg=defaultAudio):
        self.audioName=arg["audioName"]
        self.tags=arg["tags"]
        self.preAudioName=arg["preAudioName"]
        self.nextAudioNames=["nextAudioNames"]
        self.postTime=arg["postTime"]
        self.timeLength=arg["timeLength"]
        self.fileSize=arg["fileSize"]
        self.posterId=arg["posterId"]
#             self.sourceLink=arg["sourceLink"]

    def getAudioName(self):
        return self.audioName
    def getPostTime(self):
        return self.postTime
    def getTimeLength(self):
        return self.timeLength
    def getFileSize(self):
        return self.fileSize
    def getPosterId(self):
        return self.posterId
#     def getSourceLink(self):
#         return self.sourceLink

    def setAudioName(self,audioName):
        self.audioName=audioName
        return True
    def setPostTime(self,postTime):
        self.postTime=postTime
        return True
    def setTimeLength(self,timeLength):
        self.timeLength=timeLength
        return True
    def setFileSize(self,fileSize):
        self.fileSize=fileSize
        return True
    def setPosterId(self,posterId):
        self.posterId=posterId
        return True
    def setPreAudioName(self,preAudioName):
        self.preAudioName=preAudioName
        return True
#     def setSourceLink(self,sourceLink):
#         self.sourceLink=sourceLink
#         return True

    def toDictionary(self):
        dic={}
        dic["audioName"]=self.audioName
        dic["tags"]=self.tags
        dic["preAudioName"]=self.preAudioName
        dic["nextAudioNames"]=self.nextAudioNames
        dic["postTime"]=self.postTime
        dic["timeLength"]=self.timeLength
        dic["fileSize"]=self.fileSize
        dic["posterId"]=self.posterId
#         dic["sourceLink"]=self.sourceLink
        return dic
    

##############################################################
######Talk class
##############################################################
defaultTalk={"talkId":0, "title":"default","description":"default","tags":["default"],"startTime":time.time(),"lastUpdateTime":0.0, "talkerIds":[0],"audioCount":0,"audios":{"default":Audio().toDictionary()}}
class Talk(object):
    """docstring for talk"""
#     talkId=0
#     title="default"
#     description="default"
#     tags=["default"]
#     startTime="default"
#     lastUpdateTime="default"
#     talkerIds=[0]#used to record all users has ever participated
#     audioCount=0
#     audios={"default":Audio().toDictionary()}
    def __init__(self, arg=defaultTalk):
        self.talkId=arg["talkId"]
        self.title=arg["title"]
        self.description=arg["description"]
        self.tags=arg["tags"]
        self.startTime=arg["startTime"]
        self.lastUpdateTime=arg["lastUpdateTime"]
        self.talkerIds=arg["talkerIds"]
        self.audioCount=arg["audioCount"]
        audiosDic={}
        for iter in arg["audios"]:
            audiosDic[iter]=Audio(arg["audios"][iter])
        self.audios=audiosDic
# 
    def getTalkId(self):
        return self.talkId
    def getStartTime(self):
        return self.startTime
    def getLastUpdateTime(self):
        return self.lastUpdateTime
    def getAudioCount(self):
        return self.audioCount
    def getTalkerIds(self):
        return self.talkerIds
    def getAudios(self):
        return self.audios

    def setTalkId(self,talkId):
        self.talkId=talkId
        return True
    
    def setTitle(self,title):
        self.title=title
        return True
    def setDescription(self,description):
        self.description=description
        return True
    def setTags(self,tags):
        self.tags=tags
        return True
    

    def setStartTime(self,startTime):
        self.startTime=startTime
        return True

    def setLastUpdateTime(self,lastUpdateTime):
        self.lastUpdateTime=lastUpdateTime
        return True

    def setLastUpdateTimeAsNow(self):
        self.lastUpdateTime=time.time()
        return True

    def setAudioCount(self,audioCount):
        self.audioCount=audioCount
        return True

    def flushAllAudios(self):
        self.talkerIds=[0]
        self.setaudioCount(0)
        self.audios={"default":Audio().toDictionary()}
        self.setLastUpdateTimeAsNow()
        return True
    def addTalkerIdToTalkerIds(self,talkerId):
        if talkerId not in self.talkerIds:
            self.talkerIds.append(talkerId)
            self.setLastUpdateTimeAsNow()
        return True
    def deleteTalkerIdFromTalkerIds(self,talkerId):
        if talkerId in self.talkerIds:
            self.talkerIds.remove(talkerId)
            self.setLastUpdateTimeAsNow()
            return True
        return False
    
    def addAudioToAudios(self,audio):
        if audio.audioName not in self.audios:
            self.audios[audio.audioName]=audio
            if audio.preAudioName !="default":
                preAudio=self.audios[audio.preAudioName]
                preAudio.nextAudioNames.append(audio.audioName)
                self.audios[audio.preAudioName]=preAudio.nextAudioNames
            self.audioCount=self.audioCount+1
            self.addTalkerIdToTalkerIds(audio.posterId)
            self.setLastUpdateTimeAsNow()
            return True
        else:
            return False

    def deleteAudioFromAudios(self,audioName):
        if audioName in self.audios:
            #you can not delet a audio when it has next audios             
            if len(self.audios[audioName].nextAudioNames)>1:
                return False
            else:
                while audioName in self.audios[self.audios[audioName].preAudioName].nextAudioNames:
                    self.audios[self.audios[audioName].preAudioName].nextAudioNames.remove(audioName)
                self.audios.pop(audioName, None)
                self.audioCount=self.audioCount-1
                self.setLastUpdateTimeAsNow()
                return True
        return True

    def toDictionary(self):
        dic={}
        dic["talkId"]=self.talkId
        dic["title"]=self.title
        dic["description"]=self.description
        dic["tags"]=self.tags
        dic["startTime"]=self.startTime
        dic["lastUpdateTime"]=self.lastUpdateTime
        dic["talkerIds"]=self.talkerIds 
        dic["audioCount"]=self.audioCount
        audioDic={}
        for audioName in self.audios:
            audioDic[audioName]=self.audios[audioName].toDictionary()
        dic["audios"]=audioDic

        return dic



