#!/usr/bin/env python3
import json


class Geocode:
    def __init__(self, filename):
        with open(filename) as f:
            content = json.load(f)

        features = content['features'][0]
        properties = features['properties']
        self.name = properties['name']
        self.id = int(properties['id'].replace('node/', ''))
        self.country = properties['country']
        self.coordinates = features['geometry']['coordinates']
        self.bbox = content['bbox']
        self.source = properties['source']

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'id': self.id,
            'country': self.country,
            'coordinates': self.coordinates,
            'bbox': self.bbox,
            'source': self.source
        }, indent=2, ensure_ascii=False)

    def is_osm(self):
        return self.source == 'openstreetmap'

    @staticmethod
    def get_id(content):
        try:
            features = content['features']

            if len(features) == 0:
                id = content['geocoding']['query']['text']
                raise IndexError()

            properties = features[0]['properties']
            id = properties['id']

            return int(id.replace('node/', ''))
        except (IndexError, ValueError):
            raise BufferError('Unsupported node: {}'.format(id)) from None

    @staticmethod
    def get_name(content):
        properties = content['features'][0]['properties']
        return properties['name']


if __name__ == '__main__':
    geocode = Geocode('geocodes/1366473642.json')
    print(geocode)
