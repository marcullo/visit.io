#!/usr/bin/env python3
import json


class City:
    def __init__(self, filename=None, from_geocode=False, content=None):
        if from_geocode:
            self._init_from_geocode(content)
        else:
            with open(filename) as f:
                try:
                    content = json.load(f)
                    self._init_itself_alone(content)
                except json.decoder.JSONDecodeError:
                    raise AssertionError('Invalid content of city file: {}'.format(filename)) from None

    def _init_from_geocode(self, content):
        self.name = content.name
        self.country = content.country
        self.coordinates = content.coordinates
        self.bbox = content.bbox

    def _init_itself_alone(self, content):
        self.name = content['name']
        self.country = content['country']
        self.coordinates = content['coordinates']
        self.bbox = content['bbox']

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'country': self.country,
            'coordinates': self.coordinates,
            'bbox': self.bbox
        }, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    city = City('cities/Warszawa.json')
    print(city)
