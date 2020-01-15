#!/usr/bin/env python3
import json
from logger import log
from poi import Poi
from utils import ophrs2tsa


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
            self.opening_timestamps = [list(tsr) for tsr in ophrs2tsa(self.opening_hours)]

    def __repr__(self):
        content = {
            'name': self.name,
            'coordinates': self.coordinates,
            'duration of stay': self.duration
        }

        if hasattr(self, 'opening_hours'):
            content['opening hours'] = self.opening_hours
        if hasattr(self, 'city'):
            content['city'] = self.city
        if hasattr(self, 'amenity'):
            content['amenity'] = self.amenity

        return json.dumps(content, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    poi = Poi('pois/U Szwejka.json')
    target = Target(poi=poi, duration_of_stay=120)
    print(target)
