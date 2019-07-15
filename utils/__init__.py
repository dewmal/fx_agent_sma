import datetime
import math


def round_time(timestamp=None, lapse=0):
    """
    Round a timestamp to a lapse according to specified minutes

    Usage:

    >>> import datetime, math
    >>> round_time(datetime.datetime(2010, 6, 10, 3, 56, 23), 0)
    datetime.datetime(2010, 6, 10, 3, 56)
    >>> round_time(datetime.datetime(2010, 6, 10, 3, 56, 23), 1)
    datetime.datetime(2010, 6, 10, 3, 57)
    >>> round_time(datetime.datetime(2010, 6, 10, 3, 56, 23), -1)
    datetime.datetime(2010, 6, 10, 3, 55)
    >>> round_time(datetime.datetime(2019, 3, 11, 9, 22, 11), 3)
    datetime.datetime(2019, 3, 11, 9, 24)
    >>> round_time(datetime.datetime(2019, 3, 11, 9, 22, 11), 3*60)
    datetime.datetime(2019, 3, 11, 12, 0)
    >>> round_time(datetime.datetime(2019, 3, 11, 10, 0, 0), 3)
    datetime.datetime(2019, 3, 11, 10, 0)

    :param timestamp: Timestamp to round (default: now)
    :param lapse: Lapse to round in minutes (default: 0)
    """
    t = timestamp or datetime.datetime.now()  # type: Union[datetime, Any]
    surplus = datetime.timedelta(seconds=t.second, microseconds=t.microsecond)
    t -= surplus
    try:
        mod = t.minute % lapse
    except ZeroDivisionError:
        return t
    if mod:  # minutes % lapse != 0
        t += datetime.timedelta(minutes=math.ceil(t.minute / lapse) * lapse - t.minute)
    elif surplus != datetime.timedelta() or lapse < 0:
        t += datetime.timedelta(minutes=(t.minute / lapse + 1) * lapse - t.minute)
    return t


def round_seconds(date_time_object):
    new_date_time = date_time_object

    if new_date_time.microsecond >= 500000:
        new_date_time = new_date_time + datetime.timedelta(seconds=1)

    return new_date_time.replace(microsecond=0)
