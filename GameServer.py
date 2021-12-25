from random import random
from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json
import redis
import Mahjong
import random

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="mahjong",
    passwd="mahjongpsw",
    database="mahjongdb",
    autocommit=True
)
cursor = conn.cursor(dictionary=True)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  

@app.route("/get_order", methods=["POST"])
def get_order():
    # 获取房间内四位玩家的id （String)
    
    player_id = request.form.get("player_id")
    table_id = request.form.get("table_id")

    select_player = "select player_id from table_player where table_id = %s and still_in_table = '1'"
    select_player_param = (table_id, )
    while True:
        try:
            cursor.execute(select_player, select_player_param)
            # conn.commit()
            break
        except Exception:
            conn.ping(True)
    results = cursor.fetchall()
    print(results)
    list = []
    for single in results:
        print(1)
        list.append(single["player_id"])
    
    json_dict = {}
    json_dict["player_order"] = list.index(player_id) + 1
    return json.dumps(json_dict)


@app.route("/start_game", methods=["POST"])
def start_game():
    # 首先需要对该局游戏创建麻将list
    # 为每位玩家发牌 
    # 返回json
    # player1: 麻将list
    # player2: 麻将list
    table_id = request.form.get("table_id")

    redis_table_key = "table" + table_id
    player_num = r.get(redis_table_key)
    if(int(player_num) < 4):
        return jsonify(message="wait until 4 players.", status = "ERROR")
    
    mj_list = []
    for i in range(108):
        mj_list.append(i)
    random.shuffle(mj_list)
    redis_mj_key = "mj" + table_id
    for i in mj_list:
        r.rpush(redis_mj_key, i)  

    redis_player1_key = "mj" + table_id + "player1"
    redis_player2_key = "mj" + table_id + "player2"
    redis_player3_key = "mj" + table_id + "player3"
    redis_player4_key = "mj" + table_id + "player4"

    player1_list = []
    player2_list = []
    player3_list = []
    player4_list = []
    for i in range(14):
        player1_list.append(r.rpop(redis_mj_key))
    for i in range(13):
        player2_list.append(r.rpop(redis_mj_key))
    for i in range(13):
        player3_list.append(r.rpop(redis_mj_key))
    for i in range(13):
        player4_list.append(r.rpop(redis_mj_key))

    for i in player1_list:
        r.rpush(redis_player1_key, i)
    for i in player2_list:
        r.rpush(redis_player2_key, i)
    for i in player3_list:
        r.rpush(redis_player3_key, i)
    for i in player4_list:
        r.rpush(redis_player4_key, i)
    
    json_dict = {}
    json_dict["player1"] = player1_list
    json_dict["player2"] = player2_list
    json_dict["player3"] = player3_list
    json_dict["player4"] = player4_list
    json_dict["order"] = 1

    json_str = json.dumps(json_dict)

    return json_str
    

@app.route("/next", methods=["POST"])
def next():
    # 玩家出牌之后call this function
    # 改变出牌玩家
    # 为下一个玩家随机发一张牌
    # 1. 要知道谁打了哪张牌

    table_id = request.form.get("table_id")
    player_order = request.form.get("player_order")
    mj = request.form.get("mj")

    redis_mj_key = "mj" + table_id
    redis_player_order_key = "mj" + table_id + "player" + player_order

    # 出牌，删除改牌在list中的位置
    r.lrem(redis_player_order_key, 0, mj)
    
    player_order_int = int(player_order)
    if int(player_order) == 4:
        player_order_int = 1
    else:
        player_order_int += 1
    
    # 给下一位玩家发一张牌
    redis_newplayer_key = "mj" + table_id + "player" + str(player_order_int)
    new_mj = r.rpop(redis_mj_key)
    r.rpush(redis_newplayer_key, mj)

    json_dict = {}
    json_dict["order"] = player_order_int
    json_dict["mj"] = new_mj
    json_str = json.dumps(json_dict)

    return json_str
    


@app.route("/peng")
def peng():
    # 玩家点击碰后触发
    # 改变出牌顺序
    pass

@app.route("/win")
def win():
    # 开始下一回合，应该和start_game类似
    pass


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8083')
