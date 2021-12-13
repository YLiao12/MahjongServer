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

