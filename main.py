from flask import Flask, request
from flask_socketio import SocketIO
from pymongo import MongoClient
import json
from flask_cors import CORS
import eventlet
from bson import json_util

try:
    client = MongoClient("mongodb+srv://ChatAdmin:123123123@chathistorydb-hwnzu.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.msgdatabase
    collection = db.chat_history
except:
    print("CANNNT CONNECT DATABASE MONGODB")

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app,cors_allowed_origins="*") 

@app.route("/api/chat")
def chathistory (methods=['GET']):
    chatdb = (collection.find().sort("time",-1).limit(10))
    chath= json_util.dumps(chatdb)
    return chath


@socketio.on ('chat message')
def resp (msg,methods=['GET','POST']):
    print(msg)
    g=request.remote_addr
    retrmsg=json_util.dumps(msg)
    msg['ip']=g
    try: collection.insert_one(msg)
    except: print("CANNNT WRITE THE DATA INTO DATABASE")
    socketio.emit('chat message', retrmsg)

if __name__ == "__main__":
    socketio.run(app)