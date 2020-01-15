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
        self.waiting = None
        self.duration = None

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
            'arrival': str(self.arrival),
            'icon': self.icon.options['icon'] if self.icon else None
        }

        if hasattr(self, 'amenity'):
            content['amenity'] = self.amenity
        if hasattr(self, 'opening_hours'):
            content['opening_hours'] = self.opening_hours

        content['waiting time'] = str(self.waiting) if self.waiting else None
        content['duration of stay'] = str(self.duration) if self.duration else None

        return json.dumps(content, indent=2, ensure_ascii=False)

    def _form_popup(self):
        popup = ''
        self.popup_wide = False

        duration = ' {}'.format(utils.td2hstr(self.duration)) if self.duration else ''
        amenity = ' in {}'.format(self.amenity) if hasattr(self, 'amenity') else ''
        popup += '<b>{}</b>{}{}<br>'.format(self.name, duration, amenity)

        raw_arrival = self.arrival
        arrival = utils.dt2hstr(self.arrival)
        if not self.start and not self.end:
            popup += '{} {} ({})<br>'.format('↷', raw_arrival, arrival)
        if self.start:
            popup += '{} {} ({})<br>'.format('↦', raw_arrival, arrival)
        if self.end and hasattr(self, 'departure'):
            popup += '{} {} ({})<br>'.format('⇥', self.departure, utils.dt2hstr(self.departure))

        if hasattr(self, 'waiting') and self.waiting:
            popup += '⌛ {}<br>'.format(utils.td2hstr(self.waiting))
        if hasattr(self, 'opening_hours'):
            popup += '⏰ {}<br>'.format(self.opening_hours)
            self.popup_wide = True

        self.popup = popup

    def _form_tooltip(self):
        self.tooltip = self.name

    def _get_connection_description(self, neighbour, id, vehicle, end):
        desc = ''

        travel_dt = self.get_travel_datetime(neighbour)
        start = end - travel_dt
        travel_time = utils.td2hstr(travel_dt)

        if vehicle == 'driving-car':
            vehicle = '🚗'
        elif vehicle == 'foot-walking':
            vehicle = '🚶'
        elif vehicle == 'cycling-regular':
            vehicle = '🚲'
        elif vehicle == 'cycling-road':
            vehicle = '🚲'
        else:
            vehicle = 'Step {}'.format(id)

        desc += '{} {}<br>'.format(travel_time, vehicle)
        desc += '↦ {}<br>'.format(start)
        desc += '⇥ {}<br>'.format(end)

        return desc

    def get_travel_datetime(self, neighbour):
        travel_time = neighbour.arrival - self.arrival
        if self.waiting:
            travel_time -= self.waiting
        if self.duration:
            travel_time -= self.duration
        return travel_time

    def add_to_map(self, gmap):
        popup_width = 300 if self.popup_wide else 260
        popup_html = folium.Html(self.popup, script=True)
        popup = folium.Popup(popup_html, max_width=popup_width, min_width=popup_width)

        if self.icon:
            folium.Marker(self.coordinates, popup=popup, tooltip=self.tooltip, icon=self.icon).add_to(gmap)
        else:
            folium.Marker(self.coordinates, popup=popup, tooltip=self.tooltip).add_to(gmap)

    def connect(self, marker, gmap, pair_nr=None, vehicle='driving-car'):
        if self.id == marker.id:
            return

        popup_width = 140
        p1 = self.coordinates
        p2 = marker.coordinates

        connection_id = pair_nr + 1
        desc = self._get_connection_description(neighbour=marker, id=connection_id, vehicle=vehicle, end=marker.arrival)
        popup_html = folium.Html(desc, script=True)
        popup = folium.Popup(popup_html, max_width=popup_width, min_width=popup_width)

        folium.PolyLine(locations=[p1, p2], popup=popup).add_to(gmap)

        arrows = utils.get_arrows(locations=[p1, p2], n_arrows=1)
        for arrow in arrows:
            arrow.add_to(gmap)

    def set_end(self, departure):
        self.departure = departure
        self.end = True
        self._form_popup()

    @property
    def arrival_day_str(self):
        return self.arrival.weekday


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

    content_steps = json.loads(optimization_example.OPTIMIZATION)['routes'][0]['steps']

    print('markers:')
    for content in content_steps:
        step = Step(content, pois_ids)
        poi = Poi.from_id(pois, step.id)
        marker = Marker(poi, step)
        print(marker)
