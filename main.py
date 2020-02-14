from flask import Flask, request
from flask_socketio import SocketIO
from pymongo import MongoClient
import json
from flask_cors import CORS
import eventlet
from bson import json_util
from werkzeug.middleware.proxy_fix import ProxyFix
import pyonegraph
from dotenv import load_dotenv
import os
import re
load_dotenv()



try:
    client = MongoClient(os.getenv("MONGODBSTRING"))
    db = client.msgdatabase
    collection = db.chat_history
except:
    print("CANNNT CONNECT DATABASE MONGODB")

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app,  x_for=1, x_host=1)
socketio = SocketIO(app,cors_allowed_origins="*") 


@app.route("/api/chat")
def chathistory (methods=['GET']):
    chatdb = (collection.find().sort("time",-1).limit(50))
    c= json_util.dumps(chatdb)
    return c


@socketio.on ('chat message')
def resp (msg,methods=['GET','POST']):
    
    result = re.search('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', msg['commend'])
    print(msg['commend'])
    if result:
        try:
            link =(pyonegraph.linkpreview(result[0]))

            for k, v in link.items():
                msg[k]=v
            msg['type']="link"
        except: pass

    retrmsg=json_util.dumps(msg)       
    print (retrmsg)
    print(result)
    socketio.emit('chat message', retrmsg)
    user_ip= request.headers.getlist("X-Forwarded-For")
    userip=""
    for x in user_ip:
        userip+=x
    msg['ip']=userip
    print(msg)
    try: collection.insert_one(msg)
    except: print("CANNNT WRITE THE DATA INTO DATABASE")
    

if __name__ == "__main__":
    socketio.run(app)