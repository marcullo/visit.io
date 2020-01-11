#!/usr/bin/env python3
import calendar
import folium
import numpy as np
import time
from collections import namedtuple

_DAY_MAP = {
    'Mo': 1,
    'Tu': 2,
    'We': 3,
    'Th': 4,
    'Fr': 5,
    'Sa': 6,
    'Su': 7
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

    if len(timestamp_list) < 2:
        return timestamp_list

    # Merge ranges
    return recursive_merge(timestamp_list.copy())


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


if __name__ == '__main__':
    opening_hours_str = 'Mo-Fr 08:00-00:00; Sa 07:00-08:00, 10:00-00:00; Su 00:00-04:00, 13:00-00:00'
    list_of_timestamps = ophrs2tsa(opening_hours_str)
    print('opening hours:', opening_hours_str)
    print('   list of ts:', list_of_timestamps)
