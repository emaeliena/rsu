import datetime

from nose.tools import assert_equal

from utils import daterange


def test__rangedate_including():
    start_date = datetime.date(2016, 12, 12)
    end_date = datetime.date(2016, 12, 16)

    result = list(daterange(start_date, end_date))

    assert_equal(len(result), 5)


def test__rangedate_excluding():
    start_date = datetime.date(2016, 12, 12)
    end_date = datetime.date(2016, 12, 16)

    result = list(daterange(start_date, end_date, including=False))

    assert_equal(len(result), 4)
