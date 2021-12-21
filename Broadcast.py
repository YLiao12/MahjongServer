from flask  import Flask,  render_template
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] =  'secret!'
socketio = SocketIO(app)

@socketio.on('mj') 
def my_event_1_handler(data):
    mj = data['mj']
    room = data['room']
    print(mj)
    print(room)
    join_room(room)
    emit('mj', mj, room = room)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

if __name__ ==  '__main__':
    socketio.run(app, host = '0.0.0.0', port='8085', debug = True)
