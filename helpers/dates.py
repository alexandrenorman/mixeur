import functools
import datetime
import calendar
from dateutil.rrule import rrule, MONTHLY, DAILY


@functools.lru_cache(maxsize=128)
def months_of_period(from_date, to_date):
    from_date = from_date.replace(day=1)
    return [dt.date() for dt in rrule(MONTHLY, dtstart=from_date, until=to_date)]


def months_of_year(year):
    return months_of_period(datetime.date(year, 1, 1), datetime.date(year, 12, 31))


@functools.lru_cache(maxsize=128)
def days_of_period(from_date, to_date):
    return [day.date() for day in rrule(DAILY, dtstart=from_date, until=to_date)]


@functools.lru_cache(maxsize=128)
def days_of_year(year):
    return days_of_period(datetime.date(year, 1, 1), datetime.date(year, 12, 31))


@functools.lru_cache(maxsize=512)
def first_day_of_month(date):
    return datetime.date(date.year, date.month, 1)


@functools.lru_cache(maxsize=512)
def last_day_of_month(date):
    return datetime.date(
        date.year, date.month, calendar.monthrange(date.year, date.month)[1]
    )
