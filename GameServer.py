from flask.wrappers import Request
import mysql.connector
from flask import Flask, request, jsonify, json

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="mahjong",
    passwd="mahjongpsw",
    database="mahjongdb",
)
cursor = conn.cursor(dictionary=True)

@app.route("/start_game")
def start_game():
    # 首先需要对该局游戏创建麻将list
    # 为每位玩家发牌 
    # 返回json
    # player1: 麻将list
    # player2: 麻将list
    pass

@app.route("/next")
def next():
    # 玩家出牌之后call this function
    # 改变出牌玩家
    # 为下一个玩家随机发一张牌
    pass

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
