#!/usr/bin/env python3
import json
from pathlib import Path
from city import City
from geocode import Geocode
from node import Node
from poi import Poi
from logger import log


class Database:
    PATHS = {
        Node: 'nodes',
        Geocode: 'geocodes',
        City: 'cities',
        Poi: 'pois'
    }

    EXTENSIONS = {
        Node: '.xml',
        Geocode: '.json',
        City: '.json',
        Poi: '.json'
    }

    def __init__(self):
        self._refresh()

    def _refresh(self):
        objtype = Node
        folder_path, extension = self.PATHS[objtype], self.EXTENSIONS[objtype]
        self.nodes_paths = sorted(Path(folder_path).glob('**/*{}'.format(extension)))

        objtype = Geocode
        folder_path, extension = self.PATHS[objtype], self.EXTENSIONS[objtype]
        self.geocodes_paths = sorted(Path(folder_path).glob('**/*{}'.format(extension)))

        objtype = City
        folder_path, extension = self.PATHS[objtype], self.EXTENSIONS[objtype]
        self.cities_paths = sorted(Path(folder_path).glob('**/*{}'.format(extension)))

        objtype = Poi
        folder_path, extension = self.PATHS[objtype], self.EXTENSIONS[objtype]
        self.pois_paths = sorted(Path(folder_path).glob('**/*{}'.format(extension)))

    def _get_object(self, id, collection, object_type):
        class_name = Database._get_class_name(object_type)

        for obj in collection:
            identifier = obj.stem

            if type(id) is int:
                identifier = int(identifier)
            if identifier != id:
                continue

            obj = object_type(obj)
            identifier = obj.id if type(id) is int else obj.name
            log('db/{}: got {}'.format(class_name, identifier))
            return obj

        log('db/{}: not {}'.format(class_name, id))
        return None

    def _put_object(self, id, content, object_type):
        class_name = Database._get_class_name(object_type)
        path = self.PATHS[object_type]
        extension = self.EXTENSIONS[object_type]
        filename = Path(path).joinpath('{}{}'.format(id, extension))
        with open(filename, 'w') as f:
            if type(content) is dict:
                content = json.dumps(content, indent=2, ensure_ascii=False)
            f.write(str(content).strip())
            f.write('\n')
        obj = object_type(filename)
        identifier = obj.id if type(id) is int else obj.name
        log('db/{}: put {}'.format(class_name, identifier))
        return obj

    def get_geocode(self, id):
        return self._get_object(id=id, collection=self.geocodes_paths, object_type=Geocode)

    def put_geocode(self, id, content):
        return self._put_object(id=id, content=content, object_type=Geocode)

    def get_node(self, id):
        return self._get_object(id=id, collection=self.nodes_paths, object_type=Node)

    def put_node(self, id, content):
        return self._put_object(id=id, content=content, object_type=Node)

    def get_city(self, name):
        return self._get_object(id=name, collection=self.cities_paths, object_type=City)

    def put_city(self, name, content):
        return self._put_object(id=name, content=content, object_type=City)

    def get_poi(self, name):
        return self._get_object(id=name, collection=self.pois_paths, object_type=Poi)

    def put_poi(self, name, content):
        return self._put_object(id=name, content=content, object_type=Poi)

    def print_stats(self):
        self._refresh()

        geocodes = len(self.geocodes_paths)
        nodes = len(self.geocodes_paths)
        cities = len(self.cities_paths)
        pois = len(self.pois_paths)

        log('db stats: geocodes {} nodes {} cities {} pois {}'.format(
            geocodes, nodes, cities, pois
        ))

    @staticmethod
    def _get_class_name(object_type):
        name = str(object_type)
        name = name.replace("<class '", '').replace("'>", '').split('.', 1)[1].lower()
        return name


if __name__ == '__main__':
    def log_object(obj, identifier):
        log('{}:'.format(identifier), verbose=True)
        log(obj, indent=0, verbose=True)

    import db_example
    db = Database()

    # Node
    node = db.get_node(123456789)
    node = db.get_node(316886479)
    log_object(node, node.id)

    raw_node = db_example.NODE
    db.put_node(312892887, raw_node)

    # Geocode
    geocode = db.get_geocode(123456789)
    geocode = db.get_geocode(1366473642)
    log_object(geocode, geocode.id)

    raw_geocode = db_example.GEOCODE
    db.put_geocode(101752117, raw_geocode)

    # City
    city = db.get_city('Awaszraw')
    city = db.get_city('Warszawa')
    log_object(city, city.name)

    raw_city = db_example.CITY
    db.put_city('Kraków', raw_city)

    # Poi
    poi = db.get_poi('ZORRO')
    poi = db.get_poi('ORZO')
    log_object(poi, poi.name)

    raw_poi = db_example.POI
    db.put_poi('Secado', raw_poi)
