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

# from aichatbot import chat
from pyonegraph import linkpreview
# from chat_nlt import chatbots

load_dotenv()
bot_status= []

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
    global bot_status
    
    if bot_status == []:
        bot_status.append("false")
        print(bot_status)
    if bot_activate:
        bot_status[0] = "True"
        sysmsg = {
				"author": "system", 
				"commend": "Sherlock bot is currently offline. ",
				"time": datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                "type": "bot"
        }
        collection.insert_one(sysmsg)
        sysmsg = json_util.dumps(sysmsg)
        socketio.emit('chat message', sysmsg)
    retrmsg=json_util.dumps(msg)       
    socketio.emit('chat message', retrmsg)

    # if msg['commend'] == 'quit' and bot_status[0] == "True":
    #     bot_status[0] = "False"
    #     sysmsg = {
	# 			"author": "system", 
	# 			"commend": "Sherlock bot deactivated",
	# 			"time": datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
    #             "type": "bot"
    #     }
    #     collection.insert_one(sysmsg)
    #     sysmsg = json_util.dumps(sysmsg)
    #     socketio.emit('chat message', sysmsg)
    
    # if bot_status[0] == "True":
        
    #     text = msg['commend']
    #     if '@sherlock' in text:
    #         text = text.lower().strip('@sherlock')
            
    #     bot_responses = chat(text)
    #     botmsg = {
	# 			"author": "sherlock_bot", 
	# 			"commend": bot_responses,
	# 			"time": datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
    #             "type": "bot"
    #     }
        
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
    
    print(msg)
    try: collection.insert_one(msg)
    except: print("CANNNT WRITE THE DATA INTO DATABASE")
    

if __name__ == "__main__":
    socketio.run(app)
