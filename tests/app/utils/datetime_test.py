import datetime

from app.utils.datetime import utc_now


def test_should_utc_now():
    now = utc_now()
    assert type(now) == datetime.datetime
