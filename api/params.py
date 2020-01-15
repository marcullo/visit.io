#!/usr/bin/env python3
import json
from datetime import datetime
from logger import log
from utils import str2dt, strhr2sec


class Params:
    def __init__(self, path):
        with open(path) as f:
            raw = json.load(f)
            available = raw['available']

        self.city = raw['city']
        self.from_place = available['from']['place']
        self.from_at = str2dt(available['from']['at'])
        self.to_place = available['to']['place']
        self.to_at = str2dt(available['to']['at'])
        self.pois = raw['pois']
        self.profile = raw['profile']

        profiles = [
            'driving-car',
            'foot-walking',
            'cycling-regular',
            'cycling-road'
        ]
        if self.profile not in profiles:
            raise AssertionError('Profile {} not supported'.format(self.profile))

    def __repr__(self):
        content = {
            'city': self.city,
            'available': {
                'from': {
                    'place': self.from_place,
                    'at': str(self.from_at)
                },
                'to': {
                    'place': self.to_place,
                    'at': str(self.to_at)
                }
            },
            'pois': self.pois,
            'profile': self.profile
        }

        if hasattr(self, 'from_coordinates'):
            content['available']['from']['coordinates'] = self.from_coordinates
        if hasattr(self, 'to_coordinates'):
            content['available']['to']['coordinates'] = self.to_coordinates

        return json.dumps(content, indent=2, ensure_ascii=False)

    def set_coordinates(self, coord_from, coord_to):
        self.from_coordinates = coord_from
        self.to_coordinates = coord_to

    def set_relative_time_window(self):
        from_datetime = datetime.fromtimestamp(self.from_at)
        to_datetime = datetime.fromtimestamp(self.to_at)

        from_day_s = from_datetime.weekday() * 86400
        from_hour_s = strhr2sec(str(from_datetime.time())[:5])
        to_day_s = to_datetime.weekday() * 86400
        to_hour_s = strhr2sec(str(to_datetime.time())[:5])

        self.from_at = from_day_s + from_hour_s
        self.to_at = to_day_s + to_hour_s


if __name__ == '__main__':
    params = Params('params/example.json')
    params.set_coordinates(coord_from=[1.0, 2.0], coord_to=[3.0, 4.0])
    log(params, indent=0)
