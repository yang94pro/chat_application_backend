from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

class Db_collection:
    
    def __init__(self, *args):
        self.args = args
   
    def _dbconnect(self):
        db = MongoClient(os.getenv("MONGODBSTRING")).msgdatabase
        return db

        
        

    def read_history(self):
        collection = self._dbconnect().chat_history
        return collection.find().sort("time",-1).limit(50)


    def chat_history(self,data):
        collection = self._dbconnect().chat_history
        collection.insert_one(self.data)
        return


    def ip_add_tracking(self,data):
        collection = self._dbconnect().ip_add_tracking
        collection.insert_one(self.data)
        return
            

        
        