#!/usr/bin/env python3
import sys
sys.path.insert(0, 'api')

from api.argparser import parse_args
from api.city import City
from api.db import Database
from api.geocode import Geocode
from api.poi import Poi
from api.logger import log
from api.openrouteservice import Params, request_point, request_node


class Fetch:
    def __init__(self, db, api_key):
        self._db = db
        self._api_key = api_key

    def city(self, name):
        city = Fetch.try_fetch(self._db.get_city, name)

        if city:
            return city

        content = request_point(name=name, api_key=self._api_key)
        id = Geocode.get_id(content)
        name = Geocode.get_name(content)
        geocode = self._db.put_geocode(id=id, content=content)
        city = City(from_geocode=True, content=geocode)
        city = self._db.put_city(name=name, content=city)
        return city

    def poi(self, name, city=None):
        poi = Fetch.try_fetch(self._db.get_poi, name)

        if poi:
            return poi

        content = request_point(
            name=name,
            api_key=self._api_key,
            city=city,
            osm_only=True)

        try:
            id = Geocode.get_id(content)
        except BufferError as e:
            log('Warning: {}'.format(e))
            log('Skipping: {}'.format(name))
            return None

        name = Geocode.get_name(content)
        self._db.put_geocode(id=id, content=content)

        content = request_node(id=id, api_key=self._api_key)
        node = self._db.put_node(id=id, content=content)

        poi = Poi(from_node=True, content=node)
        poi = self._db.put_poi(name=name, content=poi)

        return poi

    def stats(self):
        self._db.print_stats()

    @staticmethod
    def try_fetch(query, argument):
        try:
            city = query(argument)
        except AssertionError:
            log('Warning: Invalid content of {}!'.format(argument))
            city = None

        return city


if __name__ == '__main__':
    try:
        args = parse_args()
        db = Database()
        fetch = Fetch(db=db, api_key=args.api_key)
        params = Params(args.params)

        city = params.city
        pois = params.pois

        if len(pois) > 20:
            input('Do you really want to process {} pois? (Enter)'.format(len(pois)))

        city = fetch.city(name=city)
        log(city, indent=0, verbose=True)

        for poi in pois:
            poi = fetch.poi(name=poi, city=city)
            if poi:
                log(poi, indent=0, verbose=True)

        fetch.stats()
    except (KeyboardInterrupt):
        print()
