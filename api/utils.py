#!/usr/bin/env python3


import calendar
import time

_DAY_MAP = {
    'Mo': 1,
    'Tu': 2,
    'We': 3,
    'Th': 4,
    'Fr': 5,
    'Sa': 6,
    'Su': 7
}


def str2ts(val):
    """Convert string to timestamp"""
    return calendar.timegm(time.strptime(val, "%Y-%m-%d %H:%M:%S"))


def strhr2sec(hour):
    """Convert string hour o'clock to seconds"""
    hours, minutes = hour.split(':')
    hours = int(hours)
    minutes = int(minutes)
    seconds = 3600 * hours + 60 * minutes
    return seconds


def strday2sec(day):
    """Convert string day to seconds"""
    return _DAY_MAP[day] * 86400


def sec2strday(seconds):
    """Convert seconds to string day"""
    day_nr = int(seconds / 86400)
    return _DAY_MAP.values().index(day_nr)


def sec2strhr(seconds):
    """Convert seconds to string hour o'clock"""
    hours = int(seconds / 3600)
    seconds -= hours * 3600
    minutes = int(seconds / 60)
    return '{:02}:{:02}'.format(hours, minutes)


def ophrs2tsa(opening_hours_str):
    """Convert opening hours string to list of timestamps"""
    tokens = opening_hours_str.strip().split('; ')

    timestamp_list = []

    for token in tokens:
        _drange, _hranges = token.split(' ', 1)

        hours = []
        days = _drange.split('-')
        _hranges = _hranges.split(', ')

        for h in _hranges:
            h = h.split('-')
            h = list(map(lambda e: strhr2sec(e), h))
            if h[0] > h[1] and h[1] == 0:
                h[1] = strhr2sec('24:00')
            hours.append((h[0], h[1]))

        days = list(map(lambda d: strday2sec(d), days))
        days_st = days[0]
        days_sp = days[1] if len(days) > 1 else days[0]

        for d in range(days_st, days_sp + 1, 86400):
            for h in hours:
                ts = (d + h[0], d + h[1])
                timestamp_list.append(ts)

    return timestamp_list


if __name__ == '__main__':
    opening_hours_str = 'Mo-Fr 08:00-00:00; Sa 07:00-08:00, 10:00-00:00; Su 13:00-00:00'
    list_of_timestamps = ophrs2tsa(opening_hours_str)
    print('opening hours:', opening_hours_str)
    print('   list of ts:', list_of_timestamps)
