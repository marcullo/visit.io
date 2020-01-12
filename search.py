#!/usr/bin/env python3
import sys
sys.path.insert(0, 'api')

from api.argparser import parse_args
from api.city import City
from api.db import Database
from api.geocode import Geocode
from api.optimization import Optimization
from api.params import Params
from api.poi import Poi
from api.target import Target
from api.visualize import visualize
from api.logger import log
from api.openrouteservice import request_point, request_node, request_route_optimization


class Fetch:
    def __init__(self, db, profile, api_key):
        self._db = db
        self._profile = profile
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
            id, type = Geocode.get_id_type(content)
        except BufferError as e:
            log('Warning: {}'.format(e))
            log('Skipping: {}'.format(name))
            return None

        name = Geocode.get_name(content)
        self._db.put_geocode(id=id, content=content)

        if type == 'polyline':
            geocode = Fetch.try_fetch(self._db.get_geocode, id)
            poi = Poi(init_from='geocode', content=geocode)
        else:
            content = request_node(id=id, api_key=self._api_key)
            node = self._db.put_node(id=id, content=content)
            poi = Poi(init_from='node', content=node)

        poi = self._db.put_poi(name=name, content=poi)

        return poi

    def point(self, name, city):
        return self.poi(name=name, city=city)

    def stats(self):
        self._db.print_stats()

    def optimization(self, targets, params):
        if not targets:
            log('Warning: Nothing to optimize!')
            exit(0)

        content = request_route_optimization(targets=targets, params=params, profile=self._profile, api_key=self._api_key)

        return content

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
        params = Params(args.params)
        fetch = Fetch(db=db, profile=params.profile, api_key=args.api_key)

        city = params.city
        pois = params.pois

        if len(pois) > 20:
            input('Do you really want to process {} pois? (Enter)'.format(len(pois)))

        city = fetch.city(name=city)
        log(city, indent=0, verbose=True)

        start_point = fetch.point(name=params.from_place, city=city)
        log(start_point, indent=0, verbose=True)

        end_point = fetch.point(name=params.to_place, city=city)
        log(end_point, indent=0, verbose=True)

        params.set_coordinates(coord_from=start_point.coordinates, coord_to=end_point.coordinates)
        params.set_relative_time_window()

        targets = []
        pois_to_visualize = []

        pois_to_visualize.append(start_point)

        for poi in pois:
            poi = fetch.poi(name=poi, city=city)
            if poi:
                duration_of_stay = pois[poi.name] * 60  # in seconds
                target = Target(poi, duration_of_stay)
                targets.append(target)
                pois_to_visualize.append(poi)

                log(poi, indent=0, verbose=True)
                log(target, indent=0, verbose=True)

        pois_to_visualize.append(end_point)
        pois_ids = list(map(lambda p: p.id, pois_to_visualize))

        fetch.stats()

        optimization_content = fetch.optimization(targets, params)
        optimization = Optimization(optimization_content, pois_ids)
        visualize(optimization, pois_to_visualize)
    except KeyboardInterrupt:
        print()
