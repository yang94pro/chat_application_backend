from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client.msgdatabase
collection = db.chat_history


x= collection.find().sort("time",-1).limit(10)
for y in x:
    print (y)