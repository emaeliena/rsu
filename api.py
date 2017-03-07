import datetime
import json
import os

from bson.objectid import ObjectId
from flask import Flask, request
from pymongo import MongoClient
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response

MONGODB_URI = os.getenv('MONGODB_URI')


app = application = Flask(__name__)
mongo_conn = MongoClient(MONGODB_URI)
mongo = mongo_conn.get_default_database()


mongo.connections.insert({'dt': datetime.datetime.now()})


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')


@app.route("/")
def index():
    return jsonify({"versions": {"v1": "/v1"}})


@app.route("/v1/rates/<string:currency>")
def show_exchange_rate(currency):
    date = request.args.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
    rate = mongo.rates.find_one({'currency': currency, 'date': date})
    if rate is None:
        abort(404, 'Rate exchange not found')
    return jsonify(rate)

if __name__ == "__main__":
    app.run()
