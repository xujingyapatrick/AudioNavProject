'''
Created on Mar 12, 2017

@author: patrick
'''
from DynamoDB.databaseManager import databaseWebUserManager, databaseTalksManager
from S3.s3Manager import S3Manager

import DynamoDB.databaseSetup
import S3.s3Setup

userManager=databaseWebUserManager()
talkManager=databaseTalksManager()

userManager.initTable()
talkManager.initTable()



