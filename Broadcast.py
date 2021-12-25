from flask  import Flask,  render_template
from flask_socketio import SocketIO, join_room, leave_room, rooms, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] =  'secret!'
socketio = SocketIO(app)

@socketio.on('mj') 
def my_event_1_handler(data):
    mj = data['mj']
    room = data['room']
    print(mj)
    print(room)
    # join_room(room)
    emit('mj', mj, room = room)

@socketio.on('join')
def on_join(data):
    room = data['room']
    player_num = data['playerNum']
    join_room(room)
    # if player_num == 3:
      #   emit('start_game', data,  room = room)
    # send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    print(room)
    leave_room(room)
    # send(username + ' has entered the room.', room=room)

@socketio.on('start_game')
def start_game(data):
    room = data['room']
    print(room)
    emit('start_game', data,  room = room)
    pass

@socketio.on('next')
def next(data):
    room = data['room']
    
    emit('next', data, room = room)
    pass

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

if __name__ ==  '__main__':
    socketio.run(app, host = '0.0.0.0', port='8085', debug = True)
