#!/usr/bin/env python3
import calendar
import folium
import humanize
import numpy as np
import time
from collections import namedtuple
from datetime import datetime, timedelta

_DAY_MAP = {
    'Mo': 0,
    'Tu': 1,
    'We': 2,
    'Th': 3,
    'Fr': 4,
    'Sa': 5,
    'Su': 6
}


def recursive_merge(inter, start_index=0):
    for i in range(start_index, len(inter) - 1):
        if inter[i][1] >= inter[i+1][0]:
            new_start = inter[i][0]
            new_end = inter[i+1][1]
            inter[i] = (new_start, new_end)
            del inter[i+1]
            return recursive_merge(inter.copy(), start_index=i)
    return inter


def str2ts(val):
    """Convert string to timestamp"""
    return calendar.timegm(time.strptime(val, "%Y-%m-%d %H:%M:%S"))


def ts2dt(val):
    """Convert timestamp to local datetime"""
    return datetime.fromtimestamp(val)


def i2dt(val):
    """Convert integer to timedelta"""
    if not val:
        return None
    return timedelta(seconds=val)


def str2dt(val, with_tz=False):
    """Convert string to datetime"""
    dt = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
    if with_tz:
        return dt.astimezone()
    return dt


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


def dt2strday(dt):
    """Convert datetime to string day"""
    weekday = dt.weekday()
    for v in _DAY_MAP:
        if _DAY_MAP[v] == weekday:
            return v
    return None


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

    if len(timestamp_list) < 2:
        return timestamp_list

    # Merge ranges
    return recursive_merge(timestamp_list.copy())


def _populate_datetime_ranges(opening_timestamps_week, start, end):
    start_midnight = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end_midnight = end.replace(hour=0, minute=0, second=0, microsecond=0)
    last_monday = start_midnight - timedelta(days=start_midnight.weekday())
    delta = end_midnight - last_monday
    weeks = int(delta.days / 7) + 1  # including not full week
    opening_datetimes = []

    for i in range(weeks):
        monday_delta_s = i * 604800
        for (tss, tse) in opening_timestamps_week:
            seconds_start = monday_delta_s + tss
            seconds_end = monday_delta_s + tse
            dts = last_monday + timedelta(seconds=seconds_start)
            dte = last_monday + timedelta(seconds=seconds_end)
            dtr = (dts, dte)

            if dts <= end and dte >= start:
                opening_datetimes.append(dtr)

    return opening_datetimes


def ohs2dtrstr(opening_hours_str, start, end):
    """Convert opening hours string to datetime ranges array within specified range in string"""
    start_dt = str2dt(start, with_tz=True)
    end_dt = str2dt(end, with_tz=True)
    return ohs2dtrdt(opening_hours_str=opening_hours_str, start_dt=start_dt, end_dt=end_dt)


def ohs2dtrdt(opening_hours_str, start_dt, end_dt):
    """Convert opening hour string to datetime ranges array withing specified range in datetime"""
    opening_timestamps_week = ophrs2tsa(opening_hours_str)
    datetimes = _populate_datetime_ranges(opening_timestamps_week, start=start_dt, end=end_dt)
    return datetimes


def get_bearing(p1, p2):
    '''
    Returns compass bearing from p1 to p2

    Parameters
    p1 : namedtuple with lat lon
    p2 : namedtuple with lat lon

    Return
    compass bearing of type float

    Notes
    Based on https://gist.github.com/jeromer/2005586
    '''

    long_diff = np.radians(p2.lon - p1.lon)

    lat1 = np.radians(p1.lat)
    lat2 = np.radians(p2.lat)

    x = np.sin(long_diff) * np.cos(lat2)
    y = (np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(long_diff)))

    bearing = np.degrees(np.arctan2(x, y))

    # adjusting for compass bearing
    if bearing < 0:
        return bearing + 360
    return bearing


def get_arrows(locations, color='blue', size=6, n_arrows=3):
    '''
    Get a list of correctly placed and rotated
    arrows/markers to be plotted

    Parameters
    locations : list of lists of lat lons that represent the
                start and end of the line.
                eg [[41.1132, -96.1993],[41.3810, -95.8021]]
    arrow_color : default is 'blue'
    size : default is 6
    n_arrows : number of arrows to create.  default is 3    Return
    list of arrows/markers
    '''

    Point = namedtuple('Point', field_names=['lat', 'lon'])

    # creating point from our Point named tuple
    p1 = Point(locations[0][0], locations[0][1])
    p2 = Point(locations[1][0], locations[1][1])

    # getting the rotation needed for our marker.
    # Subtracting 90 to account for the marker's orientation
    # of due East(get_bearing returns North)
    rotation = get_bearing(p1, p2) - 90

    # get an evenly space list of lats and lons for our arrows
    # note that I'm discarding the first and last for aesthetics
    # as I'm using markers to denote the start and end
    arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)[1:n_arrows+1]
    arrow_lons = np.linspace(p1.lon, p2.lon, n_arrows + 2)[1:n_arrows+1]

    arrows = []

    # creating each "arrow" and appending them to our arrows list
    for points in zip(arrow_lats, arrow_lons):
        arrows.append(folium.RegularPolygonMarker(location=points,
                      fill_color=color, number_of_sides=3,
                      radius=size, rotation=rotation))
    return arrows


def dt2hstr(dt):
    """Convert datetime to human string"""
    return humanize.naturaltime(dt)


def td2hstr(td):
    """Convert timedelta to human string"""
    return humanize.naturaldelta(td)


if __name__ == '__main__':
    opening_hours_str = 'Mo-Fr 08:00-00:00; Sa 07:00-08:00, 10:00-00:00; Su 00:00-04:00, 13:00-00:00'
    list_of_timestamps = ophrs2tsa(opening_hours_str)
    print('opening hours:', opening_hours_str)
    print('   list of ts:', list_of_timestamps)

    start = '2020-01-10 10:00:00'
    end = '2020-01-14 16:00:00'
    opening_datetimes = ohs2dtrstr(opening_hours_str, start=start, end=end)
    print('        range:', start, '-', end)
    print(' within range:', ['{} - {}'.format(dts, dte) for (dts, dte) in opening_datetimes])

    human_durations = []
    for dt_range in opening_datetimes:
        dt_delta = dt_range[1] - dt_range[0]
        duration = td2hstr(dt_delta)
        human_durations.append(duration)
    print('    human str:', human_durations)
