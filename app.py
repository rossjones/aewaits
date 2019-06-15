from scraper import fetch_data 
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    data = fetch_data()
    return jsonify(data)
    
