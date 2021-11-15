from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json

app = Flask(__name__)

conn = mysql.connector.connect(
  host="localhost",       
  user="mahjong",    
  passwd="mahjongpsw",   
  database = "mahjongdb",
)
cursor = conn.cursor(dictionary = True)

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/player_id")
def get_playerid():
    get_id = "select player_id from players order by player_id desc limit 0,1"
    while True:
        try:
            cursor.execute(get_id)
            break
        except Exception:
            conn.ping(True)
    result = cursor.fetchall()
    jsonResult = json.dumps(result)
    return jsonify(id = jsonResult)

@app.route("/create_player", methods=["POST"])
def create_player():
    player_name = request.form.get("player_name")
    insert_player = "insert into players (name) values (%s)"
    insert_player_param = (player_name, )
    while True:
        try:
            cursor.execute(insert_player, insert_player_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)
    return jsonify(status="OK")

@app.route("/get_tables")
def get_tables():
    # get records from mysql
    # change records into json
    # return json
    query_tables = "SELECT * FROM mj_tables ORDER BY table_id ASC"
    while True:
        try:
            cursor.execute(query_tables)
            break
        except Exception:
            conn.ping(True)
    results = cursor.fetchall()
    jsonResult = json.dumps(results)
    # some issues about json 
    return jsonify(status="OK", data=jsonResult)

@app.route("/coming_into_tables", methods=["POST"])
def coming_into_table():
    # it should be a post
    # when player click the table button in the first page, post this api to the server
    # in database, record the player number of each table
    # after receiving the post, player number + 1s
    table_id = request.form.get("table_id")
    player_id = request.form.get("player_id")
    query_player_num = "select players_num from mj_table where table_id = %s;"
    query_player_num_param = (table_id, )
    while True:
        try:
            cursor.execute(query_player_num, query_player_num_param)
            break
        except Exception:
            conn.ping(True)
    player_num_results = cursor.fetchall()
    player_num = player_num_results[0]["players_num"]
    if (player_num == 4):
        return jsonify(message="The table is full, sorry.", status = "ERROR")
    player_num += 1

    update_player_num = "update mj_tables set players_num = %s where table_id = %s;"
    update_player_num_param = (player_num, table_id)
    while True:
        try:
            cursor.execute(update_player_num, update_player_num_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)
    
    insert_table_player = "insert into table_player (table_id, player_id) values (%s, %s)"
    insert_table_player_param = (table_id, player_id)
    while True:
        try:
            cursor.execute(insert_table_player, insert_table_player_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)

    return jsonify(status="OK")

if __name__ == "__main__": 
    app.run(debug = True, host = '0.0.0.0', port='8080')
