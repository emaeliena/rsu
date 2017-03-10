import requests


API_URL = 'http://api.nbp.pl/api/exchangerates/rates'


def get_exchange_rate(date, currency='USD', table='A'):
    result = requests.get('{}/{}/{}/{}'.format(API_URL, table, currency, date))
    return result


def get_exchange_rates(startDate, endDate, currency='USD', table='A'):
    result = requests.get('{}/{}/{}/{}/{}'.format(API_URL, table, currency, startDate, endDate))
    return result
