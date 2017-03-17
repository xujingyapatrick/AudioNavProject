'''
Created on Mar 7, 2017

@author: patrick
'''
from __future__ import print_function # Python 2/3 compatibility
import boto3
from DynamoDB.databaseManager import databaseTalksManager,databaseWebUserManager

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
print("you have imported databaseSetUp")

usersTable = dynamodb.create_table(
    TableName='WebUsers',
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

talksTable = dynamodb.create_table(
    TableName='Talks',
    KeySchema=[
        {
            'AttributeName': 'talk_id',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'talk_id',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

talkManager=databaseTalksManager()
userManager=databaseWebUserManager()
talkManager.initTable()
userManager.initTable()
talkManager.createNewTalk()
talkManager.createNewTalk()
userManager.createNewUser()
userManager.createNewUser()

print("UsersTable status:", usersTable.table_status)
print("TalksTable status:", talksTable.table_status)

print("tables setup finished!")



