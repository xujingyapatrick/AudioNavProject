'''
Created on Mar 10, 2017

@author: patrick
'''
import boto3
import botocore
 
s3=boto3.resource('s3')
s3.create_bucket(Bucket='ituedupatrickxujingya')
print("s3 setup success")
