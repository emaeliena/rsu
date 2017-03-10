import os

from pymongo import MongoClient

MONGODB_URI = os.getenv('MONGODB_URI')


mongo_conn = MongoClient(MONGODB_URI)
mongo = mongo_conn.get_default_database()
