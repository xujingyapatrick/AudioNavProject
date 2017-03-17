'''
Created on Mar 7, 2017

@author: patrick
'''
from DynamoDB.itemDefinition import Talk, Audio

a=Audio()
b=Talk()
print(b.toDictionary())
# from dataBaseManager import dataBsaeManager
# 
# manager=dataBsaeManager()
# # manager.insertExampleItem()
# # print("insert finished!")
# manager.updateExampleItem()
# print(manager.scanAllData()[0].author)
