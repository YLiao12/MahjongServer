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

@app.route("/get_tables")
def get_tables():
    # get records from mysql
    # change records into json
    # return json
    query_tables = "SELECT * FROM mj_tables ORDER BY id ASC"
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

@app.route("/coming_into_tables")
def coming_into_table():
    # it should be a post
    # when player click the table button in the first page, post this api to the server
    # in database, record the player number of each table
    # after receiving the post, player number + 1s


if __name__ == "__main__": 
    app.run(debug = True, host = '0.0.0.0', port='8080')