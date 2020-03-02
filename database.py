# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
client = MongoClient(os.getenv("MONGODBSTRING"))

# y = client['msgdatabase']['ip_add_tracking'].remove({"user_ip": ",115.164.51.221"})
y =client['msgdatabase']['chat_history'].remove({"time":{"$gte":"2020/03/02 19:24:45" }})

print(y)