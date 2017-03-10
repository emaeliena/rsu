import datetime
import json

from bson.objectid import ObjectId
from flask import Flask
from werkzeug.wrappers import Response

import tasks
from db import mongo
from utils import daterange, datetime_obj_from_str, date_obj_from_str

app = application = Flask(__name__)
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


@app.route("/v1/rates/<string:currency>/<string:date_start>/<string:date_end>")
def show_exchange_rate(currency, date_start, date_end):
    query_filter = {
        'currency': currency,
        'date': {
            '$gte': datetime_obj_from_str(date_start),
            '$lte': datetime_obj_from_str(date_end)
        }
    }
    rates = list(mongo.rates.find(query_filter, sort=[('date', -1)]))
    if len(rates) != len(list(daterange(date_start, date_end))):
        tasks.store_exchange_rates.delay(date_start, date_end)
        response = jsonify({'status': 'preparing data...'})
    else:
        response = jsonify(rates)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route("/v1/delegate/<string:date>")
def delegate(date):
    result = tasks.store_rate.delay(date)
    return jsonify({'status': 'ok', 'task_id': getattr(result, 'task_id', 'no task_id attribute found')})


@app.route("/v1/tasks/<string:task_id>")
def check_task(task_id):
    result = tasks.add.AsyncResult(task_id)
    return jsonify({
        'failed': result.failed(),
        'id': result.id,
        'ready': result.ready(),
        'status': result.status,
        'successful': result.successful(),
        'result': result.result
    })

if __name__ == "__main__":
    app.run()
