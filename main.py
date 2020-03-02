from flask import Flask, request
from flask_socketio import SocketIO
from pymongo import MongoClient
from flask_cors import CORS
from bson import json_util
from werkzeug.middleware.proxy_fix import ProxyFix
from pyonegraph import linkpreview
from dotenv import load_dotenv
from datetime import datetime
from aichatbot import chat
import os
import re
from datetime import datetime
load_dotenv()

try:
    client = MongoClient(os.getenv("MONGODBSTRING"))
    db = client.msgdatabase
    collection = db.chat_history
    collection2 = db.ip_add_tracking
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
    try:
        user_ip= request.headers.getlist("X-Forwarded-For")
        user_ip_str=''
        for x in user_ip:
            user_ip_str = user_ip_str+","+x
        user_data= {
            "time": datetime.utcnow(),
            "user_ip": user_ip_str,
        }
        collection2.insert_one(user_data)
        print("An user is visiting. IP address added")

    except: 
        print("DATABASE ERROR")
    return c


@socketio.on ('chat message')
def resp (msg,methods=['GET','POST']):
    result = re.search('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', msg['commend'])
    
    if result:
        try:
            link =linkpreview(result[0])
            for k, v in link.items():
                msg[k]=v
            msg['type']="link"
        except: pass
    bot_activate = re.search('^@Sherlock', msg['commend'],  re.IGNORECASE)
    print(bot_activate)
   
    retrmsg=json_util.dumps(msg)       
    socketio.emit('chat message', retrmsg)
    if bot_activate:
        text = msg['commend']
        text = text.lower().split('@sherlock')
        text[1]= text[1].strip()
        bot_responses = chat(text[1])
        botmsg = {
				"author": "sherlock_bot", 
				"commend": bot_responses,
				"time": datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                "type": "bot",
        }
        print(botmsg)
        try: 
            retrmsg=json_util.dumps(botmsg)
            socketio.emit('chat message', retrmsg)

        except: print("Bot system offline")
    user_ip= request.headers.getlist("X-Forwarded-For")
    userip=""
    for x in user_ip:
        userip= userip +","+ x
    msg['ip']=userip
    
    print(msg)
    try: collection.insert_one(msg)
    except: print("CANNNT WRITE THE DATA INTO DATABASE")
    

if __name__ == "__main__":
    socketio.run(app)