'''
Created on Mar 7, 2017

@author: patrick
'''
from __future__ import print_function # Python 2/3 compatibility
import boto3
from DynamoDB.itemDefinition import User, Talk, Audio
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import urllib2
import requests
import time
import nltk
from docutils.nodes import description


# from database_setup import Base, Music
# Helper class to convert a DynamoDB item to JSON.
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             if o % 1 > 0:
#                 return float(o)
#             else:
#                 return int(o)
#         return super(DecimalEncoder, self).default(o)

############################################################################
#user manager class
############################################################################ 
class databaseWebUserManager():
    """docstring for dataBsaeManager"""
    dynamodb=None
    table=None

    def __init__(self):
        self.dynamodb=boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.table=self.dynamodb.Table("WebUsers")
        
    def initTable(self):
        #set id=0 to remember next avaliable id
        self.table.put_item(Item={"user_id":0,"info":1})


    def changeDynamoDBDicToPythonDic(self,userDic):
        userDic['userId']=int(userDic['userId'])
        talks=[]
        for talkId in userDic['talks']:
            talks.append(int(talkId))
        userDic['talks']=talks
        return userDic

    def createNewUser(self):
        try:
            response = self.table.get_item(
                Key={
                    'user_id': 0
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
            print("GetItem succeeded:")
#             print(item)
            self.table.update_item(Key={'user_id':0},UpdateExpression="set info = info + :val",ExpressionAttributeValues={':val':1},ReturnValues="UPDATED_NEW")
            usr=User().toDictionary()
            usr['userId']=int(item['info'])
            self.table.put_item(Item={'user_id':int(item['info']),'info':usr})
            return int(item['info'])
        
    def getUser(self, userId):
        try:
            response = self.table.get_item(
                Key={
                    'user_id': userId
                }
            )
        except ClientError as e:
            print('ERROR')
            print(e.response['Error']['Message'])
            return None
        else:
            print('RESPONSE')
            print(response)
            if 'Item' not in response:
                return None
            item = response['Item']
            print("GetItem succeeded:")
            item['info']=self.changeDynamoDBDicToPythonDic(item['info'])
#             print(json.dumps(item['info']))
            return User(item['info'])
        
    def deleteUser(self,userId):
        try:
            response = self.table.delete_item(
                Key={
                    'user_id': userId
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
            return False
        else:
            print("DeleteItem succeeded:")
            print(json.dumps(response))
            return True
        
    def flushDataOfUser(self,userId):
        response = self.table.update_item(
            Key={
                'user_id': userId
            },
            UpdateExpression="set info = :r",
            ExpressionAttributeValues={
                ':r': User().toDictionary()
            },
            ReturnValues="UPDATED_NEW"
        )
        return userId
    
    def updateEmail(self,userId,email):
        response = self.table.update_item(
            Key={
                'user_id': userId
            },
            UpdateExpression="set info.email = :r",
            ExpressionAttributeValues={
                ':r': email
            },
            ReturnValues="UPDATED_NEW"
        )
        return email
    
    def updatePassword(self,userId,password):
        response = self.table.update_item(
            Key={
                'user_id': userId
            },
            UpdateExpression="set info.password = :r",
            ExpressionAttributeValues={
                ':r': password
            },
            ReturnValues="UPDATED_NEW"
        )
        return password
    
    def addTalkToUser(self,userId,talkId):
        usr=self.getUser(userId)
        usr.addTalkToTalks(talkId)
        response = self.table.update_item(
             Key={
                'user_id': userId
            },
            UpdateExpression="set info.talks = :r",
            ExpressionAttributeValues={
                ':r': usr.talks
            },
            ReturnValues="UPDATED_NEW"
        )
        return usr.talks
    
    def deleteTalkFromUser(self,userId,talkId):
        usr=self.getUser(userId)
        usr.deleteTalkFromTalks(talkId)
        response = self.table.update_item(
            Key={
                'user_id': userId
            },
            UpdateExpression="set info.talks = :r",
            ExpressionAttributeValues={
                ':r': usr.talks
            },
            ReturnValues="UPDATED_NEW"
        )
        return usr.talks
    
    def getTalksFromUser(self,userId):
        usr=self.getUser(userId)
        if usr!=None:
            return usr.talks
        else:
            return None
    
    def getEmailFromUser(self,userId):
        usr=self.getUser(userId)
        if usr!=None:
            return usr.email
        else:
            return None
    
    def getPasswordFromUser(self,userId):
        usr=self.getUser(userId)
        if usr!=None:
            return usr.password
        else:
            return None
    
    def flushTalksOfUser(self,userId):
        usr=self.getUser(userId)
        usr.flushTalks()
        response = self.table.update_item(
            Key={
                'user_id': userId
            },
            UpdateExpression="set info.talks = :r",
            ExpressionAttributeValues={
                ':r': usr.talks
            },
            ReturnValues="UPDATED_NEW"
        )
        return usr.talks



############################################################################
#talk manager class
############################################################################ 
class databaseTalksManager():
    """docstring for dataBsaeManager"""
    dynamodb=None
    table=None

    def __init__(self):
        self.dynamodb=boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        self.table=self.dynamodb.Table("Talks")
        
    def initTable(self):
        #set id=0 to remember next avaliable id
        self.table.put_item(Item={"talk_id":0,"info":1})
    

    
    
    
    def changeDynamoDBDicToPythonDic(self,talkDic):
        talkDic['talkId']=int(talkDic['talkId'])
#         talkDic['startTime']=float(talkDic['startTime'])
#         talkDic['lastUpdateTime']=float(talkDic['lastUpdateTime'])
        talkerIds=[]
        for id in talkDic['talkerIds']:
            talkerIds.append(int(id))
        talkDic['talkerIds']=talkerIds
        talkDic['audioCount']=int(talkDic['audioCount'])
        audios={}
        for ad in talkDic['audios']:
#             talkDic['audios'][ad]["postTime"]=float(talkDic['audios'][ad]["postTime"])
#             talkDic['audios'][ad]["timeLength"]=float(talkDic['audios'][ad]["timeLength"])
            talkDic['audios'][ad]["fileSize"]=int(talkDic['audios'][ad]["fileSize"])
            talkDic['audios'][ad]["posterId"]=int(talkDic['audios'][ad]["posterId"])
            audios[ad]=talkDic['audios'][ad]
        talkDic['audios']=audios
        return talkDic

    def createNewTalk(self,title='unknown',tags=['default'],description='unknown'):
        try:
            response = self.table.get_item(
                Key={
                    'talk_id': 0
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
            print("GetItem succeeded:")
#             print(item)
            self.table.update_item(Key={'talk_id':0},UpdateExpression="set info = info + :val",ExpressionAttributeValues={':val':1},ReturnValues="UPDATED_NEW")
            talk=Talk()
            talk.talkId=int(item['info'])
            talk.title=title
            talk.tags=tags
            talk.description=description
            audDic=talk.audios
            audDic['default'].audioName='0s'+str(talk.talkId)+'sdefault'
            audDic[audDic['default'].audioName]=audDic['default']
            audDic.pop('default')
#             talk.audios.pop('default')
            talk.audios=audDic
            print(talk.toDictionary())
            self.table.put_item(Item={'talk_id':int(item['info']),'info':talk.toDictionary()})
            return int(item['info'])

    def getTalk(self,talkId):
        try:
            response = self.table.get_item(
                Key={
                    'talk_id': talkId
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            item = response['Item']
            item['info']=self.changeDynamoDBDicToPythonDic(item['info'])
            print("GetItem succeeded:")
            print(json.dumps(item['info']))
            return Talk(item['info'])
    def getAllTalks(self):
        fe = Key('talk_id').between(1, 50);
        
        response = self.table.scan(
            FilterExpression=fe
            )
        talks=[]
#         print(response['Items'])
        for item in response['Items']:
            item['info']=self.changeDynamoDBDicToPythonDic(item['info'])
            talks.append(Talk(item['info']))
        return talks

    def updateTalk(self,talkId,talk):
        response = self.table.update_item(
            Key={
                'talk_id': talkId
            },
            UpdateExpression="set info = :r",
            ExpressionAttributeValues={
                ':r': talk.toDictionary()
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    
    def updateTalkWhenAddAudio(self,talkId,talk):
        #TBD:could select useful data to push to cloud instead of all data. 
        return self.updateTalk(talkId, talk)

    def updateTalkWhenDeleteAudio(self,talkId,talk):
        #TBD:could select useful data to push to cloud instead of all data. 
        return self.updateTalk(talkId, talk)

        
        
    
    def getAudios(self,talkId):
        talk=self.getTalk(talkId)
        return talk.audios

    def deleteTalk(self,talkId):
        talk=self.getTalk(talkId)
        userManager=databaseWebUserManager()
        
        for userId in talk.talkerIds:
            userManager.deleteTalkFromUser(userId, talkId)
        
        try:
            response = self.table.delete_item(
                Key={
                    'talk_id': talkId
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
            return False
        else:
            print("DeleteItem succeeded:")
            print(response)
            return True
            
    def addAudio(self,talkId,audio):
        talk=self.getTalk(talkId)
        talk.addAudioToAudios(audio)
        response = self.table.update_item(
            Key={
                'talk_id': talkId
            },
            UpdateExpression="set info = :r",
            ExpressionAttributeValues={
                ':r': talk.toDictionary()
            },
            ReturnValues="UPDATED_NEW"
        )
        print("NEWTALKWITHNEWAUDIO")
        print(talk.toDictionary())
        return True
            
            
    def deleteAudio(self,talkId,audioId):
        talk=self.getTalk(talkId)
        talk.deleteAudioFromAudios(audioId)
        response = self.table.update_item(
            Key={
                'talk_id': talkId
            },
            UpdateExpression="set info = :r",
            ExpressionAttributeValues={
                ':r': talk.toDictionary()
            },
            ReturnValues="UPDATED_NEW"
        )
        return True
    def createAudioTags(self,soundFile):
        data = {'apikey':'a0eb3f3b-fef6-4377-b0b8-28585ab6390c',
                'file':  soundFile
                }
        res=requests.post("https://api.havenondemand.com/1/api/async/recognizespeech/v1", files=data)
        print(res.text)
        resJson=json.loads(res.text)
        jobId=resJson.get('jobID','toofast')
        while jobId=='toofast':#in case the post is too frequent
            time.sleep(20)
            res=requests.post("https://api.havenondemand.com/1/api/async/recognizespeech/v1", files=data)
            print(res.text)
            resJson=json.loads(res.text)
            jobId=resJson.get('jobID','toofast')
                    
        para={'apikey':'a0eb3f3b-fef6-4377-b0b8-28585ab6390c'}
        print(para)
        time.sleep(1)
        response=requests.post("https://api.havenondemand.com/1/job/status/"+jobId,data=para)
        jsonData=response.json()
        count=0;
        while(jsonData['status']!='finished'):#wait until the process is done
            count=count+1;
            print("checking: "+str(count))
            time.sleep(20)
            response=requests.post("https://api.havenondemand.com/1/job/status/"+jobId,data=para)
            jsonData=response.json()
        print(response.text)
        docu=jsonData['actions'][0]['result']['document']
        if len(docu)==0:
            tags=[]
        else:
            contents=docu[0]['content']
            contents=contents.replace("<Music/Noise>","")
            contents=contents.replace('  ',' ')
#           print(contents)
            tags=nltk.word_tokenize(contents)
        print('tags:::')
        print(tags)
#         time.sleep(3)

        return tags
#         res=urllib2.urlopen('https://api.havenondemand.com/1/api/async/recognizespeech/v1', data)
        
        

