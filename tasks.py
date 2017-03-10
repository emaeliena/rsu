import os
import time

import celery


app = celery.Celery('rsutasks', broker=os.getenv('REDIS_URL'), backend=os.getenv('MONGODB_URI'))


@app.task
def add(x, y):
    time.sleep(5)
    return x + y
