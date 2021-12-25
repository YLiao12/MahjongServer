from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json
import redis

app = Flask(__name__)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  

conn = mysql.connector.connect(
  host="localhost",       
  user="mahjong",    
  passwd="mahjongpsw",   
  database = "mahjongdb",
)
cursor = conn.cursor(dictionary = True)

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
    player_id = request.form.get("player_id")
    insert_player = "insert into players (player_id, name) values (%s, %s)"
    insert_player_param = (player_id, player_name)
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

#进入房间，table表players_num ++，Table_player表Still_in_table设为1
@app.route("/coming_into_tables", methods=["POST"])
def coming_into_table():
    # it should be a post
    # when player click the table button in the first page, post this api to the server
    # in database, record the player number of each table
    # after receiving the post, player number + 1s
    table_id = request.form.get("table_id")
    player_id = request.form.get("player_id")
    # query_player_num = "select players_num from mj_tables where table_id = %s;"
    # query_player_num_param = (table_id, )
    redis_table_key = "table" + table_id
    
    # while True:
    #     try:
    #         cursor.execute(query_player_num, query_player_num_param)
    #         break
    #     except Exception:
    #         conn.ping(True)
    # player_num_results = cursor.fetchall()
    # player_num = player_num_results[0]["players_num"]
    player_num = r.get(redis_table_key)
    if (int(player_num) == 4):
        return jsonify(message="The table is full, sorry.", status = "ERROR")
    # player_num += 1

    r.incr(redis_table_key)
    player_num = r.get(redis_table_key)
    update_player_num = "update mj_tables set players_num = %s where table_id = %s;"
    update_player_num_param = (player_num, table_id)
    while True:
        try:
            cursor.execute(update_player_num, update_player_num_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)

    still_in_table = 1

    insert_table_player = "insert into table_player (table_id, player_id, Still_in_table) values (%s)"
    insert_table_player_param = (table_id, player_id, still_in_table)

    # if (int(table_id) == 1):
    #     print(1)
    #     insert_table_player = "insert into table1 (player_id) values (%s)"
    #     insert_table_player_param = (player_id, )
    
    # if (int(table_id) == 2):
    #     print(2)
    #     insert_table_player = "insert into table2 (player_id) values (%s)"
    #     insert_table_player_param = (player_id, )
    
    # if (int(table_id) == 3):
    #     print(3)
    #     insert_table_player = "insert into table3 (player_id) values (%s)"
    #     insert_table_player_param = (player_id, )

    while True:
        try:
            cursor.execute(insert_table_player, insert_table_player_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)

    return jsonify(status="OK")

#离开房间，table表players_num --，Table_player表Still_in_table设为0
@app.route("/leaving_tables", methods=["POST"])
def leaving_tables():
    table_id = request.form.get("table_id")
    player_id = request.form.get("player_id")
    redis_table_key = "table" + table_id
    # query_player_num = "select players_num from mj_tables where table_id = %s;"
    # query_player_num_param = (table_id, )
    # while True:
    #     try:
    #         cursor.execute(query_player_num, query_player_num_param)
    #         break
    #     except Exception:
    #         conn.ping(True)
    # player_num_results = cursor.fetchall()
    # player_num = player_num_results[0]["players_num"]
    # player_num -= 1

    r.decr(redis_table_key)
    player_num = r.get(redis_table_key)
    update_player_num = "update mj_tables set players_num = %s where table_id = %s;"
    update_player_num_param = (player_num, table_id)
    while True:
        try:
            cursor.execute(update_player_num, update_player_num_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)
    
    update_table_player = "update table_player set still_in_table = 0 where table_id = %s and player_id = %s "
    update_table_player_param = (table_id, player_id)

    # delete_table_player = "delete from %s where player_id = %s"
    # delete_table_player_param = (redis_table_key, player_id)

    # if (int(table_id) == 1):
    #     delete_table_player = "delete from table1 where player_id = %s"
    #     delete_table_player_param = (player_id, )
    
    # if (int(table_id) == 2):
    #     delete_table_player = "delete from table2 where player_id = %s"
    #     delete_table_player_param = (player_id, )
    
    # if (int(table_id) == 3):
    #     delete_table_player = "delete from table3 where player_id = %s"
    #     delete_table_player_param = (player_id, )

    while True:
        try:
            cursor.execute(update_table_player, update_table_player_param)
            conn.commit()
            break
        except Exception:
            conn.ping(True)

    return jsonify(status="OK")

if __name__ == "__main__": 
    app.run(debug = True, host = '0.0.0.0', port='8080')
