#!/usr/bin/env python3
import json
import xml.etree.ElementTree as et
from utils import ophrs2tsa


class Node:
    def __init__(self, filename):
        tree = et.parse(filename)
        root = tree.getroot()
        node = root[0]
        attrib = node.attrib

        if 'id' in attrib:
            self.id = int(attrib['id'])
        if 'lat' in attrib and 'lon' in attrib:
            self.coordinates = [float(attrib['lat']), float(attrib['lon'])]

        for tag in node:
            attrib = tag.attrib
            key = attrib['k']
            val = attrib['v']

            if key == 'addr:city':
                self.city = val
            elif key == 'amenity':
                self.amenity = val
            elif key == 'name':
                self.name = val
            elif key == 'opening_hours':
                self.opening_timestamps = ophrs2tsa(val)
                self.opening_hours = val

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

        return json.dumps(content, indent=2)


if __name__ == '__main__':
    node = Node('nodes/316886479.xml')
    print(node)
