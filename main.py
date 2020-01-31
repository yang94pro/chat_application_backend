from flask import Flask, send_from_directory, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)

socketio = SocketIO(app,cors_allowed_origins="*") 

@app.route("/")
def sessions():
    return send_from_directory('./public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('./public', path)




@socketio.on ('chat message')
def resp (json,methods=['GET','POST']):
    print(json)
    socketio.emit('chat message', json)




if __name__ == "__main__":

    socketio.run(app)