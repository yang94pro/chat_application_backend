# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ChatAdmin:123123123@chathistorydb-hwnzu.gcp.mongodb.net/test?authSource=admin&replicaSet=chathistorydb-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true')

y =client['msgdatabase']['chat_history'].remove({"time":{"$gte":"2020/02/18 14:29:29" }})
print(y)