#!/usr/bin/env python3
import folium
import json
import utils
import optimization_example
from poi import Poi
from step import Step


class Marker:
    def __init__(self, poi, step):
        self.id = poi.id
        self.name = poi.name
        self.coordinates = poi.coordinates
        self.start = step.start
        self.end = step.end
        self.icon = folium.Icon(icon='home') if step.start or step.end else None
        self.arrival = step.arrival

        if hasattr(poi, 'amenity'):
            self.amenity = poi.amenity
        if hasattr(poi, 'opening_hours'):
            self.opening_hours = poi.opening_hours
            self.opening_timestamps = poi.opening_timestamps
        if hasattr(step, 'waiting'):
            self.waiting = step.waiting
        if hasattr(step, 'duration'):
            self.duration = step.duration

        self._form_popup()
        self._form_tooltip()

    def __repr__(self):
        content = {
            'name': self.name,
            'coordinates': self.coordinates,
            'start': self.start,
            'end': self.end,
            'arrival': self.arrival,
            'icon': self.icon.options['icon'] if self.icon else None
        }

        if hasattr(self, 'amenity'):
            content['amenity'] = self.amenity
        if hasattr(self, 'opening_hours'):
            content['opening_hours'] = self.opening_hours
        if hasattr(self, 'waiting'):
            content['waiting time'] = self.waiting
        if hasattr(self, 'duration'):
            content['duration of stay'] = self.duration

        return json.dumps(content, indent=2)

    def _form_popup(self):
        self.popup = self.name

    def _form_tooltip(self):
        self.tooltip = self.name

    def add_to_map(self, gmap):
        if self.icon:
            folium.Marker(self.coordinates, popup=self.popup, tooltip=self.tooltip, icon=self.icon).add_to(gmap)
        else:
            folium.Marker(self.coordinates, popup=self.popup, tooltip=self.tooltip).add_to(gmap)

    def connect(self, marker, gmap):
        if self.id == marker.id:
            return

        p1 = self.coordinates
        p2 = marker.coordinates

        folium.PolyLine(locations=[p1, p2]).add_to(gmap)

        arrows = utils.get_arrows(locations=[p1, p2], n_arrows=1)
        for arrow in arrows:
            arrow.add_to(gmap)


if __name__ == '__main__':
    pois = [
        Poi('pois/Pętla Dworzec Centralny.json'),
        Poi('pois/U Szwejka.json'),
        Poi('pois/ORZO.json'),
        Poi('pois/Secado.json'),
        Poi('pois/Pomnik Wincentego Witosa.json'),
        Poi('pois/Pętla Dworzec Centralny.json')
    ]
    pois_ids = list(map(lambda p: p.id, pois))

    content_steps = json.loads(optimization_example.STEPS)

    print('markers:')
    for content in content_steps:
        step = Step(content, pois_ids)
        poi = Poi.from_id(pois, step.id)
        marker = Marker(poi, step)
        print(marker)
