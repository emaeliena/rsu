from datetime import date
from datetime import datetime as dt
from datetime import timedelta


def daterange(start_date, end_date, including=True):
    if not isinstance(start_date, date):
        start_date = date_obj_from_str(start_date)
    if not isinstance(end_date, date):
        end_date = date_obj_from_str(end_date)
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
    if including:
        yield start_date + timedelta(n+1)


def date_obj_from_str(datestring):
    return date(*[int(elem) for elem in datestring.split('-')])


def datetime_obj_from_str(datestring):
    return dt.combine(date_obj_from_str(datestring), dt.min.time())
