import requests
import json
from logger import log
from .utils import str2ts


class Params:
    def __init__(self, path):
        with open(path) as f:
            raw = json.load(f)
            available = raw['available']

        self.raw = raw
        self.city = raw['city']
        self.from_place = available['from']['place']
        self.from_at = str2ts(available['from']['at'])
        self.to_place = available['to']['place']
        self.to_at = str2ts(available['to']['at'])
        self.pois = raw['pois']

    def __repr__(self):
        return json.dumps(self.raw, indent=2, ensure_ascii=False)


def request_point(name, api_key, city=None, osm_only=False):
    endpoint = 'https://api.openrouteservice.org/geocode/search'
    payload = {
        'api_key': api_key,
        'boundary.country': 'PL',
        'size': '1'
    }
    payload['text'] = name

    if osm_only:
        payload['sources'] = ['osm']

    if city:
        payload['boundary.rect.min_lon'] = city.bbox[0]
        payload['boundary.rect.min_lat'] = city.bbox[1]
        payload['boundary.rect.max_lon'] = city.bbox[2]
        payload['boundary.rect.max_lat'] = city.bbox[3]

    res = requests.get(endpoint, params=payload)
    res.raise_for_status()
    log('ors/geocode: got {}'.format(name))

    return res.json()


def request_node(id, api_key):
    endpoint = 'https://api.openstreetmap.org/api/0.6/node/{}'.format(id)
    res = requests.get(endpoint)
    res.raise_for_status()
    log('ors/node: got {}'.format(id))

    return res.text
