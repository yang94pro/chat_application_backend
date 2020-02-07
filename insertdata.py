from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client.msgdatabase
collection = db.chat_history

collection.insert_one(x)