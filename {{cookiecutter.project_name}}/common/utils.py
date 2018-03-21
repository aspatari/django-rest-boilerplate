import datetime

from django.utils import timezone


def get_time_with_offset(offset):
    """
    Get a DateTime object with added time offset
    :param offset: Dictionary with one of keys one from `days`, `hours`
    :return: DateTime object with added time offset
    """
    assert len(offset.keys()) == 1 and list(offset.keys())[0] in ['days', 'hours', 'minutes'], (
        "Argument must be just one from list ['days', 'hours','minutes'] ")

    current_time = timezone.localtime()

    return current_time + datetime.timedelta(**offset)
