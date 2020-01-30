from flask import Flask, send_from_directory, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)

socketio = SocketIO(
    app, 
    cors_allowed_origins="*",)

@socketio.on ('chat message')
def resp (json,methods=['GET','POST']):
    print(json)
    socketio.emit('chat message', json)


@socketio.on('connect')
def test_connect():
    socketio.emit('chat message', {"author": "system", "commend":" a user connected"})


@socketio.on('disconnect')
def disconnection():
    socketio.emit('chat message', {"author": "system", "commend":" a user disconnected"})
    print("Client disconnected")



if __name__ == "__main__":

    socketio.run(app, debug=True)