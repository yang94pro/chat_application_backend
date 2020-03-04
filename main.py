import os
import re
from datetime import datetime

from bson import json_util
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
from werkzeug.middleware.proxy_fix import ProxyFix

# from chat_nlt import chatbots
from bot_protocol import Bot

from pyonegraph import linkpreview

load_dotenv()


bot_status = ''


app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app,  x_for=1, x_host=1)
socketio = SocketIO(app,cors_allowed_origins="*") 

try:
    db = MongoClient(os.getenv("MONGODBSTRING")).msgdatabase
except:
    print("DATABASES UNAVAILABLE")
@app.route("/api/chat")
def chathistory (methods=['GET']):
    chatdb = db.chat_history.find().sort("time",-1).limit(50)

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
        db.ip_add_tracking.insert_one(user_data)
        print("An user is visiting. IP address added")

    except: 
        print("DATABASE ERROR")
    return c


@socketio.on ('chat message')
def resp (msg,methods=['GET','POST']):

    #to create link preview by using regex detection
    result = re.search('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', msg['commend'])
    if result:
        try:
            link =linkpreview(result[0])
            for k, v in link.items():
                msg[k]=v
            msg['type']="link"
        except: pass
    retrmsg=json_util.dumps(msg)       
    socketio.emit('chat message', retrmsg)
    db.chat_history.insert_one(msg)


    bot_activate = re.search('^@Sherlock', msg['commend'],  re.IGNORECASE)
    global bot_status
    if bot_activate:
        texts = Bot(msg['commend'], bot_status)
        (resp, bot_status) = texts._conversion()
        botmsg = json_util.dumps(resp)
        socketio.emit('chat message', botmsg)
        db.chat_history.insert_one(resp)

    if bot_status:
        texts = Bot(msg['commend'], bot_status)
        (resp, bot_status) = texts._conversion()
        botmsg = json_util.dumps(resp)
        socketio.emit('chat message', botmsg)
        db.chat_history.insert_one(resp)

        
    #     try: 
    #         collection.insert_one(botmsg)
    #         retrmsg=json_util.dumps(botmsg)
    #         socketio.emit('chat message', retrmsg)
            
    #     #     nltk_botcontent = chatbots()
    #     #     nltk_botmsg = {
	# 	# 		"author": "sherlock_bot", 
	# 	# 		"commend": "Sherlock is currently down. You can talk to my friends",
	# 	# 		"time": datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
    #     #         "type": "bot",
    #     # }
        


        # except: print("Bot system offline")
    user_ip= request.headers.getlist("X-Forwarded-For")
    userip=""
    for x in user_ip:
        userip= userip +","+ x
    msg['ip']=userip

    
    

if __name__ == "__main__":
    socketio.run(app)
