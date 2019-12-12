#!/usr/bin/env python3
import json
from utils import ophrs2tsa


class Poi:
    def __init__(self, filename=None, from_node=False, content=None):
        if from_node:
            self._init_from_node(content)
        else:
            with open(filename) as f:
                try:
                    content = json.load(f)
                    self._init_itself_alone(content)
                except json.decoder.JSONDecodeError:
                    raise AssertionError('Invalid content of city file: {}'.format(filename)) from None

    def _init_from_node(self, content):
        self.name = content.name
        self.id = content.id
        self.coordinates = content.coordinates

        if hasattr(content, 'city'):
            self.city = content.city
        if hasattr(content, 'amenity'):
            self.amenity = content.amenity
        if hasattr(content, 'opening_hours'):
            self.opening_hours = content.opening_hours
            self.opening_timestamps = content.opening_timestamps

    def _init_itself_alone(self, content):
        self.name = content['name']
        self.id = content['id']
        self.coordinates = content['coordinates']

        if 'city' in content:
            self.city = content['city']
        if 'amenity' in content:
            self.amenity = content['amenity']
        if 'opening hours' in content:
            self.opening_hours = content['opening hours']
            self.opening_timestamps = ophrs2tsa(self.opening_hours)

    def __repr__(self):
        content = {
            'name': self.name,
            'id': self.id,
            'coordinates': self.coordinates
        }

        if hasattr(self, 'city'):
            content['city'] = self.city
        if hasattr(self, 'amenity'):
            content['amenity'] = self.amenity
        if hasattr(self, 'opening_hours'):
            content['opening hours'] = self.opening_hours

        return json.dumps(content, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    poi = Poi('pois/U Szwejka.json')
    print(poi)
