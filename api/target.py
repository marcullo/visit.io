#!/usr/bin/env python3
import json
from logger import log
from params import Params
from poi import Poi
from utils import ohs2dtrdt


class Target:
    DEFAULT_OPENING_HOURS = {
        'global': 'Mo-Su 00:00-24:00',
        'restaurant': 'Mo-Su 12:00-22:00'
    }

    def __init__(self, poi, duration_of_stay):
        self.duration = duration_of_stay
        self.name = poi.name
        self.coordinates = poi.coordinates

        if hasattr(poi, 'city'):
            self.city = poi.city
        if hasattr(poi, 'amenity'):
            self.amenity = poi.amenity

        if hasattr(poi, 'opening_hours'):
            self.opening_hours = poi.opening_hours
            self.opening_timestamps = [list(tsr) for tsr in poi.opening_timestamps]
        else:
            opening_hours = self.DEFAULT_OPENING_HOURS['global']
            if hasattr(self, 'amenity'):
                if self.amenity in self.DEFAULT_OPENING_HOURS:
                    opening_hours = self.DEFAULT_OPENING_HOURS[self.amenity]

            log('Warning: {} does not have opening hours. Assuming {}!'.format(poi.name, opening_hours))
            self.opening_hours = opening_hours

    def __repr__(self):
        content = {
            'name': self.name,
            'coordinates': self.coordinates,
            'duration of stay': self.duration
        }

        if hasattr(self, 'opening_datetimes'):
            content['opening hours'] = [[str(dts), str(dte)] for (dts, dte) in self.opening_datetimes]
        if hasattr(self, 'city'):
            content['city'] = self.city
        if hasattr(self, 'amenity'):
            content['amenity'] = self.amenity

        return json.dumps(content, indent=2, ensure_ascii=False)

    def set_opening_timestamps_in_range(self, start_dt, end_dt):
        self.opening_datetimes = ohs2dtrdt(self.opening_hours, start_dt=start_dt, end_dt=end_dt)
        self.opening_timestamps = [[int(dts.timestamp()), int(dte.timestamp())] for dts, dte in self.opening_datetimes]


if __name__ == '__main__':
    params = Params('params/example.json')
    poi = Poi('pois/U Szwejka.json')
    target = Target(poi=poi, duration_of_stay=120)
    target.set_opening_timestamps_in_range(start_dt=params.from_at, end_dt=params.to_at)
    print(target)
