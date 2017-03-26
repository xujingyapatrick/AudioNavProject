'''
Created on Mar 8, 2017

@author: patrick
'''
import boto3
import botocore


class S3Manager(object):
    """docstring for user"""
#     userId=0
#     s3=None
#     bucket=None

    def __init__(self):
        self.s3=boto3.resource('s3')
        self.bucket=self.s3.Bucket('ituedupatrickxujingya')
    
    def createBucket(self):
        self.s3.create_bucket(Bucket='ituedupatrickxujingya')
        print("create bucket success")
    def initS3DataBase(self):
        self.createBucket()
        print("init S3 remote bucket success")
    def deleteBucket(self):
        for key in self.bucket.objects.all():
            key.delete()
        self.bucket.delete()
        print("bucket delete success")
    
    def storeFile(self,dataName,data):
        self.s3.Object('ituedupatrickxujingya', dataName).put(Body=data)
        return True
    
    def getFile(self,fileId):
        obj=self.bucket.Object(fileId)
#         print('OBJOBJOBJ')
#         print(obj)
        data=obj.get()['Body'].read()
#         print('DATA DATA')
#         print(data)
        return data
    
    def deleteFile(self,fileId):
        self.bucket.Object(fileId).delete()
        return True

# s3=S3Manager()
# dataId="87877676865676789"
# data="dnbaibdyebfuenfuyb bfbfyeuwb hbfuhbfyuew"
# s3.storeFile(dataId,data)
# 
# st=s3.getFile(dataId)
# print(st)
# print(s3.deleteFile(dataId))
# # st=s3.getFile(dataId)
# print(st)