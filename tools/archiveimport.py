import csv
import datetime
import io
import logging
import os
import re
import sys

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pymongo import MongoClient
import requests


ARCHIVE_URL = 'http://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_2016.csv'


logging.basicConfig(level=logging.DEBUG)


conn = MongoClient(os.getenv('MONGODB_URI'))
mongo = conn.get_default_database()


cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': 'data',
    'cache.lock_dir': 'lock'
}


cache = CacheManager(**parse_cache_config_options(cache_opts))


def get_etag(url):
    result = requests.head(url)
    if 'ETag' not in result.headers:
        raise ValueError('No ETag in response headers')
    return result.headers['ETag']


@cache.cache('download_archive', type='file')
def download_archive(url, *args, **kwargs):
    result = requests.get(url)
    result.encoding = 'iso-8859-2'
    return result.text


def get_archive(url):
    etag = get_etag(url)
    logging.debug('ETag: {}'.format(etag))
    return download_archive(url, etag)


def extract_currency_rates(archive, currency_code):
    f = io.StringIO(archive)
    reader = csv.reader(f, delimiter=';')
    header_codes = next(reader)
    header_names = next(reader)
    values = list()
    for row in reader:
        if len(row) < 1 or not re.fullmatch('\d{8}', row[0]):
            break
        values.append(row)
    footer_units = next(reader)
    currency_index = footer_units.index(currency_code)
    footer_names = next(reader)
    footer_nums = next(reader)
    for entry in values:
        rate = list(zip(entry, footer_units))[currency_index]
        yield {'date': datetime.datetime.strptime(entry[0], '%Y%m%d'), 'value': rate[0], 'currency': rate[1], 'per': footer_nums[currency_index]}


def save(entry):
    mongo.rates.insert(entry)


def main():
    archive = get_archive(ARCHIVE_URL)
    logging.debug('archive length: {}'.format(len(archive)))
    for rate_entry in extract_currency_rates(archive, 'USD'):
        save(rate_entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
