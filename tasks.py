import datetime
import logging
import os

import celery
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import nbpapiclient
from utils import daterange


logging.basicConfig(level=logging.DEBUG)


MONGODB_URI = os.getenv('MONGODB_URI')


mongo_conn = MongoClient(MONGODB_URI)
mongo = mongo_conn.get_default_database()


app = celery.Celery('rsutasks', broker=os.getenv('REDIS_URL'), backend=MONGODB_URI)


@app.task
def store_exchange_rates(start_date, end_date, currency='USD', table='A'):
    result = nbpapiclient.get_exchange_rates(
        start_date,
        end_date,
        currency,
        table)
    if result.status_code not in [200, 404]:
        raise Exception(result.text)

    values = dict()
    for date in daterange(start_date, end_date):
        values[date.strftime('%Y-%m-%d')] = {
            'currency': currency,
            'date': datetime.datetime.combine(date, datetime.datetime.min.time()),
            'value': '-'
        }
    for rate in result.json()['rates']:
        values[rate['effectiveDate']]['value'] = rate['mid']
    for key, value in values.items():
        try:
            result = mongo.rates.insert(value)
            logging.debug(result)
        except DuplicateKeyError:
            logging.debug('exchange rate for {} at {} exists'.format(currency, value['date']))
    return 0

