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


def jsonify(args):
    return Response(json.dumps(args, cls=MongoJsonEncoder), mimetype='application/json')


@app.route("/")
def index():
    return jsonify({"versions": {"v1": "/v1"}})


@app.route("/v1/rates/<string:currency>")
def show_exchange_rate(currency):
    date = request.args.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
    query_filter = {
        'currency': currency,
        'date': {'$lte': datetime.datetime(*[int(i) for i in date.split('-')])}
    }
    rate = mongo.rates.find(query_filter, sort=[('date', -1)], limit=5)
    if rate is None:
        abort(404, 'Rate exchange not found')
    return jsonify(list(rate))

if __name__ == "__main__":
    app.run()
