from flask import Flask, request
from flask_socketio import SocketIO
from chatbot import ChatBot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

chatbot_instance = ChatBot('''You are expert in answering any kind of questions asked related to just video games. VERY IMPORTANT THING, you must answer any query asked based only on the CONTEXT given to you.''')

@socketio.on('ask_question')
def handle_ask_question(data):
    question = data['question']
    print(question)
    answer = chatbot_instance.ask_question(question)
    socketio.emit('answer', {'answer': answer[-1]['content']})

if __name__ == '__main__':
    socketio.run(app)