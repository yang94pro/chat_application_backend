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
    chatdb = (collection.find().sort("time",-1).limit(100))
    c= json_util.dumps(chatdb)
    return c


@socketio.on ('chat message')
def resp (msg,methods=['GET','POST']):
    retrmsg=json_util.dumps(msg)
    socketio.emit('chat message', retrmsg)
    print(msg)
    userip= request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    msg['ip']=userip
    try: collection.insert_one(msg)
    except: print("CANNNT WRITE THE DATA INTO DATABASE")
    

if __name__ == "__main__":
    socketio.run(app)