'''
Created on Mar 7, 2017

@author: patrick
'''
from __future__ import print_function # Python 2/3 compatibility
import boto3
from DynamoDB.databaseManager import databaseTalksManager,databaseWebUserManager
from S3.s3Manager import S3Manager
import time

talkManager=databaseTalksManager()
userManager=databaseWebUserManager()
s3=S3Manager()

talks=talkManager.getAllTalks()
for talk in talks:
    audioDic=talk.audios
    for audioName in audioDic:
        if audioDic[audioName].tags==["default"]:
            try:
                audioFile=s3.getFile(audioName)
            except:
                print("No resource in :"+audioName)
            else:
                tags=talkManager.createAudioTags(audioFile)
                if len(tags)==0:
                    tags=["empty audio"]
                talk.audios[audioName].tags=tags
#                 time.sleep(60)
    talkManager.updateTalk(talk.talkId, talk)

print("all tags update done")
    