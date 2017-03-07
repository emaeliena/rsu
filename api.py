import datetime
import os

from flask import Flask, jsonify
from pymongo import MongoClient


MONGODB_URI = os.getenv('MONGODB_URI')


app = application = Flask(__name__)
mongo_conn = MongoClient(MONGODB_URI)
mongo = mongo_conn.get_default_database()


mongo.connections.insert({'dt': datetime.datetime.now()})


@app.route("/")
def index():
    return jsonify({"versions": {"v1": "/v1"}})

if __name__ == "__main__":
    app.run()
